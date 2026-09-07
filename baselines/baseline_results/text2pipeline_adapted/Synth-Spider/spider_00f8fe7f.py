import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Platform_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'pn', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'md', 'func': 'def transform(s):\n    s = str(s).strip()\n    return s.title()\n'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'pn', 'new_name': 'Platform_Name'}, {'old_name': 'md', 'new_name': 'Market_District'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Platform_ID', 'Platform_Name', 'Market_District', 'Download_rank']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Game_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Title', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Franchise', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Developers', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['Game_ID', 'Title', 'Release_Date', 'Franchise', 'Developers'], 'value_vars': [1, 2, 3, 4], 'var_name': 'Platform_ID', 'value_name': 'Platform_Metric'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Platform_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Game_ID', 'Title', 'Release_Date', 'Franchise', 'Developers', 'Platform_ID', 'Platform_Metric']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Platform_ID'] = pd.to_numeric(tmp_0['Platform_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['pn'] = tmp_1['pn'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    return s.title()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['md'] = tmp_2['md'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'pn': 'Platform_Name', 'md': 'Market_District'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Platform_ID', 'Platform_Name', 'Market_District', 'Download_rank']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Game_ID'] = pd.to_numeric(tmp_0['Game_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Title'] = tmp_1['Title'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Franchise'] = tmp_2['Franchise'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['Developers'] = tmp_3['Developers'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: Stack
    tmp_4 = tmp_3.melt(id_vars=['Game_ID', 'Title', 'Release_Date', 'Franchise', 'Developers'], value_vars=[1, 2, 3, 4], var_name='Platform_ID', value_name='Platform_Metric')
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['Platform_ID'] = pd.to_numeric(tmp_5['Platform_ID'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['Game_ID', 'Title', 'Release_Date', 'Franchise', 'Developers', 'Platform_ID', 'Platform_Metric']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
g_long = prepared_table_2.copy()
# Join all game-platform rows to platform attributes
integrated = g_long.merge(prepared_table_1, on='Platform_ID', how='inner')
# Filter to market districts Asia or USA (case-insensitive, robust)
mask = integrated['Market_District'].astype(str).str.strip().str.casefold().isin(['asia','usa'])
filtered = integrated[mask]
# Keep titles of games that have at least one platform in those districts
result = filtered[['Title']].drop_duplicates().sort_values('Title')
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
