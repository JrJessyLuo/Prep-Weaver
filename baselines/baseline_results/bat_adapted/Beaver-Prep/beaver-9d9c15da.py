import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['SUBJECT_SUMMARY_KEY','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_NAME','CLUSTER_TYPE','HGN_CODE','SUBJECT_ENROLLMENT_NUMBER','CLUSTER_ENROLLMENT_NUMBER']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_NAME','NUM_ENROLLED_STUDENTS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','subject_id','TIP_MATERIAL_KEY','ISBN','RECORD_COUNT']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_5(table_1):
    target = table_1[['TIP_MATERIAL_KEY','ISBN','TITLE','NEW_SHELF_PRICE','USED_SHELF_PRICE','MATERIAL_INFO_SOURCE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_tip_subjects = prepared_table_3
prepared_table_4 = _prep_4(tables['table_1'])
prepared_tip_material_links = prepared_table_4
prepared_table_5 = _prep_5(tables['table_4'])
prepared_tip_materials = prepared_table_5

# Start from prepared per-table dataframes: prepared_subject_offerings (table_2), prepared_tip_subjects (table_3), prepared_tip_material_links (table_4), prepared_tip_materials (table_5)

# 1) Filter biology courses: SUBJECT_TITLE contains 'Biology' (case-insensitive)
biol = prepared_subject_offerings[prepared_subject_offerings['SUBJECT_TITLE'].str.contains('biology', case=True, na=False) | prepared_subject_offerings['SUBJECT_TITLE'].str.contains('Biology', na=False)]

# 2) Join offerings to TIP subjects on (SUBJECT_ID, TERM_CODE)
basel = biol.merge(prepared_tip_subjects, how='left', left_on=['SUBJECT_ID','TERM_CODE'], right_on=['SUBJECT_ID','TERM_CODE'], suffixes=('', '_tip'))

# 3) Bring in TIP subject->material links via TIP_SUBJECT_OFFERED_KEY
links = basel.merge(prepared_tip_material_links, how='left', left_on='TIP_SUBJECT_OFFERED_KEY', right_on='TIP_SUBJECT_OFFERED_KEY')

# 4) Bring in material pricing
full = links.merge(prepared_tip_materials, how='left', left_on='TIP_MATERIAL_KEY', right_on='TIP_MATERIAL_KEY', suffixes=('', '_mat'))

# 5) Compute aggregations needed per group: by (CLUSTER_TYPE, HGN_CODE)
# First, per subject offering compute material-level stats
agg_per_subject = full.groupby(['SUBJECT_SUMMARY_KEY','CLUSTER_TYPE','HGN_CODE','OFFER_DEPT_NAME','SUBJECT_TITLE'], dropna=False).agg(
    total_enroll=('SUBJECT_ENROLLMENT_NUMBER','sum'),
    cluster_enroll=('CLUSTER_ENROLLMENT_NUMBER','mean'),
    num_unique_materials=('TIP_MATERIAL_KEY', lambda x: x.dropna().nunique()),
    avg_new_price_tip=('NEW_SHELF_PRICE','mean'),
    avg_used_price_tip=('USED_SHELF_PRICE','mean'),
    tip_material_record_count=('RECORD_COUNT','sum'),
    num_unique_library_titles=('TITLE', lambda x: x.dropna().nunique()),
    num_unique_library_isbns=('ISBN', lambda x: x.dropna().nunique())
).reset_index()

# 6) For each (CLUSTER_TYPE, HGN_CODE) group, list required columns per subject offering
# Also compute average enrollment within its cluster: interpreted as average SUBJECT_ENROLLMENT_NUMBER within same CLUSTER_TYPE; compute from agg_per_subject
cluster_avg = agg_per_subject.groupby(['CLUSTER_TYPE']).agg(
    avg_enroll_within_cluster=('total_enroll','mean')
).reset_index()

result = agg_per_subject.merge(cluster_avg, how='left', on='CLUSTER_TYPE')

# 7) Select and rename columns to match the question wording
result = result.rename(columns={
    'OFFER_DEPT_NAME': 'department_name',
    'SUBJECT_TITLE': 'course_title',
    'CLUSTER_TYPE': 'cluster_type',
    'HGN_CODE': 'course_level',
    'total_enroll': 'total_enrollments',
    'avg_new_price_tip': 'avg_new_price_tip_materials',
    'avg_used_price_tip': 'avg_used_price_tip_materials',
    'tip_material_record_count': 'total_tip_material_record_count',
    'num_unique_library_titles': 'unique_library_titles',
    'num_unique_library_isbns': 'unique_library_isbns',
    'num_unique_materials': 'unique_course_materials'
})

# 8) Final ordering
result = result[[
    'department_name', 'course_title', 'cluster_type', 'total_enrollments',
    'avg_enroll_within_cluster', 'course_level', 'unique_course_materials',
    'avg_new_price_tip_materials', 'avg_used_price_tip_materials',
    'total_tip_material_record_count', 'unique_library_titles', 'unique_library_isbns'
]].sort_values(['cluster_type','course_level','department_name','course_title'])

answer = result

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
