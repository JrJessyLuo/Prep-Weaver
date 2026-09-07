import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'statusId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'statusId']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'status_combined', 'target_columns': ['statusId_str', 'status_label'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'statusId_str', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'statusId_str', 'new_name': 'statusId'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status_label', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['statusId', 'status_label']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'driverId', 'new_name': 'attribute'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['attribute'], 'value_vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], 'var_name': 'driverId_str', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'driverId_str', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'driverId_str', 'new_name': 'driverId'}]}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'driverId', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'nationality', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'nationality']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['statusId'] = pd.to_numeric(tmp_1['statusId'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['driverId', 'statusId']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['status_combined'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['statusId_str'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['status_label'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['statusId_str'] = pd.to_numeric(tmp_1['statusId_str'], errors='coerce').fillna(0).astype(int)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'statusId_str': 'statusId'})
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['status_label'] = tmp_3['status_label'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['statusId', 'status_label']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'driverId': 'attribute'})
    # Step 2: Stack
    tmp_1 = tmp_0.melt(id_vars=['attribute'], value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], var_name='driverId_str', value_name='value')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['driverId_str'] = pd.to_numeric(tmp_2['driverId_str'], errors='coerce').fillna(0).astype(int)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'driverId_str': 'driverId'})
    # Step 5: Pivot
    tmp_4 = pd.pivot_table(tmp_3, index='driverId', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['nationality'] = tmp_5['nationality'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['driverId', 'nationality']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='statusId', how='left').merge(prepared_table_3, on='driverId', how='left')
# Identify puncture-related statuses and American nationality robustly
puncture_mask = integrated['status_label'].astype(str).str.contains('puncture', case=False, na=False)
# Consider American drivers by nationality containing 'american' or exactly 'usa' variants
nat_series = integrated['nationality'].astype(str).str.lower()
american_mask = nat_series.str.contains('american', na=False) | nat_series.str.contains('\busa\b', na=False) | nat_series.str.contains('united states', na=False) | nat_series.str.contains('u\.s\.|u s a|u\. s\. a\.', regex=True, na=False)
filtered = integrated[puncture_mask & american_mask]
# Count unique American drivers with puncture status
count_df = filtered[['driverId']].drop_duplicates()
count = len(count_df)
target = pd.DataFrame({'american_drivers_with_puncture':[count]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
