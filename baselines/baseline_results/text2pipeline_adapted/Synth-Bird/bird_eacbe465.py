import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'link_to_member', 'target_columns': ['event_component'], 'func': 'def transform(s):\n    return [s]'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['recD078PnS3x2doBe', 'recP6DJPyi5donvXL', 'rec28ORZgcm1dtqBZ', 'recTjHY5xXhvkCdVT', 'recZ4PkGERzl9ziHO', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recJMazpPVexyFYTc', 'reccW7q1KkhSKZsea', 'recjHj4BS5A541n9v', 'recL94zpn6Xh6kQii', 'reccSUPwy30AeZLEb', 'recttfySfQnYb68u3', 'recf4UKTfipCzgcSA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'rec75vvFxgYtHmqxY', 'reco0mr8dXTgs5wWA', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'rec4BLdZHS2Blfp4v'], 'target_column': 'member_id', 'func': "def transform(row):\n    for col in row.index:\n        if col == 'link_to_member' or col == 'event_component':\n            continue\n        val = row[col]\n        if val is None:\n            continue\n        s = str(val).strip()\n        if s == '' or s.lower() == 'nan':\n            continue\n        if s.startswith('rec') and len(s) >= 5:\n            return s\n    return None"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['event_component', 'member_id']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'member_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'phone', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'phone', 'full_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return [s]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['link_to_member'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['event_component'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: Concatenate
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(row):\n    for col in row.index:\n        if col == 'link_to_member' or col == 'event_component':\n            continue\n        val = row[col]\n        if val is None:\n            continue\n        s = str(val).strip()\n        if s == '' or s.lower() == 'nan':\n            continue\n        if s.startswith('rec') and len(s) >= 5:\n            return s\n    return None", globals(), _ns_2)
    _concat_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('concat')
    tmp_1['member_id'] = tmp_1[['recD078PnS3x2doBe', 'recP6DJPyi5donvXL', 'rec28ORZgcm1dtqBZ', 'recTjHY5xXhvkCdVT', 'recZ4PkGERzl9ziHO', 'recEFd8s6pkrTt4Pz', 'recEymrwCUKxiiosI', 'recQaxyXBQG5BBtD0', 'recT92PyyZCGq1R68', 'recJMazpPVexyFYTc', 'reccW7q1KkhSKZsea', 'recjHj4BS5A541n9v', 'recL94zpn6Xh6kQii', 'reccSUPwy30AeZLEb', 'recttfySfQnYb68u3', 'recf4UKTfipCzgcSA', 'recro8T1MPMwRadVH', 'recsTO4OZIF9rbubk', 'rec75vvFxgYtHmqxY', 'reco0mr8dXTgs5wWA', 'recuSfhAZIlKba4s2', 'recxBj3tjKTGHqucS', 'recUdRhbhcEO1Hk5r', 'recVsoJJHFI8bgtfw', 'rec4BLdZHS2Blfp4v']].apply(_concat_func_2, axis=1)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['event_component', 'member_id']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['member_id'] = tmp_0['member_id'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['phone'] = tmp_1['phone'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['member_id', 'phone', 'full_name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='member_id')
# Robust phone matching: exact match first, fallback to case-insensitive contains if needed
exact = integrated[integrated['phone'].astype(str) == '954-555-6240']
if exact.empty:
    ci = integrated[integrated['phone'].astype(str).str.contains('954-555-6240', case=False, na=False)]
    working = ci
else:
    working = exact
# Count distinct event components attended by the matching member(s)
result = working[['event_component']].drop_duplicates()
count_df = result.agg({'event_component': 'count'}).rename({'event_component': 'events_attended'})
target = count_df.to_frame().T

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
