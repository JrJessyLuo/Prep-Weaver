import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_MATERIAL_STATUS_KEY','TERM_CODE','SUBJECT_ID','LIBRARY_COURSE_INSTRUCTOR_KEY']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS_CODE','LIBRARY_MATERIAL_STATUS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['term_code','TERM_DESCRIPTION']].copy()
    prepared = prepared.drop_duplicates(subset=['term_code'])
    target = prepared[['term_code','TERM_DESCRIPTION']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_library_reserves = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_material_status_ref = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_terms = prepared_table_3
prepared_table_4 = _prep_4(tables['table_8'])
prepared_subject_org = prepared_table_4

# Start from prepared tables
res = prepared_library_reserves.copy()
status_ref = prepared_material_status_ref.copy()
terms = prepared_terms.copy()
org = prepared_subject_org.copy()

# Join status reference (many-to-one)
res1 = res.merge(status_ref, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')

# Join term description
res2 = res1.merge(terms, left_on='TERM_CODE', right_on='term_code', how='left')

# Join organizational mapping by term to enable counting occurrences across departments and schools
res_org = res2.merge(org[['TERM_CODE','DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']], on='TERM_CODE', how='left')

# Derive instructor id from composite if needed (assume instructor component precedes term in LIBRARY_COURSE_INSTRUCTOR_KEY separated by '-')
# If the composite structure is different, adjust parsing accordingly.
def extract_instructor(x):
    if pd.isna(x):
        return pd.NA
    # Example formats observed like '4.602-VANCE2010SP:4.602'; take segment before TERM_CODE by splitting on ':' first
    left = str(x).split(':')[0]
    # then split on '-' to separate subject and instructor+term; take middle if present
    parts = left.split('-')
    if len(parts) >= 2:
        return parts[1]
    return left

res_org['INSTRUCTOR_TOKEN'] = res_org['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(extract_instructor)

# Aggregate metrics per material status code and term code
agg = res_org.groupby(['LIBRARY_MATERIAL_STATUS_CODE','TERM_CODE','LIBRARY_MATERIAL_STATUS','TERM_DESCRIPTION'], dropna=False).agg(
    total_courses=pd.NamedAgg(column='SUBJECT_ID', aggfunc=lambda s: s.dropna().nunique()),
    total_materials=pd.NamedAgg(column='LIBRARY_RESERVE_CATALOG_KEY', aggfunc=lambda s: s.dropna().nunique()),
    occurrences_in_departments=pd.NamedAgg(column='DEPARTMENT_CODE', aggfunc=lambda s: s.dropna().nunique()),
    occurrences_in_schools=pd.NamedAgg(column='SCHOOL_NAME', aggfunc=lambda s: s.dropna().nunique()),
    total_instructors=pd.NamedAgg(column='INSTRUCTOR_TOKEN', aggfunc=lambda s: s.dropna().nunique())
).reset_index()

# Final selection and ordering
target = agg.rename(columns={
    'LIBRARY_MATERIAL_STATUS_CODE': 'material_status_code',
    'LIBRARY_MATERIAL_STATUS': 'material_status',
    'TERM_CODE': 'term_code',
    'TERM_DESCRIPTION': 'term_description'
})

# target now has: material_status_code, material_status, term_code, term_description,
# total_courses, total_materials, occurrences_in_departments, occurrences_in_schools, total_instructors

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
