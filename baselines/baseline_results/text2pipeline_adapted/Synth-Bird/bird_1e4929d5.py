import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'date_received', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'amount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'source', 'func': 'def transform(s):\n    # Trim whitespace but preserve original case\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_member', 'new_name': 'member_record_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['income_id', 'date_received', 'amount', 'source', 'notes', 'member_record_id']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['member_id'], 'value_vars': ['rec1x5zBFIqoOuPW8', 'rec280Sk7o31iG0Tx', 'rec28ORZgcm1dtqBZ', 'rec2a03QXbFQAUZ7X', 'rec3pH4DxMcWHMRB7', 'rec4BLdZHS2Blfp4v', 'rec4O9rmGnLx3j8vt', 'rec75vvFxgYtHmqxY', 'recD078PnS3x2doBe', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recJMazpPVexyFYTc', 'recL4aEZBZoPk9NYx', 'recL94zpn6Xh6kQii', 'recP6DJPyi5donvXL', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recTjHY5xXhvkCdVT', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'recWh2lJVOT6HjChK', 'recZ4PkGERzl9ziHO', 'recZN8afUWlE5fZHG', 'reccSUPwy30AeZLEb', 'reccW7q1KkhSKZsea', 'recf4UKTfipCzgcSA', 'recjHj4BS5A541n9v', 'reco0mr8dXTgs5wWA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'recttfySfQnYb68u3', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS'], 'var_name': 'member_record_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'member_record_id', 'columns': 'member_id', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_record_id', 'first_name', 'last_name', 'email']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['date_received'] = pd.to_datetime(tmp_0['date_received'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['amount'] = pd.to_numeric(tmp_1['amount'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim whitespace but preserve original case\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['source'] = tmp_2['source'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'link_to_member': 'member_record_id'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['income_id', 'date_received', 'amount', 'source', 'notes', 'member_record_id']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['member_id'], value_vars=['rec1x5zBFIqoOuPW8', 'rec280Sk7o31iG0Tx', 'rec28ORZgcm1dtqBZ', 'rec2a03QXbFQAUZ7X', 'rec3pH4DxMcWHMRB7', 'rec4BLdZHS2Blfp4v', 'rec4O9rmGnLx3j8vt', 'rec75vvFxgYtHmqxY', 'recD078PnS3x2doBe', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recJMazpPVexyFYTc', 'recL4aEZBZoPk9NYx', 'recL94zpn6Xh6kQii', 'recP6DJPyi5donvXL', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recTjHY5xXhvkCdVT', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'recWh2lJVOT6HjChK', 'recZ4PkGERzl9ziHO', 'recZN8afUWlE5fZHG', 'reccSUPwy30AeZLEb', 'reccW7q1KkhSKZsea', 'recf4UKTfipCzgcSA', 'recjHj4BS5A541n9v', 'reco0mr8dXTgs5wWA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'recttfySfQnYb68u3', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS'], var_name='member_record_id', value_name='value')
    # Step 2: Pivot
    tmp_1 = pd.pivot_table(tmp_0, index='member_record_id', columns='member_id', values='value', aggfunc='first').reset_index()
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['first_name'] = tmp_2['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['last_name'] = tmp_3['last_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['member_record_id', 'first_name', 'last_name', 'email']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
dues = prepared_table_1.copy()
# Keep only dues-related income after integration prep
# Case-insensitive contains 'dues' to be robust
mask_dues = dues['source'].astype(str).str.contains('dues', case=False, na=False)
dues = dues[mask_dues]
# Join to member directory on member_record_id
integrated = dues.merge(prepared_table_2, how='left', on='member_record_id')
# Find the earliest payment date
integrated_sorted = integrated.sort_values(['date_received', 'income_id'], ascending=[True, True])
first_payment = integrated_sorted.head(1)
# Build full name; fallback to available parts
full_name = (first_payment['first_name'].fillna('') + ' ' + first_payment['last_name'].fillna('')).str.strip()
first_payment = first_payment.assign(full_name=full_name)
# Final projection
target = first_payment[['full_name']].rename(columns={'full_name': 'Full Name'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
