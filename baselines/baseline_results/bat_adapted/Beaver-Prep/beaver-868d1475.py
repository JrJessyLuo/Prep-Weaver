import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['MOIRA_LIST_NAME','IS_ACTIVE','IS_MOIRA_MAILING_LIST']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['EMAIL_ADDRESS','DEPARTMENT_NAME','STUDENT_YEAR']].copy()
    df['STUDENT_YEAR'] = df['STUDENT_YEAR'].astype('string')
    df['EMAIL_ADDRESS'] = df['EMAIL_ADDRESS'].astype('string')
    df = df[df['STUDENT_YEAR'].notna() & (df['STUDENT_YEAR'].str.strip() != '')]
    df = df[df['EMAIL_ADDRESS'].notna() & (df['EMAIL_ADDRESS'].str.strip() != '')]
    target = df.drop_duplicates()[['EMAIL_ADDRESS','DEPARTMENT_NAME','STUDENT_YEAR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_lists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_people = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])

# Assumptions for integration: membership expansion from the mailing list to individual emails is required but not present in the selected tables.
# Therefore, derive membership solely from people whose email addresses match the mailing list name via conventional list-address pattern (not available),
# which is insufficient. To correctly answer, a list-membership table mapping list names to member email addresses is needed.

# Placeholder to show intended logic if a membership mapping were available as `prepared_members` with columns: MOIRA_LIST_NAME, EMAIL_ADDRESS
# prepared_members = ...  # synthesized from the actual membership table

# Filter to the requested list (and active Moira mailing lists)
lists_f = prepared_lists.copy()
lists_f['MOIRA_LIST_NAME'] = lists_f['MOIRA_LIST_NAME'].str.strip()
list_name = 'kangaroo-inspire-yearn'
lists_f = lists_f[(lists_f['MOIRA_LIST_NAME'] == list_name) & (lists_f['IS_ACTIVE'] == 'Y') & (lists_f['IS_MOIRA_MAILING_LIST'] == 'Y')]

# Join members to people to bring department and student status
# members_in_list = prepared_members.merge(lists_f[['MOIRA_LIST_NAME']], on='MOIRA_LIST_NAME', how='inner')
# people_in_list = members_in_list.merge(prepared_people, on='EMAIL_ADDRESS', how='left')

# Keep only students (STUDENT_YEAR not null/empty)
# students = people_in_list[people_in_list['STUDENT_YEAR'].notna() & (people_in_list['STUDENT_YEAR'].astype(str).str.strip() != '')]

# Aggregate by department name
# dept_counts = students.groupby('DEPARTMENT_NAME', dropna=False).size().reset_index(name='student_count')
# total = dept_counts['student_count'].sum()
# dept_counts['percentage'] = (dept_counts['student_count'] / total * 100).round(2)
# result = dept_counts.rename(columns={'DEPARTMENT_NAME': 'department_name'})[['department_name', 'student_count', 'percentage']]

# result

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
