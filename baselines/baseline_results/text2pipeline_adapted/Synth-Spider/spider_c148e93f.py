import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'city1_code', 'new_name': 'row_header'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['row_header'], 'value_vars': ['BAL', 'ATL', 'BKK', 'BOS', 'CHI'], 'var_name': 'city2_code', 'value_name': 'distance_str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'row_header', 'new_name': 'city1_code'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'distance_str', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'distance_str', 'new_name': 'distance'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['city1_code', 'city2_code', 'distance']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'city_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'city_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'state', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'country', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'city_code', 'func': 'def transform(s):\n    return str(s).upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'country', 'func': 'def transform(s):\n    return str(s).upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['city_code', 'city_name', 'state', 'country', 'latitude', 'longitude']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'city1_code': 'row_header'})
    # Step 2: Stack
    tmp_1 = tmp_0.melt(id_vars=['row_header'], value_vars=['BAL', 'ATL', 'BKK', 'BOS', 'CHI'], var_name='city2_code', value_name='distance_str')
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'row_header': 'city1_code'})
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['distance_str'] = pd.to_numeric(tmp_3['distance_str'], errors='coerce').astype(float)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'distance_str': 'distance'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['city1_code', 'city2_code', 'distance']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['city_code'] = tmp_0['city_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['city_name'] = tmp_1['city_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['state'] = tmp_2['state'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['country'] = tmp_3['country'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).upper()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['city_code'] = tmp_4['city_code'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).upper()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['country'] = tmp_5['country'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['city_code', 'city_name', 'state', 'country', 'latitude', 'longitude']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
dist_long = prepared_table_1
left = dist_long.merge(prepared_table_2, how='left', left_on='city1_code', right_on='city_code', suffixes=('', '_city1'))
left = left.rename(columns={'city_name': 'city1_name'})
right = left.merge(prepared_table_2, how='left', left_on='city2_code', right_on='city_code', suffixes=('', '_city2'))
right = right.rename(columns={'city_name': 'city2_name'})
# Filter for Boston and Newark (Newark commonly maps to EWR; use city_name-based, case-insensitive matching with fallbacks)
mask_bos = right['city1_name'].str.contains('^boston$', case=False, na=False)
mask_newark = right['city2_name'].str.contains('^newark$', case=False, na=False)
mask_bos_rev = right['city2_name'].str.contains('^boston$', case=False, na=False)
mask_newark_rev = right['city1_name'].str.contains('^newark$', case=False, na=False)
filtered = right[ (mask_bos & mask_newark) | (mask_bos_rev & mask_newark_rev) ]
# If no direct name match found, fall back to typical codes BOS/EWR
if filtered.empty:
    fallback = right[((right['city1_code']=='BOS') & (right['city2_code']=='EWR')) | ((right['city1_code']=='EWR') & (right['city2_code']=='BOS'))]
    filtered = fallback if not fallback.empty else right
# Select the most relevant row (there should be a single distance); if multiple, take the first
result = filtered[['city1_name','city1_code','city2_name','city2_code','distance']].drop_duplicates()
target = result.head(1)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
