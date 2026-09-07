import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['library_reserve_catalog_key','CATALOG_YEAR','CATALOG_RECORD_CREATE_DATE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['LIBRARY_SUBJECT_OFFERED_KEY','term_code','OFFER_DEPT_NAME','NUM_ENROLLED_STUDENTS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_course_materials = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_material_status = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_catalog = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_subject_offered = prepared_table_4

# Assume the prepared tables are dataframes: prepared_course_materials (pcm), prepared_material_status (pms), prepared_catalog (pcat), prepared_subject_offered (pso)

# 1) Integrate tables
m1 = pcm.merge(pcat, left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key', how='inner')
m2 = m1.merge(pms, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')
full = m2.merge(pso, left_on=['LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE'], right_on=['LIBRARY_SUBJECT_OFFERED_KEY','term_code'], how='left')

# 2) Filter to books cataloged on or after 2000.
# Prefer CATALOG_YEAR when available; fall back to parsed year from CATALOG_RECORD_CREATE_DATE if CATALOG_YEAR is 0/NaN.
cat_year = pd.to_numeric(full['CATALOG_YEAR'], errors='coerce')
# Parse year from date like '19-APR-12' -> 2012 (assuming YY>=50 => 1900s else 2000s). Adjust as needed for actual format.
create_dt = pd.to_datetime(full['CATALOG_RECORD_CREATE_DATE'], errors='coerce', infer_datetime_format=True)
create_year = create_dt.dt.year

use_year = cat_year.where(cat_year.notna() & (cat_year > 0), create_year)
filtered = full[use_year >= 2000].copy()

# 3) Prepare aggregations: count of catalog items and total enrolled students per material status and department.
# Each row corresponds to a catalog item tied to a course offering; count distinct catalog items by key to avoid double-counting duplicates per join.
filtered['catalog_item'] = filtered['library_reserve_catalog_key']

# For student totals, sum NUM_ENROLLED_STUDENTS across associated offerings; convert to numeric safely.
filtered['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(filtered['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0)

# Detail grouping
detail = (
    filtered.groupby(['LIBRARY_MATERIAL_STATUS', 'OFFER_DEPT_NAME'], dropna=False)
    .agg(num_catalog_items=('catalog_item','nunique'), total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum'))
    .reset_index()
)

# Subtotals per status
status_sub = (
    filtered.groupby(['LIBRARY_MATERIAL_STATUS'], dropna=False)
    .agg(num_catalog_items=('catalog_item','nunique'), total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum'))
    .reset_index()
)
status_sub['OFFER_DEPT_NAME'] = 'Subtotal'

# Grand total
grand = pd.DataFrame({
    'LIBRARY_MATERIAL_STATUS': ['Grand Total'],
    'OFFER_DEPT_NAME': ['Grand Total'],
    'num_catalog_items': [filtered['catalog_item'].nunique()],
    'total_enrolled_students': [filtered['NUM_ENROLLED_STUDENTS'].sum()]
})

# Combine
result = pd.concat([detail, status_sub, grand], ignore_index=True)

# Final select/rename as needed for output
result = result.rename(columns={
    'LIBRARY_MATERIAL_STATUS': 'material_status',
    'OFFER_DEPT_NAME': 'department_name',
    'num_catalog_items': 'num_associated_catalog_items',
    'total_enrolled_students': 'total_enrolled_students'
})

# Optionally sort for presentation (not required by schema)
# result = result.sort_values(['material_status','department_name'])

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
