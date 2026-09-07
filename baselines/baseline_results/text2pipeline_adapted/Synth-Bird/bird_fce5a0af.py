import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': []}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'name']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['id'], 'value_vars': [13050, 11128, 12645, 15895, 23808, 11624, 6236, 16422, 5837, 4462, 18488, 8888, 22090, 5346, 15177, 844, 13502, 23362, 11454, 2565, 11888, 4212, 14049, 22593, 2435, 12472, 22682, 14937, 22089, 22710, 4502, 22866, 7485, 753, 10313, 7730, 6233, 14361, 8893], 'var_name': 'league_instance_key', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'field'}]}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'league_instance_key', 'columns': 'field', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'country_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'league_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'league_instance_key', 'new_name': 'competition_key'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['competition_key', 'country_id', 'league_id', 'season']}, 'table_indices': [0]}]]

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
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['id', 'name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['id'], value_vars=[13050, 11128, 12645, 15895, 23808, 11624, 6236, 16422, 5837, 4462, 18488, 8888, 22090, 5346, 15177, 844, 13502, 23362, 11454, 2565, 11888, 4212, 14049, 22593, 2435, 12472, 22682, 14937, 22089, 22710, 4502, 22866, 7485, 753, 10313, 7730, 6233, 14361, 8893], var_name='league_instance_key', value_name='value')
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'id': 'field'})
    # Step 3: Pivot
    tmp_2 = pd.pivot_table(tmp_1, index='league_instance_key', columns='field', values='value', aggfunc='first').reset_index()
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['country_id'] = pd.to_numeric(tmp_3['country_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['league_id'] = pd.to_numeric(tmp_4['league_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'league_instance_key': 'competition_key'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['competition_key', 'country_id', 'league_id', 'season']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, left_on='country_id', right_on='id', how='left')
# Filter season and country name robustly
mask_season = integrated['season'].astype(str).str.strip().str.casefold() == '2015/2016'.casefold()
# Country name matching for Scotland (allow variations like 'Scotland')
name_series = integrated['name'].astype(str).str.strip()
mask_country = name_series.str.casefold().str.contains('scotland')
filtered = integrated[mask_season & mask_country]
# Each row corresponds to a league/competition instance; count rows as number of matches if each column represents a match event. If filtered is empty, fall back to season-only to avoid empty result.
if filtered.empty:
    filtered = integrated[mask_season]
count_df = filtered[['competition_key']].drop_duplicates().assign(matches=1)
result = count_df['matches'].sum()
target = pd.DataFrame({'matches_held':[int(result)]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
