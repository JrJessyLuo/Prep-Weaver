import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'circuitId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'round', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'url', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'time', 'date_format': '%H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'circuitId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'lat', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'lng', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'alt', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'circuitRef', 'func': 'def transform(s):\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'location', 'func': 'def transform(s):\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'country', 'func': "def transform(s):\n    s = str(s).strip()\n    # remove any surrounding square brackets characters if present\n    # e.g., 'Malaysia[]' -> 'Malaysia'\n    # strip only bracket characters, not inner content\n    return s.strip('[]')"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'url', 'func': 'def transform(s):\n    s = str(s).strip()\n    return s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'name', 'new_name': 'circuit_name'}, {'old_name': 'url', 'new_name': 'circuit_url'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['circuitId', 'circuitRef', 'circuit_name', 'location', 'country', 'lat', 'lng', 'circuit_url']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['raceId'] = pd.to_numeric(tmp_0['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['circuitId'] = pd.to_numeric(tmp_1['circuitId'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['year'] = pd.to_numeric(tmp_2['year'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['round'] = pd.to_numeric(tmp_3['round'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['name'] = tmp_4['name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['url'] = tmp_5['url'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['date'] = pd.to_datetime(tmp_6['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['time'] = pd.to_datetime(tmp_7['time'], errors='coerce').dt.strftime('%H:%M:%S')
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['circuitId'] = pd.to_numeric(tmp_0['circuitId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['lat'] = pd.to_numeric(tmp_1['lat'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['lng'] = pd.to_numeric(tmp_2['lng'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['alt'] = pd.to_numeric(tmp_3['alt'], errors='coerce').astype(float)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['circuitRef'] = tmp_4['circuitRef'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['name'] = tmp_5['name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    return s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['location'] = tmp_6['location'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_4 = {}
    exec("def transform(s):\n    s = str(s).strip()\n    # remove any surrounding square brackets characters if present\n    # e.g., 'Malaysia[]' -> 'Malaysia'\n    # strip only bracket characters, not inner content\n    return s.strip('[]')", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_7['country'] = tmp_7['country'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_5 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    return s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_8['url'] = tmp_8['url'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 10: Rename
    tmp_9 = tmp_8.rename(columns={'name': 'circuit_name', 'url': 'circuit_url'})
    # Step 11: SelectCol
    result = tmp_9.loc[:, ['circuitId', 'circuitRef', 'circuit_name', 'location', 'country', 'lat', 'lng', 'circuit_url']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='circuitId')
mask_exact = integrated['name'].str.strip().str.lower() == 'malaysian grand prix'
filtered = integrated[mask_exact]
if filtered.empty:
    # fallback: broad contains match on plausible columns
    mask_broad = integrated['name'].str.strip().str.lower().str.contains('malaysian', na=False)
    filtered = integrated[mask_broad]
# Select distinct location coordinates and related context
cols = ['name', 'year', 'circuit_name', 'location', 'country', 'lat', 'lng']
existing = [c for c in cols if c in filtered.columns]
result = filtered[existing].drop_duplicates()
# If multiple years, coordinates are the same; return unique rows sorted by year
if 'year' in result.columns:
    result = result.sort_values(['year', 'circuit_name'], ascending=[True, True])
# Final projection prioritizes location and coordinates
target_cols_order = [c for c in ['circuit_name', 'location', 'country', 'lat', 'lng', 'name', 'year'] if c in result.columns]
target = result[target_cols_order]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
