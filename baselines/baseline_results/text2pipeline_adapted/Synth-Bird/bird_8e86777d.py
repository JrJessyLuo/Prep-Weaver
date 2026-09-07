import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Stack', 'params': {'id_vars': ['id'], 'value_vars': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], 'var_name': 'hero_index', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'hero_index', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'hero_index', 'columns': 'id', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'superhero_name', 'new_name': 'hero_name'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'hero_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['hero_index', 'hero_name']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'hero_power', 'target_columns': ['hero_index', 'power_index'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 2:\n        return [parts[0], parts[1]]\n    return [None, None]"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'hero_index', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'power_index', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['hero_power']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['hero_index', 'power_index']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['id'], value_vars=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39], var_name='hero_index', value_name='value')
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['hero_index'] = pd.to_numeric(tmp_1['hero_index'], errors='coerce').fillna(0).astype(int)
    # Step 3: Pivot
    tmp_2 = pd.pivot_table(tmp_1, index='hero_index', columns='id', values='value', aggfunc='first').reset_index()
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'superhero_name': 'hero_name'})
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['hero_name'] = tmp_4['hero_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['hero_index', 'hero_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('-', 1)\n    if len(parts) == 2:\n        return [parts[0], parts[1]]\n    return [None, None]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['hero_power'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['hero_index'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['power_index'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['hero_index'] = pd.to_numeric(tmp_1['hero_index'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['power_index'] = pd.to_numeric(tmp_2['power_index'], errors='coerce').fillna(0).astype(int)
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['hero_power'], errors='ignore').copy()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['hero_index', 'power_index']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='hero_index', how='inner')
mask = integrated['hero_name'].str.strip().str.casefold() == 'amazo'
amazo_powers = integrated[mask]
if amazo_powers.empty:
    # fallback: partial match on contains to avoid empty due to minor naming differences
    mask2 = integrated['hero_name'].str.strip().str.contains('amazo', case=False, na=False)
    amazo_powers = integrated[mask2]
count_df = amazo_powers.groupby('hero_name', as_index=False)['power_index'].nunique().rename(columns={'power_index':'power_count'})
if count_df.empty:
    target = amazo_powers[['hero_name']].drop_duplicates().assign(power_count=0)
else:
    target = count_df

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
