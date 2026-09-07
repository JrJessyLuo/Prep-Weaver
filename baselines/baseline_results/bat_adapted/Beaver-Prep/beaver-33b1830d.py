import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['DEPARTMENT','DEPARTMENT_NAME','SCHOOL_NAME','COURSE_LEVEL','IS_DEGREE_GRANTING']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['DEPARTMENT_CODE','department_full_name','SCHOOL_CODE','SCHOOL_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_courses_by_dept_level = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_department_lookup = prepared_table_2

integrated = prepared_courses_by_dept_level.merge(prepared_department_lookup, left_on='DEPARTMENT', right_on='DEPARTMENT_CODE', how='left')
# Normalize degree-granting flag
integrated['is_deg'] = (integrated['IS_DEGREE_GRANTING'].astype(str).str.upper() == 'Y')
# Aggregate by school code, school name, department full name, and course level
answer = (
    integrated.groupby(['SCHOOL_CODE', 'SCHOOL_NAME_y', 'department_full_name', 'COURSE_LEVEL'], dropna=False)
    .agg(total_courses=('COURSE_LEVEL', 'size'), total_degree_granting=('is_deg', 'sum'))
    .reset_index()
)
# Rename SCHOOL_NAME_y to SCHOOL_NAME if merge produced suffixes
if 'SCHOOL_NAME_y' in answer.columns:
    answer = answer.rename(columns={'SCHOOL_NAME_y': 'SCHOOL_NAME'})
# Final selected columns in required order
answer = answer[['SCHOOL_CODE', 'SCHOOL_NAME', 'department_full_name', 'COURSE_LEVEL', 'total_courses', 'total_degree_granting']]

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
