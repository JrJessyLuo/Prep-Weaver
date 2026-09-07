import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'resultId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'constructorId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'grid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'positionOrder', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'laps', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'statusId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'number', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'position', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'points', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'milliseconds', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLap', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rank', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLapSpeed', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'dob', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'driverRef', 'number', 'code', 'forename', 'surname', 'dob', 'nationality', 'url']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['raceId'] = pd.to_numeric(tmp_1['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['resultId'] = pd.to_numeric(tmp_2['resultId'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['constructorId'] = pd.to_numeric(tmp_3['constructorId'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['grid'] = pd.to_numeric(tmp_4['grid'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['positionOrder'] = pd.to_numeric(tmp_5['positionOrder'], errors='coerce').fillna(0).astype(int)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['laps'] = pd.to_numeric(tmp_6['laps'], errors='coerce').fillna(0).astype(int)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['statusId'] = pd.to_numeric(tmp_7['statusId'], errors='coerce').fillna(0).astype(int)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['number'] = pd.to_numeric(tmp_8['number'], errors='coerce').astype(float)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['position'] = pd.to_numeric(tmp_9['position'], errors='coerce').astype(float)
    # Step 11: CastType
    tmp_10 = tmp_9.copy()
    tmp_10['points'] = pd.to_numeric(tmp_10['points'], errors='coerce').astype(float)
    # Step 12: CastType
    tmp_11 = tmp_10.copy()
    tmp_11['milliseconds'] = pd.to_numeric(tmp_11['milliseconds'], errors='coerce').astype(float)
    # Step 13: CastType
    tmp_12 = tmp_11.copy()
    tmp_12['fastestLap'] = pd.to_numeric(tmp_12['fastestLap'], errors='coerce').astype(float)
    # Step 14: CastType
    tmp_13 = tmp_12.copy()
    tmp_13['rank'] = pd.to_numeric(tmp_13['rank'], errors='coerce').astype(float)
    # Step 15: CastType
    tmp_14 = tmp_13.copy()
    tmp_14['fastestLapSpeed'] = pd.to_numeric(tmp_14['fastestLapSpeed'], errors='coerce').astype(float)
    # Step 16: SelectCol
    result = tmp_14.loc[:, ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['dob'] = pd.to_datetime(tmp_1['dob'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['driverId', 'driverRef', 'number', 'code', 'forename', 'surname', 'dob', 'nationality', 'url']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='driverId')
# Keep rows where fastestLapSpeed is present to find the fastest overall
integrated_nonnull = integrated[integrated['fastestLapSpeed'].notna()].copy()
if integrated_nonnull.empty:
    # Fallback: if no speeds present after merge, use all integrated rows
    working = integrated.copy()
else:
    working = integrated_nonnull
# Find the maximum fastestLapSpeed and select the driver(s)
max_speed = working['fastestLapSpeed'].max()
fastest_rows = working[working['fastestLapSpeed'] == max_speed]
# Project the driver's nationality (deduplicate in case of ties)
target = fastest_rows[['nationality']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
