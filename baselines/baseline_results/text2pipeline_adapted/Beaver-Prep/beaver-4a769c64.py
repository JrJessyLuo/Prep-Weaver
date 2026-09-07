import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TERM_CODE', 'new_name': 'term_code'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'LIBRARY_MATERIAL_STATUS_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'term_code', 'SUBJECT_ID', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'LIBRARY_MATERIAL_STATUS', 'new_name': 'MATERIAL_STATUS_DESCRIPTION'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'MATERIAL_STATUS_DESCRIPTION', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'term_code', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_TERMS_KEY', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TERM_CODE', 'new_name': 'term_code'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_FULL_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SCHOOL_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SUBJECT_GROUPING_KEY', 'term_code', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_NAME', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TERM_CODE': 'term_code'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['LIBRARY_MATERIAL_STATUS_KEY'] = tmp_1['LIBRARY_MATERIAL_STATUS_KEY'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'term_code', 'SUBJECT_ID', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'LIBRARY_MATERIAL_STATUS': 'MATERIAL_STATUS_DESCRIPTION'})
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS_CODE', 'MATERIAL_STATUS_DESCRIPTION', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['term_code'] = tmp_0['term_code'].astype(str)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_TERMS_KEY', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'TERM_CODE': 'term_code'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['DEPARTMENT_CODE'] = tmp_1['DEPARTMENT_CODE'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['DEPARTMENT_NAME'] = tmp_2['DEPARTMENT_NAME'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['DEPARTMENT_FULL_NAME'] = tmp_3['DEPARTMENT_FULL_NAME'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['SCHOOL_NAME'] = tmp_4['SCHOOL_NAME'].astype(str)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['SUBJECT_GROUPING_KEY', 'term_code', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'DEPARTMENT_FULL_NAME', 'SCHOOL_NAME', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_8', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='LIBRARY_MATERIAL_STATUS_KEY').merge(prepared_table_3, how='left', on='term_code').merge(prepared_table_4[['term_code','DEPARTMENT_CODE','DEPARTMENT_NAME','DEPARTMENT_FULL_NAME','SCHOOL_NAME']].drop_duplicates(), how='left', on='term_code')
# Compute per library material status key/code and term code/description:
# - total number of courses: approximate by distinct SUBJECT_ID within the group
# - total number of materials: distinct LIBRARY_RESERVE_CATALOG_KEY within the group
# - occurrences in departments: distinct DEPARTMENT_CODE within the group
# - occurrences in school: distinct SCHOOL_NAME within the group
# - total number of instructors: approximate by distinct LIBRARY_COURSE_INSTRUCTOR_KEY within the group
agg = integrated.groupby(['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS_CODE','MATERIAL_STATUS_DESCRIPTION','term_code','TERM_DESCRIPTION'], dropna=False).agg(
    total_courses=('SUBJECT_ID', lambda s: s.nunique(dropna=True)),
    total_materials=('LIBRARY_RESERVE_CATALOG_KEY', lambda s: s.nunique(dropna=True)),
    occurrences_in_departments=('DEPARTMENT_CODE', lambda s: s.nunique(dropna=True)),
    occurrences_in_school=('SCHOOL_NAME', lambda s: s.nunique(dropna=True)),
    total_instructors=('LIBRARY_COURSE_INSTRUCTOR_KEY', lambda s: s.nunique(dropna=True))
).reset_index()
# Final projection and sensible ordering
cols = ['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS_CODE','MATERIAL_STATUS_DESCRIPTION','term_code','TERM_DESCRIPTION','total_courses','total_materials','occurrences_in_departments','occurrences_in_school','total_instructors']
target = agg[cols].sort_values(['LIBRARY_MATERIAL_STATUS_KEY','term_code'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
