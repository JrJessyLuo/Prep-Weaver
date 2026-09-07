import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_CATEGORY_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SPONSOR_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SPONSOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IAP_SUBJECT_SESSION_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SESSION_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SPONSOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'iap_subject_session_key', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SESSION_TITLE', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SESSION_LOCATION', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SESSION_START_TIME', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SESSION_END_TIME', 'func': "def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['iap_subject_session_key', 'SESSION_TITLE', 'SESSION_START_TIME', 'SESSION_END_TIME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['IAP_SUBJECT_CATEGORY_KEY'] = tmp_1['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['IAP_SUBJECT_SPONSOR_KEY'] = tmp_2['IAP_SUBJECT_SPONSOR_KEY'].astype(str)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['IAP_SUBJECT_SPONSOR_KEY'] = tmp_3['IAP_SUBJECT_SPONSOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['IAP_SUBJECT_SESSION_KEY'] = tmp_4['IAP_SUBJECT_SESSION_KEY'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_5['IAP_SUBJECT_SESSION_KEY'] = tmp_5['IAP_SUBJECT_SESSION_KEY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_SPONSOR_KEY'] = tmp_0['IAP_SUBJECT_SPONSOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['iap_subject_session_key'] = tmp_0['iap_subject_session_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SESSION_TITLE'] = tmp_1['SESSION_TITLE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['SESSION_LOCATION'] = tmp_2['SESSION_LOCATION'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['SESSION_START_TIME'] = tmp_3['SESSION_START_TIME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec("def transform(s):\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()", globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['SESSION_END_TIME'] = tmp_4['SESSION_END_TIME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['iap_subject_session_key', 'SESSION_TITLE', 'SESSION_START_TIME', 'SESSION_END_TIME']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='IAP_SUBJECT_CATEGORY_KEY').merge(prepared_table_3, how='left', on='IAP_SUBJECT_SPONSOR_KEY').merge(prepared_table_4, how='left', left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key')
# Count total sessions per subject by counting session rows per subject-session key
session_counts = integrated.groupby(['IAP_SUBJECT_SESSION_KEY'], dropna=False).size().reset_index(name='TOTAL_SESSIONS')
integrated = integrated.merge(session_counts, how='left', on='IAP_SUBJECT_SESSION_KEY')
# Final projection of requested fields
cols = ['ACTIVITY_TITLE', 'IAP_CATEGORY_NAME', 'SESSION_TITLE', 'SESSION_START_TIME', 'SESSION_END_TIME', 'SPONSOR_NAME', 'TOTAL_SESSIONS']
target = integrated[cols]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
