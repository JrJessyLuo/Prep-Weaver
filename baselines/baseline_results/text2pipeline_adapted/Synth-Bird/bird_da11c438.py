import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['client_id', 'district_id', 'gender', 'birth_date']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['district_id'], 'value_vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], 'var_name': 'district_ordinal', 'value_name': 'district_name'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'district_id', 'new_name': 'region_code'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'district_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'district_ordinal', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['region_code', 'district_ordinal', 'district_name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'disp_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'client_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'lx', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['disp_id', 'client_id', 'account_id', 'lx']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'loan_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'account_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'duration', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'payments', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['loan_id', 'account_id', 'date', 'amount', 'duration', 'payments', 'status']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['client_id'] = pd.to_numeric(tmp_0['client_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['district_id'] = pd.to_numeric(tmp_1['district_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['client_id', 'district_id', 'gender', 'birth_date']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_5', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['district_id'], value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], var_name='district_ordinal', value_name='district_name')
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'district_id': 'region_code'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['district_name'] = tmp_2['district_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['district_ordinal'] = pd.to_numeric(tmp_3['district_ordinal'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['region_code', 'district_ordinal', 'district_name']].copy()
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
    tmp_3['lx'] = tmp_3['lx'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['disp_id', 'client_id', 'account_id', 'lx']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['loan_id'] = pd.to_numeric(tmp_0['loan_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['account_id'] = pd.to_numeric(tmp_1['account_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['amount'] = pd.to_numeric(tmp_2['amount'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['duration'] = pd.to_numeric(tmp_3['duration'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['payments'] = pd.to_numeric(tmp_4['payments'], errors='coerce').astype(float)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['date'] = pd.to_datetime(tmp_5['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_6['status'] = tmp_6['status'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['loan_id', 'account_id', 'date', 'amount', 'duration', 'payments', 'status']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_3, on='client_id', how='inner').merge(prepared_table_4, on='account_id', how='inner')
# Bring in district names by matching client district_id (ordinal) to table_2 district_ordinal
integrated = integrated.merge(prepared_table_2, left_on='district_id', right_on='district_ordinal', how='left')
# Interpret eligibility for loans: accounts with a loan whose status is 'A' (accepted/paid properly) or generally active/good standing.
# We'll treat status 'A' as eligible primarily; if there are no 'A', broaden to include 'B' as potentially eligible.
eligible = integrated[integrated['status'].str.upper() == 'A']
if eligible.empty:
    eligible = integrated[integrated['status'].str.upper().isin(['A','B'])]
# Filter for district name Tabor, case-insensitive, robust to whitespace
mask_tabor = eligible['district_name'].astype(str).str.strip().str.lower() == 'tabor'
subset = eligible[mask_tabor]
if subset.empty:
    # fallback: contains match in case of minor variations
    mask_tabor_ci = eligible['district_name'].astype(str).str.contains('tabor', case=False, na=False)
    subset = eligible[mask_tabor_ci]
# Keep unique accounts whose district is Tabor and eligible
result = subset[['account_id']].drop_duplicates().sort_values('account_id')
target = result.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
