import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'IAP_SUBJECT_SESSION_KEY', 'new_name': 'IAP_SUBJECT_SESSION_KEY'}, {'old_name': 'IAP_SUBJECT_SPONSOR_KEY', 'new_name': 'IAP_SUBJECT_SPONSOR_KEY'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SPONSOR_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SESSION_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_PERSON_KEY']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SPONSOR_NAME', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SPONSOR_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SPONSOR_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'iap_subject_session_key', 'new_name': 'IAP_SUBJECT_SESSION_KEY'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SESSION_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HAS_SESSION_INFO', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SESSION_KEY']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'IAP_SUBJECT_SESSION_KEY': 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_SPONSOR_KEY': 'IAP_SUBJECT_SPONSOR_KEY'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['IAP_SUBJECT_SPONSOR_KEY'] = tmp_1['IAP_SUBJECT_SPONSOR_KEY'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['IAP_SUBJECT_SESSION_KEY'] = tmp_2['IAP_SUBJECT_SESSION_KEY'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_PERSON_KEY']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SPONSOR_NAME'] = tmp_0['SPONSOR_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['IAP_SUBJECT_SPONSOR_KEY'] = tmp_1['IAP_SUBJECT_SPONSOR_KEY'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['SPONSOR_NAME'] = tmp_2['SPONSOR_NAME'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'iap_subject_session_key': 'IAP_SUBJECT_SESSION_KEY'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['IAP_SUBJECT_SESSION_KEY'] = tmp_1['IAP_SUBJECT_SESSION_KEY'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['HAS_SESSION_INFO'] = tmp_2['HAS_SESSION_INFO'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IAP_SUBJECT_SESSION_KEY']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='IAP_SUBJECT_SPONSOR_KEY', how='left').merge(prepared_table_3, on='IAP_SUBJECT_SESSION_KEY', how='left')
agg = integrated.groupby(['IAP_SUBJECT_SPONSOR_KEY','SPONSOR_NAME']).agg(num_iap_sessions=('IAP_SUBJECT_SESSION_KEY','nunique'), num_unique_subjects=('IAP_SUBJECT_PERSON_KEY','nunique')).reset_index()
target = agg[['SPONSOR_NAME','num_iap_sessions','num_unique_subjects']].sort_values(['SPONSOR_NAME']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
