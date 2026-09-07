import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['id', 'borderColor']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'id', 'target_columns': ['card_ids_raw'], 'func': 'def transform(s):\n    import ast\n    try:\n        lst = ast.literal_eval(str(s))\n    except Exception:\n        lst = []\n    out = []\n    for x in lst:\n        sx = str(x)\n        if (sx.startswith("\'") and sx.endswith("\'")) or (sx.startswith(\'"\') and sx.endswith(\'"\')):\n            sx = sx[1:-1]\n        if (sx.startswith("\'") and sx.endswith("\'")) or (sx.startswith(\'"\') and sx.endswith(\'"\')):\n            sx = sx[1:-1]\n        out.append(sx)\n    return [out]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'value', 'target_columns': ['value_list'], 'func': 'def transform(s):\n    import ast\n    try:\n        lst = ast.literal_eval(str(s))\n    except Exception:\n        lst = []\n    return [list(map(str,lst))]'}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'card_ids_raw', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'value_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'value_list', 'target_columns': ['format_name', 'status', 'status_uuid'], 'func': "def transform(s):\n    parts = str(s).split('|',2)\n    while len(parts)<3:\n        parts.append('')\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'format_name', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'card_ids_raw', 'target_columns': ['card_id_str'], 'func': 'def transform(s):\n    sx = str(s)\n    if (sx.startswith("\'") and sx.endswith("\'")) or (sx.startswith(\'"\') and sx.endswith(\'"\')):\n        sx = sx[1:-1]\n    return [sx]'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'card_id_str', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'card_id_str', 'new_name': 'card_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['card_id', 'format_name', 'status']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['id', 'borderColor']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import ast\n    try:\n        lst = ast.literal_eval(str(s))\n    except Exception:\n        lst = []\n    out = []\n    for x in lst:\n        sx = str(x)\n        if (sx.startswith("\'") and sx.endswith("\'")) or (sx.startswith(\'"\') and sx.endswith(\'"\')):\n            sx = sx[1:-1]\n        if (sx.startswith("\'") and sx.endswith("\'")) or (sx.startswith(\'"\') and sx.endswith(\'"\')):\n            sx = sx[1:-1]\n        out.append(sx)\n    return [out]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['id'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['card_ids_raw'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import ast\n    try:\n        lst = ast.literal_eval(str(s))\n    except Exception:\n        lst = []\n    return [list(map(str,lst))]', globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['value'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['value_list'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 3: Explode
    tmp_2 = tmp_1.explode('card_ids_raw')
    # Step 4: Explode
    tmp_3 = tmp_2.explode('value_list')
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec("def transform(s):\n    parts = str(s).split('|',2)\n    while len(parts)<3:\n        parts.append('')\n    return parts", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_4['value_list'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['format_name'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_4['status'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_4['status_uuid'] = _split_values_3.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['format_name'] = tmp_5['format_name'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_6['status'] = tmp_6['status'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 8: SplitColumn
    tmp_7 = tmp_6.copy()
    _ns_6 = {}
    exec('def transform(s):\n    sx = str(s)\n    if (sx.startswith("\'") and sx.endswith("\'")) or (sx.startswith(\'"\') and sx.endswith(\'"\')):\n        sx = sx[1:-1]\n    return [sx]', globals(), _ns_6)
    _split_func_6 = _ns_6.get('transform') or _ns_6.get('transform') or _ns_6.get('split')
    _split_values_6 = tmp_7['card_ids_raw'].apply(_split_func_6)
    _split_values_6 = _split_values_6.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_7['card_id_str'] = _split_values_6.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['card_id_str'] = pd.to_numeric(tmp_8['card_id_str'], errors='coerce').fillna(0).astype(int)
    # Step 10: Rename
    tmp_9 = tmp_8.rename(columns={'card_id_str': 'card_id'})
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['card_id', 'format_name', 'status']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1.copy()
t2 = prepared_table_2.copy()
# Join on card id
integrated = t2.merge(t1, left_on='card_id', right_on='id', how='inner')
# Filter banned and white border
banned = integrated[integrated['status'].str.lower() == 'banned']
white = banned[banned['borderColor'].str.lower() == 'white']
# Count how many such rows/cards
result = white.agg({'card_id':'nunique'})
target = result.to_frame().transpose().rename(columns={'card_id':'white_border_banned_count'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
