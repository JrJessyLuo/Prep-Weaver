import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['DEPARTMENT_NAME','FULL_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['SIS_ADMIN_DEPARTMENT_NAME','department_phone_number']].copy()
    df['department_phone_number'] = df['department_phone_number'].where(df['department_phone_number'].notna(), pd.NA)
    df['department_phone_number'] = df['department_phone_number'].astype('string').str.replace(r'\.0$', '', regex=True)
    target = df[['SIS_ADMIN_DEPARTMENT_NAME','department_phone_number']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_departments = prepared_table_2

# Assume prepared_students and prepared_departments already materialized as per target schemas
# 1) Integrate on department name
merged = prepared_students.merge(
    prepared_departments,
    left_on='DEPARTMENT_NAME',
    right_on='SIS_ADMIN_DEPARTMENT_NAME',
    how='left'
)

# 2) Compute per-department aggregates
# Name length based on FULL_NAME string length
merged['name_len'] = merged['FULL_NAME'].fillna('').str.len()

gb = merged.groupby(['DEPARTMENT_NAME', 'department_phone_number'], dropna=False)
result = gb.agg(
    number_of_students=('FULL_NAME', 'count'),
    longest_full_name_length=('name_len', 'max')
).reset_index()

# 3) Rename columns to match requested output semantics
result = result.rename(columns={
    'DEPARTMENT_NAME': 'department_name',
    'department_phone_number': 'department_phone_number'
})

# Final output in result with columns: department_name, department_phone_number, number_of_students, longest_full_name_length
output = result[['department_name', 'department_phone_number', 'number_of_students', 'longest_full_name_length']]

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
