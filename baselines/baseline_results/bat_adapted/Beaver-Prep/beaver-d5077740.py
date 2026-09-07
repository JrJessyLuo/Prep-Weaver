import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['CLUSTER_TYPE','CLUSTER_TYPE_DESC','OFFER_DEPT_CODE','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME','SUBJECT_ID','TERM_CODE','SUBJECT_ENROLLMENT_NUMBER','NUM_ENROLLED_STUDENTS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME','IS_DEGREE_GRANTING']].copy()
    df = df.drop_duplicates(subset=['DEPARTMENT_CODE'])
    target = df[['DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME','IS_DEGREE_GRANTING']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_subject_offerings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
prepared_departments = prepared_table_2

# Assume prepared_subject_offerings (s1) and prepared_departments (d1) are provided per the targets above
s1 = prepared_subject_offerings.copy()
d1 = prepared_departments.copy()

# Integrate on department code
merged = s1.merge(d1, left_on='OFFER_DEPT_CODE', right_on='DEPARTMENT_CODE', how='left')

# Compute enrollment per row; prefer NUM_ENROLLED_STUDENTS if present, else SUBJECT_ENROLLMENT_NUMBER
enroll = merged['NUM_ENROLLED_STUDENTS']
if 'NUM_ENROLLED_STUDENTS' in merged and merged['NUM_ENROLLED_STUDENTS'].notna().any():
    enroll = merged['NUM_ENROLLED_STUDENTS']
else:
    enroll = merged['SUBJECT_ENROLLMENT_NUMBER']
merged['enrollment_val'] = pd.to_numeric(enroll, errors='coerce')

# Exclude groups with no student data: drop rows where enrollment is NaN or 0
merged_nonzero = merged[merged['enrollment_val'] > 0]

# Group and aggregate
grp_cols = [
    'CLUSTER_TYPE',
    'OFFER_DEPT_NAME',
    'SCHOOL_NAME'
]
agg_df = (
    merged_nonzero
    .groupby(grp_cols, dropna=False)
    .agg(
        IS_DEGREE_GRANTING=('IS_DEGREE_GRANTING', 'first'),
        total_subjects=('SUBJECT_ID', 'nunique'),
        total_enrollment=('enrollment_val', 'sum'),
        average_enrollment=('enrollment_val', 'mean')
    )
    .reset_index()
)

# Rename for final output clarity
agg_df = agg_df.rename(columns={
    'CLUSTER_TYPE': 'cluster_type',
    'OFFER_DEPT_NAME': 'department_name',
    'SCHOOL_NAME': 'school_name',
    'IS_DEGREE_GRANTING': 'department_grants_degrees',
    'total_subjects': 'total_number_of_subjects',
    'total_enrollment': 'total_enrollment',
    'average_enrollment': 'average_enrollment'
})

# Result in agg_df with required columns
result = agg_df[['cluster_type', 'department_name', 'school_name', 'department_grants_degrees', 'total_number_of_subjects', 'total_enrollment', 'average_enrollment']]

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
