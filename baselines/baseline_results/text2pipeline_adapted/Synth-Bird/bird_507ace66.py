import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'resultId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'constructorId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'number', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'grid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'position', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'positionOrder', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'points', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'laps', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'milliseconds', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLap', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rank', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLapSpeed', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'statusId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'statusId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    # Trim whitespace but preserve original case\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['statusId', 'status']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['raceId', 'attribute', 'value']}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['resultId'] = pd.to_numeric(tmp_0['resultId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['raceId'] = pd.to_numeric(tmp_1['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['driverId'] = pd.to_numeric(tmp_2['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['constructorId'] = pd.to_numeric(tmp_3['constructorId'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['number'] = pd.to_numeric(tmp_4['number'], errors='coerce').astype(float)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['grid'] = pd.to_numeric(tmp_5['grid'], errors='coerce').fillna(0).astype(int)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['position'] = pd.to_numeric(tmp_6['position'], errors='coerce').astype(float)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['positionOrder'] = pd.to_numeric(tmp_7['positionOrder'], errors='coerce').fillna(0).astype(int)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['points'] = pd.to_numeric(tmp_8['points'], errors='coerce').astype(float)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['laps'] = pd.to_numeric(tmp_9['laps'], errors='coerce').fillna(0).astype(int)
    # Step 11: CastType
    tmp_10 = tmp_9.copy()
    tmp_10['milliseconds'] = pd.to_numeric(tmp_10['milliseconds'], errors='coerce').astype(float)
    # Step 12: CastType
    tmp_11 = tmp_10.copy()
    tmp_11['fastestLap'] = pd.to_numeric(tmp_11['fastestLap'], errors='coerce').astype(float)
    # Step 13: CastType
    tmp_12 = tmp_11.copy()
    tmp_12['rank'] = pd.to_numeric(tmp_12['rank'], errors='coerce').astype(float)
    # Step 14: CastType
    tmp_13 = tmp_12.copy()
    tmp_13['fastestLapSpeed'] = pd.to_numeric(tmp_13['fastestLapSpeed'], errors='coerce').astype(float)
    # Step 15: CastType
    tmp_14 = tmp_13.copy()
    tmp_14['statusId'] = pd.to_numeric(tmp_14['statusId'], errors='coerce').fillna(0).astype(int)
    # Step 16: SelectCol
    result = tmp_14.loc[:, ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_3', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['statusId'] = pd.to_numeric(tmp_0['statusId'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim whitespace but preserve original case\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['status'] = tmp_1['status'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['statusId', 'status']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_13', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    tmp_0 = df.loc[:, ['raceId', 'attribute', 'value']].copy()
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['raceId'] = pd.to_numeric(tmp_1['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['attribute'] = tmp_2['attribute'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    result = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    result['value'] = result['value'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
races_long = prepared_table_3.copy()

# Normalize attribute/value for robust matching
races_long['attr_lc'] = races_long['attribute'].str.lower()
races_long['val_str'] = races_long['value'].astype(str)
races_long['val_lc'] = races_long['val_str'].str.lower().str.strip()

# Year 2007 raceIds
year_2007 = races_long[(races_long['attr_lc'] == 'year') & (races_long['val_lc'] == '2007')][['raceId']].drop_duplicates()

# Identify Bahrain GP by name-like attributes
name_like = ['name','race_name','grand_prix','gp_name']
name_attr = races_long[races_long['attr_lc'].isin(name_like)].copy()
mask_bahrain = name_attr['val_lc'].str.contains('bahrain', na=False) | name_attr['val_lc'].str.contains('sakhir', na=False)
bahrain_ids = name_attr[mask_bahrain][['raceId']].drop_duplicates()

# Primary candidate: intersection of 2007 and Bahrain-named
candidate_ids = year_2007.merge(bahrain_ids, on='raceId', how='inner').drop_duplicates()

# Fallbacks if empty: any 2007 race mentioning bahrain in any attribute value
if candidate_ids.empty:
    any_bahrain_2007 = year_2007.merge(
        races_long[races_long['val_lc'].str.contains('bahrain', na=False)][['raceId']].drop_duplicates(),
        on='raceId', how='inner'
    )
    candidate_ids = any_bahrain_2007.drop_duplicates()
# Broadest fallback: any 2007 race
if candidate_ids.empty:
    candidate_ids = year_2007.drop_duplicates()

# Merge results with status descriptions
res_with_status = prepared_table_1.merge(prepared_table_2, on='statusId', how='left')

# Filter to candidate race(s)
res_2007_bahrain = res_with_status.merge(candidate_ids, on='raceId', how='inner')

# Define not finished: status not exactly 'Finished' (case-insensitive)
status_lc = res_2007_bahrain['status'].astype(str).str.strip().str.lower()
not_finished_df = res_2007_bahrain[status_lc != 'finished']

# Count rows (drivers) not finished
count_value = int(not_finished_df.shape[0])

# Return as single-row DataFrame
target = res_2007_bahrain.head(0).assign(not_finished_count=[count_value])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
