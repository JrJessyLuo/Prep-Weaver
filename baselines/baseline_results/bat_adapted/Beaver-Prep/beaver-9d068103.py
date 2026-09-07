import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME','MOIRA_LIST_MEMBER_MIT_ID']].copy()
    df['moira_list_member'] = df['moira_list_member'].astype('string').str.strip()
    target = df[['MOIRA_LIST_KEY','moira_list_member','MOIRA_LIST_MEMBER_FULL_NAME','MOIRA_LIST_MEMBER_MIT_ID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['EMAIL_ADDRESS','FULL_NAME','FULL_NAME_UPPERCASE','DEPARTMENT','DEPARTMENT_NAME','STUDENT_YEAR']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['SIS_ADMIN_DEPARTMENT_CODE','SIS_ADMIN_DEPARTMENT_NAME','DEPARTMENT_PHONE_AREA_CODE','department_phone_number']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_mailing_list_members = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_people = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_departments = prepared_table_3

# 1) Filter mailing list to the requested list and normalize username
ml = prepared_mailing_list_members.copy()
ml = ml[ml['MOIRA_LIST_KEY'] == 'ocean-apple']
ml['member_user'] = ml['moira_list_member'].astype(str).str.strip().str.lower()

# 2) Prepare people with username extracted from email and keep only students
pp = prepared_people.copy()
pp['email_user'] = pp['EMAIL_ADDRESS'].astype(str).str.split('@').str[0].str.strip().str.lower()
# Consider a record a student if STUDENT_YEAR not null/empty
pp_students = pp[pp['STUDENT_YEAR'].notna() & (pp['STUDENT_YEAR'].astype(str).str.strip() != '')]

# 3) Join mailing list members to people via username = email local part
m_join = ml.merge(pp_students, left_on='member_user', right_on='email_user', how='inner')

# 4) Normalize department names for joining to department phone table
m_join['dept_name_norm'] = m_join['DEPARTMENT_NAME'].astype(str).str.strip().str.lower()

pdpt = prepared_departments.copy()
pdpt['dept_name_norm'] = pdpt['SIS_ADMIN_DEPARTMENT_NAME'].astype(str).str.strip().str.lower()

# 5) Join to get department phone
mj = m_join.merge(pdpt[['dept_name_norm','DEPARTMENT_PHONE_AREA_CODE','department_phone_number','SIS_ADMIN_DEPARTMENT_NAME']],
                  on='dept_name_norm', how='left')

# 6) Aggregate: count students per department name; keep phone fields
grp = mj.groupby(['DEPARTMENT_NAME','DEPARTMENT_PHONE_AREA_CODE','department_phone_number'], dropna=False).size().reset_index(name='student_count')

# 7) Find max and filter departments with that max
max_cnt = grp['student_count'].max() if len(grp) else 0
result = grp[grp['student_count'] == max_cnt].copy()

# 8) Prepare final columns: department name, phone number, total students
# Compose phone as area code + number when available
def format_phone(row):
    ac = '' if pd.isna(row['DEPARTMENT_PHONE_AREA_CODE']) else str(int(float(row['DEPARTMENT_PHONE_AREA_CODE'])))
    num = '' if pd.isna(row['department_phone_number']) else str(int(float(row['department_phone_number'])))
    if ac and num:
        return f"({ac}) {num}"
    elif num:
        return num
    else:
        return None

result['PHONE'] = result.apply(format_phone, axis=1)
answer = result[['DEPARTMENT_NAME','PHONE','student_count']].rename(columns={'DEPARTMENT_NAME':'department_name','PHONE':'phone','student_count':'total_students'})
# 'answer' is the final DataFrame

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
