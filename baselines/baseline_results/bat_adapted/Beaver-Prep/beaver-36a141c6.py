import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['subject_id','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY','RECORD_COUNT']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['TIP_MATERIAL_KEY','ISBN','NEW_SHELF_PRICE','USED_SHELF_PRICE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['SUBJECT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']].copy()
    df['SUBJECT_CODE'] = df['SUBJECT_CODE'].astype(str).str.strip()
    df['DEPARTMENT_NAME'] = df['DEPARTMENT_NAME'].astype(str).str.strip()
    df['SCHOOL_NAME'] = df['SCHOOL_NAME'].astype(str).str.strip()
    target = df.drop_duplicates().reset_index(drop=True)[['SUBJECT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_material_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_materials = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_material_status = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
prepared_subject_org = prepared_table_4

# Start from prepared tables
assign = prepared_material_assignments.copy()
mat = prepared_materials.copy()
status = prepared_material_status.copy()
org = prepared_subject_org.copy()

# Join assignments -> materials (for pricing)
assign_mat = assign.merge(mat, how='left', on='TIP_MATERIAL_KEY')

# Join assignments -> status (for status description/code)
assign_mat_stat = assign_mat.merge(status, how='left', left_on='TIP_MATERIAL_STATUS_KEY', right_on='tip_material_status_key')

# Join to org via subject/subject_code (assumes compatible coding; coerce to string/strip for robustness)
assign_mat_stat['subject_id'] = assign_mat_stat['subject_id'].astype(str).str.strip()
org['SUBJECT_CODE'] = org['SUBJECT_CODE'].astype(str).str.strip()
joined = assign_mat_stat.merge(org, how='left', left_on='subject_id', right_on='SUBJECT_CODE')

# Define helper columns
# Treat material records as those with a non-null/non-empty TIP_MATERIAL_KEY excluding explicit 'Course has no materials' markers
invalid_keys = set([None, float('nan')])
joined['has_material'] = (~joined['TIP_MATERIAL_KEY'].astype(str).str.contains('Course has no materials', case=False, na=False)) & (joined['TIP_MATERIAL_KEY'].astype(str).str.strip() != '')

# Numeric cast for prices
for c in ['NEW_SHELF_PRICE','USED_SHELF_PRICE']:
    joined[c] = pd.to_numeric(joined[c], errors='coerce')

# Group by department and school
grp_cols = ['DEPARTMENT_NAME','SCHOOL_NAME']

# Unique material count: count distinct TIP_MATERIAL_KEY among rows with has_material
def agg_frame(df):
    df_mat = df[df['has_material']]
    out = {
        'unique_course_materials': df_mat['TIP_MATERIAL_KEY'].nunique(dropna=True),
        'number_of_courses': df['subject_id'].nunique(dropna=True),
        'avg_new_shelf_price': df_mat['NEW_SHELF_PRICE'].mean(skipna=True),
        'avg_used_shelf_price': df_mat['USED_SHELF_PRICE'].mean(skipna=True),
        'total_material_records': int(df_mat.shape[0]),
        'distinct_material_statuses': df['TIP_MATERIAL_STATUS_KEY'].nunique(dropna=True)
    }
    return pd.Series(out)

by_org = joined.groupby(grp_cols, dropna=False).apply(agg_frame).reset_index()

# Grand total across all schools and departments: null dept/school
grand = agg_frame(joined).to_frame().T
grand['DEPARTMENT_NAME'] = pd.NA
grand['SCHOOL_NAME'] = pd.NA

# Reorder columns
cols = ['DEPARTMENT_NAME','SCHOOL_NAME','unique_course_materials','number_of_courses','avg_new_shelf_price','avg_used_shelf_price','total_material_records','distinct_material_statuses']
result = pd.concat([by_org[cols], grand[cols]], ignore_index=True)

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
