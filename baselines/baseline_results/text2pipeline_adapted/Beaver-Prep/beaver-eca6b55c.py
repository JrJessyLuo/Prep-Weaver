import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'LIBRARY_RESERVE_CATALOG_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    # trim and collapse internal whitespace, preserve original case\n    s = s.strip()\n    return " ".join(s.split())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NAME', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    s = s.strip()\n    return " ".join(s.split())'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'library_reserve_catalog_key', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CATALOG_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['library_reserve_catalog_key', 'CATALOG_YEAR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_numeric(tmp_0['LIBRARY_RESERVE_CATALOG_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['LIBRARY_COURSE_INSTRUCTOR_KEY'] = tmp_1['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['SUBJECT_ID'] = tmp_2['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    # trim and collapse internal whitespace, preserve original case\n    s = s.strip()\n    return " ".join(s.split())', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'] = tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    s = s.strip()\n    return " ".join(s.split())', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['COURSE_NAME'] = tmp_1['COURSE_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['library_reserve_catalog_key'] = pd.to_numeric(tmp_0['library_reserve_catalog_key'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['CATALOG_YEAR'] = pd.to_numeric(tmp_1['CATALOG_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['library_reserve_catalog_key', 'CATALOG_YEAR']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_MATERIAL_STATUS_KEY'] = tmp_0['LIBRARY_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='LIBRARY_COURSE_INSTRUCTOR_KEY')
integrated = integrated.merge(prepared_table_3, how='left', left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key')
integrated = integrated.merge(prepared_table_4, how='left', on='LIBRARY_MATERIAL_STATUS_KEY')

aggr = (
    integrated.groupby('COURSE_NAME', dropna=False)
    .agg(
        total_materials=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
        min_publication_year=('CATALOG_YEAR', 'min'),
        max_publication_year=('CATALOG_YEAR', 'max'),
        total_materials_status=('LIBRARY_MATERIAL_STATUS_KEY', 'count')
    )
    .reset_index()
)

target = aggr[['COURSE_NAME', 'total_materials', 'min_publication_year', 'max_publication_year', 'total_materials_status']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
