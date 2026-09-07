import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'LIBRARY_RESERVE_CATALOG_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'TERM_CODE', 'new_name': 'term_code'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'term_code']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_MATERIAL_STATUS_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'library_reserve_catalog_key', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CATALOG_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['library_reserve_catalog_key', 'CATALOG_YEAR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}]]

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
    tmp_1['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_1['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'TERM_CODE': 'term_code'})
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['term_code'] = tmp_3['term_code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'term_code']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_MATERIAL_STATUS_KEY'] = tmp_0['LIBRARY_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['LIBRARY_MATERIAL_STATUS_CODE'] = tmp_1['LIBRARY_MATERIAL_STATUS_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

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
    tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['term_code'] = tmp_1['term_code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_2['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
_frames = []
if isinstance(prepared_table_1, pd.DataFrame) and not prepared_table_1.empty:
    _tmp = prepared_table_1.copy()
    _tmp['__prepared_table__'] = 'prepared_table_1'
    _frames.append(_tmp)
if isinstance(prepared_table_2, pd.DataFrame) and not prepared_table_2.empty:
    _tmp = prepared_table_2.copy()
    _tmp['__prepared_table__'] = 'prepared_table_2'
    _frames.append(_tmp)
if isinstance(prepared_table_3, pd.DataFrame) and not prepared_table_3.empty:
    _tmp = prepared_table_3.copy()
    _tmp['__prepared_table__'] = 'prepared_table_3'
    _frames.append(_tmp)
if isinstance(prepared_table_4, pd.DataFrame) and not prepared_table_4.empty:
    _tmp = prepared_table_4.copy()
    _tmp['__prepared_table__'] = 'prepared_table_4'
    _frames.append(_tmp)
target = pd.concat(_frames, ignore_index=True, sort=False) if _frames else pd.DataFrame()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
