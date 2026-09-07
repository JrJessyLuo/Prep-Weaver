import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'heat', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'nation_result', 'target_columns': ['nation', 'result'], 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('|', 1)\n    left = parts[0] if len(parts) > 0 else ''\n    right = parts[1] if len(parts) > 1 else ''\n    return [left, right]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'nation', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'result', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'name', 'nation', 'result']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'cyclist_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'bike_purchase_combined', 'target_columns': ['bike_type_id', 'purchase_year'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('_', 1)\n    if len(parts) == 2:\n        return parts\n    return [parts[0] if parts else None, None]"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'bike_type_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'purchase_year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['cyclist_id', 'bike_type_id', 'purchase_year']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'weight', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'price', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'product_name', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'material', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'product_name', 'target_columns': ['is_racing_bike'], 'func': "def transform(s):\n    name = str(s).upper()\n    cues = [\n        'AERO', 'AEROAD', 'SUPER', 'RACE', 'DURA ACE',\n        'BIANCHI SPECIALISSIMA', 'CANNONDALE SUPERSIX', 'CANYON AEROAD'\n    ]\n    is_rb = any(cue in name for cue in cues)\n    return [bool(is_rb)]\n"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'product_name', 'is_racing_bike']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['heat'] = pd.to_numeric(tmp_1['heat'], errors='coerce').fillna(0).astype(int)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    parts = s.split('|', 1)\n    left = parts[0] if len(parts) > 0 else ''\n    right = parts[1] if len(parts) > 1 else ''\n    return [left, right]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_2['nation_result'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['nation'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['result'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['nation'] = tmp_3['nation'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['result'] = tmp_4['result'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['id', 'name', 'nation', 'result']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['cyclist_id'] = pd.to_numeric(tmp_0['cyclist_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('_', 1)\n    if len(parts) == 2:\n        return parts\n    return [parts[0] if parts else None, None]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_1['bike_purchase_combined'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['bike_type_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['purchase_year'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['bike_type_id'] = pd.to_numeric(tmp_2['bike_type_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['purchase_year'] = pd.to_numeric(tmp_3['purchase_year'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['cyclist_id', 'bike_type_id', 'purchase_year']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['weight'] = pd.to_numeric(tmp_1['weight'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['price'] = pd.to_numeric(tmp_2['price'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['product_name'] = tmp_3['product_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['material'] = tmp_4['material'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SplitColumn
    tmp_5 = tmp_4.copy()
    _ns_3 = {}
    exec("def transform(s):\n    name = str(s).upper()\n    cues = [\n        'AERO', 'AEROAD', 'SUPER', 'RACE', 'DURA ACE',\n        'BIANCHI SPECIALISSIMA', 'CANNONDALE SUPERSIX', 'CANYON AEROAD'\n    ]\n    is_rb = any(cue in name for cue in cues)\n    return [bool(is_rb)]\n", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_5['product_name'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_5['is_racing_bike'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['id', 'product_name', 'is_racing_bike']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
merged = prepared_table_2.merge(prepared_table_3, left_on='bike_type_id', right_on='id', how='left')
# Identify cyclists who purchased any racing bike
purchased_racing = merged[merged['is_racing_bike'] == True][['cyclist_id']].drop_duplicates()
# Left-join cyclists to the set of racing purchasers and keep those with no match
cyclists = prepared_table_1.copy()
result_df = cyclists.merge(purchased_racing, left_on='id', right_on='cyclist_id', how='left', indicator=True)
no_racing = result_df[result_df['_merge'] == 'left_only'][['name', 'nation', 'result']]
# Final projection
target = no_racing.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
