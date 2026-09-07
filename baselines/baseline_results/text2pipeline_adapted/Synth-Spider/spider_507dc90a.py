import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'IdClient', 'new_name': 'attribute'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['attribute'], 'value_vars': [1, 2, 3, 4, 5, 6], 'var_name': 'ClientID', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ClientID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'ClientID', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ClientID', 'Name']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'KH', 'new_name': 'ClientID'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ClientID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdOrder', 'ClientID']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'IdOrder', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IdOrder', 'amount']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'IdClient': 'attribute'})
    # Step 2: Stack
    tmp_1 = tmp_0.melt(id_vars=['attribute'], value_vars=[1, 2, 3, 4, 5, 6], var_name='ClientID', value_name='value')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ClientID'] = pd.to_numeric(tmp_2['ClientID'], errors='coerce').fillna(0).astype(int)
    # Step 4: Pivot
    tmp_3 = pd.pivot_table(tmp_2, index='ClientID', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['Name'] = tmp_4['Name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['ClientID', 'Name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'KH': 'ClientID'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ClientID'] = pd.to_numeric(tmp_1['ClientID'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IdOrder', 'ClientID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['IdOrder'] = tmp_0['IdOrder'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['amount'] = pd.to_numeric(tmp_1['amount'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IdOrder', 'amount']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
orders_with_clients = prepared_table_2.merge(prepared_table_1, on='ClientID', how='left')
# Count distinct orders per client using the orders header
order_counts = orders_with_clients.groupby(['ClientID','Name'], as_index=False).agg(n_orders=('IdOrder','nunique'))
# Ensure all clients appear even if they have no orders
all_clients = prepared_table_1[['ClientID','Name']]
result = all_clients.merge(order_counts, on=['ClientID','Name'], how='left')
result['n_orders'] = result['n_orders'].fillna(0).astype(int)
# Final projection: client name and number of orders
target = result[['Name','n_orders']].sort_values(['Name']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
