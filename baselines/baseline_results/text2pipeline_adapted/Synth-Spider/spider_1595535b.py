import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'nation', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'heat_result', 'target_columns': ['heat_pos', 'result_time'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], '']\n    return [parts[0], parts[1]]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'result_time', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'name', 'nation', 'heat_pos', 'result_time']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'cid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'bike_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'py', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['cid', 'bike_id', 'py']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'product_material', 'target_columns': ['bike_name', 'material'], 'func': "def transform(s):\n    parts = str(s).split('###', 1)\n    left = parts[0] if len(parts) > 0 else ''\n    right = parts[1] if len(parts) > 1 else ''\n    return [left, right]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'bike_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'material', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'weight', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'price', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'bike_name', 'material', 'weight', 'price']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['name'] = tmp_1['name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['nation'] = tmp_2['nation'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], '']\n    return [parts[0], parts[1]]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['heat_result'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['heat_pos'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['result_time'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['result_time'] = tmp_4['result_time'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['id', 'name', 'nation', 'heat_pos', 'result_time']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['cid'] = pd.to_numeric(tmp_0['cid'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['bike_id'] = pd.to_numeric(tmp_1['bike_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['py'] = pd.to_numeric(tmp_2['py'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['cid', 'bike_id', 'py']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('###', 1)\n    left = parts[0] if len(parts) > 0 else ''\n    right = parts[1] if len(parts) > 1 else ''\n    return [left, right]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_1['product_material'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['bike_name'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['material'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['bike_name'] = tmp_2['bike_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['material'] = tmp_3['material'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['weight'] = pd.to_numeric(tmp_4['weight'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['price'] = pd.to_numeric(tmp_5['price'], errors='coerce').astype(float)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['id', 'bike_name', 'material', 'weight', 'price']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', left_on='id', right_on='cid').merge(prepared_table_3, how='inner', left_on='bike_id', right_on='id')
# Parse times as mm:ss.mmm for comparison; handle robustness by splitting on ':' and casting
# Create total milliseconds for result_time and threshold
rt = integrated['result_time'].astype(str)
# Expect format like '4:16.571'; split minutes and seconds.millis
mins = rt.str.extract(r'^(\d+):')[0].astype(float)
secs = rt.str.extract(r':(\d+\.\d+)$')[0].astype(float)
integrated['result_ms'] = (mins*60.0 + secs) * 1000.0
# Threshold '4:21.558'
th_mins = 4.0
th_secs = 21.558
threshold_ms = (th_mins*60.0 + th_secs) * 1000.0
filt = integrated.loc[integrated['result_ms'] < threshold_ms]
# Distinct bike names purchased by those cyclists
result = filt[['bike_name']].drop_duplicates().sort_values('bike_name')
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
