import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'ag', 'new_name': 'age'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'sid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rtg', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'age', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['sid', 'name', 'rtg', 'age']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'sid_bid', 'target_columns': ['sid_part', 'bid_part'], 'func': "def transform(s):\n    parts = str(s).split('_', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'sid_part', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'bid_part', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'sid_part', 'new_name': 'sid'}, {'old_name': 'bid_part', 'new_name': 'bid'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'day', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['day', 'sid', 'bid']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'ag': 'age'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['sid'] = pd.to_numeric(tmp_1['sid'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['rtg'] = pd.to_numeric(tmp_2['rtg'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['age'] = pd.to_numeric(tmp_3['age'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['name'] = tmp_4['name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['sid', 'name', 'rtg', 'age']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('_', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['sid_bid'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['sid_part'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['bid_part'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['sid_part'] = pd.to_numeric(tmp_1['sid_part'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['bid_part'] = pd.to_numeric(tmp_2['bid_part'], errors='coerce').fillna(0).astype(int)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'sid_part': 'sid', 'bid_part': 'bid'})
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['day'] = tmp_4['day'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['day', 'sid', 'bid']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2[['sid']].drop_duplicates(), how='left', on='sid', indicator=True)
no_reservations = integrated[integrated['_merge'] == 'left_only']
target = no_reservations[['sid']].sort_values('sid').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
