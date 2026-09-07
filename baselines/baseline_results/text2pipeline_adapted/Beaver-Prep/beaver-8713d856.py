import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'moira_list_member', 'func': 'def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MOIRA_LIST_MEMBER_MIT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LAST_UPDATE_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'LAST_UPDATE_DATE', 'COUNTER', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'MOIRA_LIST_OWNER_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OWNER_TYPE', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'WAREHOUSE_LOAD_DATE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['moira_list_member'] = tmp_0['moira_list_member'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MOIRA_LIST_MEMBER_MIT_ID'] = tmp_1['MOIRA_LIST_MEMBER_MIT_ID'].astype(str)
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['LAST_UPDATE_DATE'] = pd.to_datetime(tmp_2['LAST_UPDATE_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_3['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME', 'MOIRA_LIST_MEMBER_MIT_ID', 'LAST_UPDATE_DATE', 'COUNTER', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['MOIRA_LIST_OWNER_KEY'] = tmp_0['MOIRA_LIST_OWNER_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['OWNER'] = tmp_1['OWNER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['OWNER_TYPE'] = tmp_2['OWNER_TYPE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_3['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['WAREHOUSE_LOAD_DATE'] = tmp_4['WAREHOUSE_LOAD_DATE'].astype(str)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['MOIRA_LIST_OWNER_KEY', 'OWNER', 'OWNER_TYPE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='MOIRA_LIST_OWNER_KEY', how='inner')

# Normalize owner key for robust matching
key_norm = 'list69.377-keeper-xenon'.strip().lower()

filtered = integrated[integrated['MOIRA_LIST_OWNER_KEY'].astype(str).str.strip().str.lower() == key_norm]

# Fallback: broader case-insensitive contains over plausible key/owner columns if strict match yields no rows
if filtered.empty:
    mask = (
        integrated['MOIRA_LIST_OWNER_KEY'].astype(str).str.strip().str.lower().str.contains('69.377-keeper-xenon', na=False)
        | integrated['OWNER'].astype(str).str.strip().str.lower().str.contains('69.377-keeper-xenon', na=False)
    )
    filtered = integrated[mask]

# Aggregate: owner name, total distinct mailing lists, and total members (rows)
result = (
    filtered.groupby(['MOIRA_LIST_OWNER_KEY', 'OWNER'], dropna=False)
    .agg(
        total_mailing_lists=('MOIRA_LIST_KEY', 'nunique'),
        total_members=('moira_list_member', 'size')
    )
    .reset_index()
)

# Select final columns
target = result[['OWNER', 'total_mailing_lists', 'total_members']]

# If still empty, fall back to the owner record with zero counts (ensuring non-empty target)
if target.empty:
    owners = prepared_table_2[prepared_table_2['MOIRA_LIST_OWNER_KEY'].astype(str).str.strip().str.lower() == key_norm]
    if owners.empty:
        owners = prepared_table_2[prepared_table_2['MOIRA_LIST_OWNER_KEY'].astype(str).str.strip().str.lower().str.contains('69.377-keeper-xenon', na=False)]
    if not owners.empty:
        owner_name = owners.iloc[0]['OWNER']
        target = owners.iloc[[0]][['OWNER']].copy()
        target['total_mailing_lists'] = 0
        target['total_members'] = 0

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
