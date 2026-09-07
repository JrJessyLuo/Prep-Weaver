import pandas as pd
import numpy as np

def _prep_1(table_1):
    source = table_1.copy()
    target = source[['SUBJECT_ID','SUBJECT_CODE','SUBJECT_TITLE','SUBJECT_DESCRIPTION','TOTAL_UNITS','DEPARTMENT_CODE','DEPARTMENT_NAME','COMM_REQ_ATTRIBUTE','COMM_REQ_ATTRIBUTE_DESC']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['hass_attribute','DESCRIPTION_ON_FORM','DESCRIPTION_IN_BULLETIN','CIS_ATTRIBUTE_GROUP','CIS_ATTRIBUTE_GROUP_NOTE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['SUBJECT_CODE','SUBJECT_CODE_DESC','DEPARTMENT_CODE','DEPARTMENT_NAME']].copy()
    df = df.drop_duplicates()
    target = df[['SUBJECT_CODE','SUBJECT_CODE_DESC','DEPARTMENT_CODE','DEPARTMENT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    prepared = table_1[['SUBJECT_ID','TERM_CODE','TOTAL_UNITS','SUBJECT_ENROLLMENT_NUMBER','NUM_ENROLLED_STUDENTS','OFFER_DEPT_CODE','OFFER_DEPT_NAME']].copy()
    prepared['TOTAL_UNITS'] = pd.to_numeric(prepared['TOTAL_UNITS'], errors='coerce')
    prepared['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(prepared['SUBJECT_ENROLLMENT_NUMBER'], errors='coerce')
    prepared['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(prepared['NUM_ENROLLED_STUDENTS'], errors='coerce')
    prepared = prepared.groupby(['SUBJECT_ID','TERM_CODE','OFFER_DEPT_CODE','OFFER_DEPT_NAME'], as_index=False).agg({'TOTAL_UNITS':'first','SUBJECT_ENROLLMENT_NUMBER':'sum','NUM_ENROLLED_STUDENTS':'sum'})
    target = prepared[['SUBJECT_ID','TERM_CODE','TOTAL_UNITS','SUBJECT_ENROLLMENT_NUMBER','NUM_ENROLLED_STUDENTS','OFFER_DEPT_CODE','OFFER_DEPT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_5(table_1):
    prepared = table_1[['DEPARTMENT','DEPARTMENT_NAME','IS_DEGREE_GRANTING']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['DEPARTMENT','DEPARTMENT_NAME','IS_DEGREE_GRANTING']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_hass_attributes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_subject_codes = prepared_table_3
prepared_table_4 = _prep_4(tables['table_7'])
prepared_offerings = prepared_table_4
prepared_table_5 = _prep_5(tables['table_8'])
prepared_departments = prepared_table_5

# Start from prepared tables
subjects = prepared_subjects.copy()
hass_ref = prepared_hass_attributes.copy()
code_map = prepared_subject_codes.copy()
offerings = prepared_offerings.copy()
departments = prepared_departments.copy()

# 1) Identify Political Science by SUBJECT_CODE description and restrict to HASS-bearing attributes
# Political Science code is typically '17'. Use SUBJECT_CODE_DESC to be robust
pol_codes = code_map[code_map['SUBJECT_CODE_DESC'].str.contains('Political Science', case=False, na=False)]['SUBJECT_CODE'].unique()
pol_subjects = subjects[subjects['SUBJECT_CODE'].isin(pol_codes)].copy()

# HASS attributes live in COMM_REQ_ATTRIBUTE; keep rows where attribute present and exists in HASS ref
pol_subjects = pol_subjects.merge(hass_ref, left_on='COMM_REQ_ATTRIBUTE', right_on='hass_attribute', how='inner')

# 2) Add subject code description for output
pol_subjects = pol_subjects.merge(code_map[['SUBJECT_CODE','SUBJECT_CODE_DESC']], on='SUBJECT_CODE', how='left')

# 3) Aggregate enrollments across offerings per subject and attribute
offer_agg = offerings.groupby('SUBJECT_ID', as_index=False).agg(
    total_enrollment=('SUBJECT_ENROLLMENT_NUMBER','sum'),
    total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum'),
    avg_units=('TOTAL_UNITS','mean')
)

pol_enriched = pol_subjects.merge(offer_agg, on='SUBJECT_ID', how='left')

# 4) Count degree-granting departments involved: join departments on department code and flag
dept_merge = pol_subjects[['SUBJECT_ID','DEPARTMENT_CODE']].drop_duplicates().merge(
    departments[['DEPARTMENT','IS_DEGREE_GRANTING']], left_on='DEPARTMENT_CODE', right_on='DEPARTMENT', how='left'
)
# normalize flag
dept_merge['is_deg'] = dept_merge['IS_DEGREE_GRANTING'].astype(str).str.upper().str.strip().eq('Y')

dept_counts = dept_merge.groupby('SUBJECT_ID', as_index=False)['is_deg'].sum().rename(columns={'is_deg':'num_deg_granting_depts'})

pol_enriched = pol_enriched.merge(dept_counts, on='SUBJECT_ID', how='left')

# 5) Final aggregation per HASS attribute (code), providing attribute name/description, counts, averages, totals
result = pol_enriched.groupby(['COMM_REQ_ATTRIBUTE','DESCRIPTION_ON_FORM','DESCRIPTION_IN_BULLETIN','SUBJECT_CODE_DESC'], as_index=False).agg(
    num_unique_subjects=('SUBJECT_ID','nunique'),
    average_units=('avg_units','mean'),
    total_enrollment=('total_enrollment','sum'),
    num_departments_granting_degrees=('num_deg_granting_depts','sum')
)

# Rename columns as requested
result = result.rename(columns={
    'COMM_REQ_ATTRIBUTE': 'attribute_code',
    'DESCRIPTION_ON_FORM': 'attribute_name',
    'DESCRIPTION_IN_BULLETIN': 'attribute_description',
    'SUBJECT_CODE_DESC': 'subject_code_description'
})

target = result

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
