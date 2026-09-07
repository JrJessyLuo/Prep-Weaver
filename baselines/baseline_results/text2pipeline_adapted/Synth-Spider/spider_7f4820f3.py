import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'b', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'clr', 'func': "def transform(s):\n    s = str(s)\n    s = s.strip().lower()\n    # remove leading/trailing underscores\n    s = s.strip('_')\n    return s"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'b', 'new_name': 'boat_id'}, {'old_name': 'name', 'new_name': 'boat_name'}, {'old_name': 'clr', 'new_name': 'color'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['boat_id', 'boat_name', 'color']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'sid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'date_value_pairs', 'split_comma': True}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'date_value_pairs', 'target_columns': ['date_str', 'boat_str'], 'func': 'def transform(s):\n    s = str(s)\n    parts = s.split(":", 1)\n    if len(parts) == 2:\n        return [parts[0], parts[1]]\n    return [s, None]'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'boat_str', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'boat_str', 'target_columns': ['boat_id', '_drop'], 'func': 'def transform(s):\n    try:\n        return [int(float(s)), None]\n    except Exception:\n        return [None, None]'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'date_str', 'new_name': 'res_date'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['sid', 'res_date', 'boat_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['b'] = pd.to_numeric(tmp_0['b'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    s = s.strip().lower()\n    # remove leading/trailing underscores\n    s = s.strip('_')\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['clr'] = tmp_1['clr'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'b': 'boat_id', 'name': 'boat_name', 'clr': 'color'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['boat_id', 'boat_name', 'color']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['sid'] = pd.to_numeric(tmp_0['sid'], errors='coerce').fillna(0).astype(int)
    # Step 2: Explode
    tmp_1 = tmp_0.copy()
    tmp_1['date_value_pairs'] = tmp_1['date_value_pairs'].apply(lambda x: str(x).split(',') if pd.notna(x) else x)
    tmp_1 = tmp_1.explode('date_value_pairs')
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    parts = s.split(":", 1)\n    if len(parts) == 2:\n        return [parts[0], parts[1]]\n    return [s, None]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['date_value_pairs'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['date_str'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['boat_str'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['boat_str'] = pd.to_numeric(tmp_3['boat_str'], errors='coerce').astype(float)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    try:\n        return [int(float(s)), None]\n    except Exception:\n        return [None, None]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_4['boat_str'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['boat_id'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['_drop'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'date_str': 'res_date'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['sid', 'res_date', 'boat_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t = prepared_table_2.merge(prepared_table_1, how='inner', on='boat_id')
# Normalize color text for filtering (robust match for red or blue)
t['color_norm'] = t['color'].astype(str).str.strip().str.lower()
# Also remove leading/trailing underscores to match samples
t['color_norm'] = t['color_norm'].str.strip('_')
mask = t['color_norm'].isin(['red','blue'])
filtered = t[mask]
# Get unique sids who reserved red or blue boats
target = filtered[['sid']].drop_duplicates().sort_values('sid').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
