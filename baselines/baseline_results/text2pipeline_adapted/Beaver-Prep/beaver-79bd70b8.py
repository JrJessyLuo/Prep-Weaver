import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'MAX_ENROLLMENT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MULTIPLE_SESSION', 'func': 'def transform(s):\n    if s is None:\n        return None\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_CANCELLED', 'func': 'def transform(s):\n    if s is None:\n        return None\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'MAX_ENROLLMENT', 'FEE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SPONSOR_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SPONSOR_TYPE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'HAS_SESSION_INFO', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()\n'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'iap_subject_session_key', 'new_name': 'IAP_SUBJECT_SESSION_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SESSION_KEY', 'HAS_SESSION_INFO']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MAX_ENROLLMENT'] = pd.to_numeric(tmp_0['MAX_ENROLLMENT'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['FEE'] = pd.to_numeric(tmp_1['FEE'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['IS_MULTIPLE_SESSION'] = tmp_2['IS_MULTIPLE_SESSION'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['IS_CANCELLED'] = tmp_3['IS_CANCELLED'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'MAX_ENROLLMENT', 'FEE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SPONSOR_NAME'] = tmp_0['SPONSOR_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SPONSOR_TYPE'] = tmp_1['SPONSOR_TYPE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['HAS_SESSION_INFO'] = tmp_0['HAS_SESSION_INFO'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'iap_subject_session_key': 'IAP_SUBJECT_SESSION_KEY'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IAP_SUBJECT_SESSION_KEY', 'HAS_SESSION_INFO']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_3, how='left', on='IAP_SUBJECT_SESSION_KEY')\
    .merge(prepared_table_2, how='left', on='IAP_SUBJECT_SPONSOR_KEY')
# Compute per-sponsor aggregates
agg = integrated.groupby(['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], dropna=False).agg(
    number_of_sessions=('IAP_SUBJECT_SESSION_KEY', 'nunique'),
    total_enrollment=('MAX_ENROLLMENT', 'sum'),
    min_fee=('FEE', 'min'),
    max_fee=('FEE', 'max'),
    sessions_with_info=('HAS_SESSION_INFO', lambda s: s.fillna('N').str.upper().eq('Y').sum()),
    sessions_without_info=('HAS_SESSION_INFO', lambda s: s.fillna('N').str.upper().ne('Y').sum())
).reset_index()
# Final projection and naming per question
target = agg.rename(columns={
    'SPONSOR_NAME': 'sponsor_name',
    'number_of_sessions': 'number_of_sessions_held',
    'total_enrollment': 'total_number_of_enrollment',
    'min_fee': 'minimum_fee',
    'max_fee': 'maximum_fee',
    'sessions_with_info': 'number_of_sessions_with_info',
    'sessions_without_info': 'number_of_sessions_without_info'
})[['sponsor_name', 'number_of_sessions_held', 'total_number_of_enrollment', 'minimum_fee', 'maximum_fee', 'number_of_sessions_with_info', 'number_of_sessions_without_info']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
