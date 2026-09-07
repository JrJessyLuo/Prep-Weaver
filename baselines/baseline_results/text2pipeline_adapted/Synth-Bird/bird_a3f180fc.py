import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'disp_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'account_id', 'attribute', 'value']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'gender', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'birth_date', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'district_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
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
    tmp_3['attribute'] = tmp_3['attribute'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['value'] = tmp_4['value'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['client_id', 'account_id', 'attribute', 'value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['client_id'] = pd.to_numeric(tmp_0['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['district_id'] = pd.to_numeric(tmp_1['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['gender'] = tmp_2['gender'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['birth_date'] = tmp_3['birth_date'].astype(str)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['client_id', 'district_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
disp = prepared_table_1.copy()
# Keep only disposition type rows
mask_type = disp['attribute'].str.upper() == 'TYPE'
disp_type = disp.loc[mask_type, ['client_id', 'account_id', 'value']].rename(columns={'value': 'disp_type'})
# Determine clients who can only have the right to issue permanent orders or apply for loans.
# Interpret as clients whose disposition type set is a subset of {DISPONENT} (issue permanent orders) or {OWNER} (apply for loans), and who do not have any other disposition type values.
# Map allowed set
allowed = set(['OWNER', 'DISPONENT'])
# Aggregate types per client
types_per_client = disp_type.groupby('client_id')['disp_type'].apply(lambda s: set(s.dropna().astype(str).str.upper())).reset_index()
# Keep clients whose types are non-empty and subset of allowed, and not a mix of both ("only" one right)
# To match the phrasing, accept clients whose set is exactly {'OWNER'} or exactly {'DISPONENT'}
only_mask = types_per_client['disp_type'].apply(lambda st: len(st) > 0 and (st == {'OWNER'} or st == {'DISPONENT'}))
eligible_clients = types_per_client.loc[only_mask, ['client_id']]
# Join to clients to get district
out = eligible_clients.merge(prepared_table_2, on='client_id', how='inner')
# Final projection: ID and district
target = out[['client_id', 'district_id']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
