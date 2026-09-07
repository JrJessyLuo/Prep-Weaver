import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'loan_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'zh_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['loan_id', 'zh_id', 'date', 'duration', 'payments', 'flz']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'disp_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'type', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['disp_id', 'client_id', 'account_id', 'type']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'gender', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    s = s.strip().upper()\n    return s[:1] if s else ''"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'birth_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'gender', 'birth_date', 'district_id']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['district_id', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['loan_id'] = pd.to_numeric(tmp_0['loan_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['zh_id'] = pd.to_numeric(tmp_1['zh_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date'] = pd.to_datetime(tmp_2['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['loan_id', 'zh_id', 'date', 'duration', 'payments', 'flz']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['disp_id'] = pd.to_numeric(tmp_0['disp_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['client_id'] = pd.to_numeric(tmp_1['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['account_id'] = pd.to_numeric(tmp_2['account_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['type'] = tmp_3['type'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['disp_id', 'client_id', 'account_id', 'type']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    s = s.strip().upper()\n    return s[:1] if s else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['gender'] = tmp_0['gender'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['birth_date'] = pd.to_datetime(tmp_1['birth_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['client_id'] = pd.to_numeric(tmp_2['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['district_id'] = pd.to_numeric(tmp_3['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['client_id', 'gender', 'birth_date', 'district_id']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['district_id', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11', 'A12', 'A13', 'A14', 'A15', 'A16']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', left_on='zh_id', right_on='account_id').merge(prepared_table_3, how='inner', on='client_id')
# Filter for the loan approved on 1994/8/25 (1994-08-25)
filtered = integrated[integrated['date'] == pd.to_datetime('1994-08-25')]
# If no exact match due to potential string/datetime normalization, try robust match on string form as fallback
if filtered.empty:
    as_str = integrated['date'].astype(str).str[:10]
    filtered = integrated[as_str.str.lower() == '1994-08-25']
# Select distinct district_ids for that account/loan date
result = filtered[['zh_id','district_id']].drop_duplicates()
# If multiple clients tied to the same account yield multiple districts (unlikely), keep unique rows
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
