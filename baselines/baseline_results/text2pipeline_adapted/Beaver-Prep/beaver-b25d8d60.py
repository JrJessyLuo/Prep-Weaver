import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['INSTRUCTOR_NAME', 'LIBRARY_COURSE_INSTRUCTOR_KEY']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'LIBRARY_RESERVE_CATALOG_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'SUBJECT_ID', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['INSTRUCTOR_NAME', 'LIBRARY_COURSE_INSTRUCTOR_KEY']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['LIBRARY_RESERVE_CATALOG_KEY'] = tmp_0['LIBRARY_RESERVE_CATALOG_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['SUBJECT_ID'] = tmp_2['SUBJECT_ID'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'SUBJECT_ID', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['SUBJECT_ID', 'TERM_CODE', 'ACADEMIC_YEAR']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
tmp = prepared_table_1.merge(prepared_table_2, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')
# Enrich with subject academic year to compute average publication year
tmp2 = tmp.merge(prepared_table_4, on=['SUBJECT_ID','TERM_CODE'], how='left')
# Optional enrichment of material status label (not required for counts but harmless); keep key-based counts
tmp3 = tmp2.merge(prepared_table_3, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')
# Compute aggregates per instructor
agg = tmp3.groupby('INSTRUCTOR_NAME').agg(
    unique_courses=('SUBJECT_ID', 'nunique'),
    total_material_assignments=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    avg_publication_year=('ACADEMIC_YEAR', 'mean'),
    distinct_status=('LIBRARY_MATERIAL_STATUS_KEY', 'nunique')
).reset_index()
# Round/clean average publication year to a reasonable numeric (keep as float if mixed years)
agg['avg_publication_year'] = agg['avg_publication_year']
# Sort by number of unique courses descending
target = agg.sort_values(['unique_courses','INSTRUCTOR_NAME'], ascending=[False, True])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
