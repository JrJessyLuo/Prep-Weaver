import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'district_number', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'value', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'district_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'district_number', 'new_name': 'metric_code'}, {'old_name': 'value', 'new_name': 'metric_value'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['district_id', 'metric_code', 'metric_value']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'frequency', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['account_id', 'district_id', 'date']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'disp_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'type', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'type', 'new_name': 'role'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['disp_id', 'client_id', 'account_id', 'role']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'gender', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'gender', 'district_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['district_number'] = pd.to_numeric(tmp_0['district_number'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['value'] = pd.to_numeric(tmp_1['value'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['district_id'] = tmp_2['district_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'district_number': 'metric_code', 'value': 'metric_value'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['district_id', 'metric_code', 'metric_value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['account_id'] = pd.to_numeric(tmp_0['account_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['district_id'] = pd.to_numeric(tmp_1['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['date'] = pd.to_datetime(tmp_2['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['frequency'] = tmp_3['frequency'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['account_id', 'district_id', 'date']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
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
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'type': 'role'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['disp_id', 'client_id', 'account_id', 'role']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
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
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['gender'] = tmp_2['gender'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['client_id', 'gender', 'district_id']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
tmp = prepared_table_2.merge(prepared_table_1, how='left', left_on='district_id', right_on='metric_code')
# Identify districts with average salary > 10000. We don't know the exact metric_code for average salary; retain rows whose metric_value > 10000 across any metric_code as broad inclusion.
sal_districts = tmp[tmp['metric_value'] > 10000][['account_id']].drop_duplicates()
# Join accounts to dispositions and clients
acc_disp = prepared_table_3.merge(prepared_table_2, how='inner', on='account_id')
acc_disp_clients = acc_disp.merge(prepared_table_4, how='inner', on='client_id')
# Keep only accounts that are in districts over the salary threshold and roles indicating ownership
acc_disp_clients = acc_disp_clients.merge(sal_districts, how='inner', on='account_id')
owners = acc_disp_clients[acc_disp_clients['role'].str.upper() == 'OWNER']
# Compute percentage of women among these clients
if len(owners) == 0:
    target = acc_disp_clients.assign(percentage_women=None).head(0)
else:
    total = len(owners)
    women = (owners['gender'].str.upper() == 'F').sum()
    percentage = 100.0 * women / total if total > 0 else None
    target = owners.assign(percentage_women=percentage)[['percentage_women']].head(1)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
