import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_PUBLIC']].copy()
    prepared['MOIRA_LIST_KEY'] = prepared['MOIRA_LIST_KEY'].astype(str).str.strip()
    target = prepared[['MOIRA_LIST_KEY','MOIRA_LIST_NAME','IS_PUBLIC']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['moira_list_member'] = df['moira_list_member'].astype('string').str.strip()
    target = df[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME','MOIRA_LIST_MEMBER_MIT_ID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    source = table_1.copy()
    source = source[['FULL_NAME','FULL_NAME_UPPERCASE','EMAIL_ADDRESS','DEPARTMENT','DEPARTMENT_NAME','STUDENT_YEAR']]
    source['FULL_NAME'] = source['FULL_NAME'].astype('string').str.strip()
    source['FULL_NAME_UPPERCASE'] = source['FULL_NAME_UPPERCASE'].astype('string').str.strip()
    source['EMAIL_ADDRESS'] = source['EMAIL_ADDRESS'].astype('string').str.strip().str.lower()
    source['DEPARTMENT'] = source['DEPARTMENT'].astype('string').str.strip()
    source['DEPARTMENT_NAME'] = source['DEPARTMENT_NAME'].astype('string').str.strip()
    source['STUDENT_YEAR'] = source['STUDENT_YEAR'].astype('string').str.strip()
    source['__dedupe_key__'] = source['EMAIL_ADDRESS'].where(source['EMAIL_ADDRESS'].notna() & (source['EMAIL_ADDRESS'] != ''), source['FULL_NAME_UPPERCASE'])
    source = source.drop_duplicates(subset=['__dedupe_key__'], keep='first')
    target = source.drop(columns=['__dedupe_key__'])[['FULL_NAME','FULL_NAME_UPPERCASE','EMAIL_ADDRESS','DEPARTMENT','DEPARTMENT_NAME','STUDENT_YEAR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.loc[:, ['DEPARTMENT_CODE','DEPARTMENT_NAME','DEPARTMENT_FULL_NAME','SCHOOL_CODE','SCHOOL_NAME']].copy()
    target = target.apply(lambda s: s.astype(str).str.replace(r'\s+', ' ', regex=True).str.strip())
    target = target.drop_duplicates(subset=['DEPARTMENT_CODE','DEPARTMENT_NAME','DEPARTMENT_FULL_NAME','SCHOOL_CODE','SCHOOL_NAME']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_memberships = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_people = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
prepared_departments = prepared_table_4

# Assume the prepared tables are provided as DataFrames: prepared_lists, prepared_memberships, prepared_people, prepared_departments

# 1) Join lists to memberships
lm = prepared_memberships.merge(prepared_lists, on='MOIRA_LIST_KEY', how='inner')

# 2) Normalize identifiers for joining memberships to people via email address
# Derive username from EMAIL_ADDRESS in people and compare to moira_list_member (both upper-trimmed)
people = prepared_people.copy()
people['EMAIL_USER'] = people['EMAIL_ADDRESS'].fillna('').str.split('@').str[0]
people['EMAIL_USER_NORM'] = people['EMAIL_USER'].str.strip().str.upper()

m = lm.copy()
m['MEMBER_NORM'] = m['moira_list_member'].astype(str).str.strip().str.upper()

# Primary join via email username == moira_list_member
lm_person = m.merge(
    people,
    left_on='MEMBER_NORM',
    right_on='EMAIL_USER_NORM',
    how='left',
    suffixes=('', '_p')
)

# For members not matched by email, try FULL_NAME matching using provided full name in memberships when available
unmatched = lm_person[lm_person['EMAIL_USER_NORM'].isna()].copy()
if not unmatched.empty:
    people_name = people[['FULL_NAME', 'FULL_NAME_UPPERCASE', 'DEPARTMENT', 'DEPARTMENT_NAME', 'STUDENT_YEAR']].copy()
    people_name['FULL_NAME_NORM'] = people_name['FULL_NAME'].fillna('').str.strip().str.upper()
    unmatched['MEMBER_FULLNAME_NORM'] = unmatched['MOIRA_LIST_MEMBER_FULL_NAME'].fillna('').str.strip().str.upper()
    rematch = unmatched.merge(
        people_name,
        left_on='MEMBER_FULLNAME_NORM',
        right_on='FULL_NAME_NORM',
        how='left',
        suffixes=('', '_n')
    )
    # Combine back, preferring email-based matches when present
    matched_email = lm_person[~lm_person['EMAIL_USER_NORM'].isna()]
    lm_person = pd.concat([matched_email, rematch], ignore_index=True, sort=False)

# 3) Compute total subscribers per list (distinct members to be safe)
lm_person['member_id_for_count'] = lm_person['moira_list_member'].astype(str).str.strip().str.upper()
subs_per_list = (
    lm_person.groupby(['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_PUBLIC'])['member_id_for_count']
    .nunique()
    .reset_index(name='total_subscribers')
)

# 4) Identify students and their departments (filter student indicator; keep department code/name)
lm_person['IS_STUDENT'] = lm_person['STUDENT_YEAR'].notna() & (lm_person['STUDENT_YEAR'].astype(str).str.strip() != '')
student_rows = lm_person[lm_person['IS_STUDENT']].copy()

# Map department code/name via departments reference when department code is present
student_rows = student_rows.merge(
    prepared_departments,
    left_on='DEPARTMENT',
    right_on='DEPARTMENT_CODE',
    how='left',
    suffixes=('', '_dept')
)

# Prefer canonical department name from departments table, else fallback to people.DEPRTMENT_NAME
student_rows['DEPT_NAME_FINAL'] = student_rows['DEPARTMENT_NAME'].where(
    student_rows['DEPARTMENT_NAME'].notna() & (student_rows['DEPARTMENT_NAME'].astype(str).str.strip() != ''),
    student_rows['DEPARTMENT_NAME_dept']
)
student_rows['DEPT_NAME_FINAL'] = student_rows['DEPT_NAME_FINAL'].fillna(student_rows['DEPARTMENT_NAME_dept'])

# Count students per department within each list
stud_counts = (
    student_rows.groupby(['MOIRA_LIST_KEY', 'DEPT_NAME_FINAL'])['member_id_for_count']
    .nunique()
    .reset_index(name='students_in_dept')
)

# For each list, select department with max students; ties broken by alphabetical department name for determinism
stud_counts_sorted = stud_counts.sort_values(['MOIRA_LIST_KEY', 'students_in_dept', 'DEPT_NAME_FINAL'], ascending=[True, False, True])
max_dept_per_list = stud_counts_sorted.groupby('MOIRA_LIST_KEY').head(1)

# 5) Combine totals with max department info
result = subs_per_list.merge(max_dept_per_list[['MOIRA_LIST_KEY', 'DEPT_NAME_FINAL', 'students_in_dept']], on='MOIRA_LIST_KEY', how='left')

# 6) Select top 100 lists by total subscribers
result_top100 = result.sort_values('total_subscribers', ascending=False).head(100)

# 7) Final projection
final = result_top100.rename(columns={
    'MOIRA_LIST_NAME': 'list_name',
    'IS_PUBLIC': 'is_public',
    'DEPT_NAME_FINAL': 'top_department_name',
    'students_in_dept': 'students_from_top_department'
})[
    ['list_name', 'total_subscribers', 'is_public', 'top_department_name', 'students_from_top_department']
]

target = final

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
