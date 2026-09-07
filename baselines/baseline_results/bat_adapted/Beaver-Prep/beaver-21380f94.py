import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['EMAIL_ADDRESS'] = df['EMAIL_ADDRESS'].astype('string')
    df = df[df['EMAIL_ADDRESS'].notna() & (df['EMAIL_ADDRESS'].str.strip() != '')]
    target = df[['EMAIL_ADDRESS','FULL_NAME','STUDENT_YEAR','DEPARTMENT_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['DEPARTMENT_NAME','DEPARTMENT_CODE','SCHOOL_CODE','SCHOOL_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_duo_users = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_departments = prepared_table_2

# prepared_duo_users and prepared_departments are the synthesized per-table outputs

# 1) Identify students in the duo mailing list (assuming STUDENT_YEAR non-null/non-empty denotes a student)
students = prepared_duo_users.copy()
students['STUDENT_YEAR'] = students['STUDENT_YEAR'].astype(str).str.strip()
students = students[students['STUDENT_YEAR'].notna() & (students['STUDENT_YEAR'] != '')]

# 2) Join to department-school mapping on department name
joined = students.merge(
    prepared_departments,
    how='left',
    left_on='DEPARTMENT_NAME',
    right_on='DEPARTMENT_NAME'
)

# 3) Compute required counts
num_students = students['EMAIL_ADDRESS'].nunique()
num_departments = joined['DEPARTMENT_NAME'].nunique()
num_schools = joined['SCHOOL_NAME'].dropna().nunique()

answer = {
    'num_students_in_mailing_list': int(num_students),
    'num_departments_for_these_students': int(num_departments),
    'num_schools_for_these_students': int(num_schools)
}

target = pd.DataFrame([answer])

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
