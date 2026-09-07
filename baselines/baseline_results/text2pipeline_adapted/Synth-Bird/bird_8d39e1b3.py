import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['event_id', 'event_name']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'link_to_member', 'target_columns': ['member_id_list'], 'func': "def transform(s):\n    if s is None:\n        return [None]\n    parts = [p.strip() for p in str(s).split(',') if p is not None]\n    # Keep as a single-cell list for Explode\n    return [parts]"}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'member_id_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'member_id_list', 'new_name': 'member_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['link_to_event', 'member_id']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'member_id', 'new_name': 'attribute'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['attribute'], 'value_vars': ['rec1x5zBFIqoOuPW8', 'rec280Sk7o31iG0Tx', 'rec28ORZgcm1dtqBZ', 'rec2a03QXbFQAUZ7X', 'rec3pH4DxMcWHMRB7', 'rec4BLdZHS2Blfp4v', 'rec4O9rmGnLx3j8vt', 'rec75vvFxgYtHmqxY', 'recD078PnS3x2doBe', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recJMazpPVexyFYTc', 'recL4aEZBZoPk9NYx', 'recL94zpn6Xh6kQii', 'recP6DJPyi5donvXL', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recTjHY5xXhvkCdVT', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'recWh2lJVOT6HjChK', 'recZ4PkGERzl9ziHO', 'recZN8afUWlE5fZHG', 'reccSUPwy30AeZLEb', 'reccW7q1KkhSKZsea', 'recf4UKTfipCzgcSA', 'recjHj4BS5A541n9v', 'reco0mr8dXTgs5wWA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'recttfySfQnYb68u3', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS'], 'var_name': 'member_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'member_id', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'first_name', 'last_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['event_id', 'event_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    if s is None:\n        return [None]\n    parts = [p.strip() for p in str(s).split(',') if p is not None]\n    # Keep as a single-cell list for Explode\n    return [parts]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['link_to_member'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['member_id_list'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: Explode
    tmp_1 = tmp_0.explode('member_id_list')
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'member_id_list': 'member_id'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['link_to_event', 'member_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'member_id': 'attribute'})
    # Step 2: Stack
    tmp_1 = tmp_0.melt(id_vars=['attribute'], value_vars=['rec1x5zBFIqoOuPW8', 'rec280Sk7o31iG0Tx', 'rec28ORZgcm1dtqBZ', 'rec2a03QXbFQAUZ7X', 'rec3pH4DxMcWHMRB7', 'rec4BLdZHS2Blfp4v', 'rec4O9rmGnLx3j8vt', 'rec75vvFxgYtHmqxY', 'recD078PnS3x2doBe', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recJMazpPVexyFYTc', 'recL4aEZBZoPk9NYx', 'recL94zpn6Xh6kQii', 'recP6DJPyi5donvXL', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recTjHY5xXhvkCdVT', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'recWh2lJVOT6HjChK', 'recZ4PkGERzl9ziHO', 'recZN8afUWlE5fZHG', 'reccSUPwy30AeZLEb', 'reccW7q1KkhSKZsea', 'recf4UKTfipCzgcSA', 'recjHj4BS5A541n9v', 'reco0mr8dXTgs5wWA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'recttfySfQnYb68u3', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS'], var_name='member_id', value_name='value')
    # Step 3: Pivot
    tmp_2 = pd.pivot_table(tmp_1, index='member_id', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['first_name'] = tmp_3['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['last_name'] = tmp_4['last_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['member_id', 'first_name', 'last_name']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
att = prepared_table_2
# Join attendance to member directory to get member names
att_members = att.merge(prepared_table_3, how='left', on='member_id')
# Filter for Maya Mclean with robust, case-insensitive matching
mask = (
    att_members['first_name'].fillna('').str.strip().str.lower().eq('maya') &
    att_members['last_name'].fillna('').str.strip().str.lower().eq('mclean')
)
maya_att = att_members[mask]
# If no exact rows, relax to any member with first name Maya
if maya_att.empty:
    mask_relaxed = att_members['first_name'].fillna('').str.strip().str.lower().eq('maya')
    maya_att = att_members[mask_relaxed]
# Join to events to get event names
maya_events = maya_att.merge(prepared_table_1, how='left', left_on='link_to_event', right_on='event_id')
# Select distinct event names attended by Maya
target = maya_events[['event_name']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
