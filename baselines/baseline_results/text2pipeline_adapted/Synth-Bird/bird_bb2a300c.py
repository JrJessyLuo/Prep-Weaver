import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'nationality', 'func': 'def transform(s):\n    # Trim but preserve original casing\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'forename', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'surname', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'driverRef', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'nationality', 'forename', 'surname', 'driverRef']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'round', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'year', 'round', 'name', 'date']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'resultId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'constructorId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'grid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'positionOrder', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'laps', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'statusId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'number', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'position', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'points', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'milliseconds', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLap', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rank', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLapSpeed', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['resultId', 'raceId', 'driverId', 'statusId', 'positionText', 'laps']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'statusId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['statusId', 'status']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim but preserve original casing\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['nationality'] = tmp_1['nationality'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['forename'] = tmp_2['forename'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['surname'] = tmp_3['surname'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['driverRef'] = tmp_4['driverRef'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['driverId', 'nationality', 'forename', 'surname', 'driverRef']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['raceId'] = pd.to_numeric(tmp_0['raceId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['year'] = pd.to_numeric(tmp_1['year'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['round'] = pd.to_numeric(tmp_2['round'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['date'] = pd.to_datetime(tmp_3['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['raceId', 'year', 'round', 'name', 'date']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
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
    result = tmp_14.loc[:, ['resultId', 'raceId', 'driverId', 'statusId', 'positionText', 'laps']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['statusId'] = pd.to_numeric(tmp_0['statusId'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['status'] = tmp_1['status'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['statusId', 'status']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_13', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_3.merge(prepared_table_2, how='inner', on='raceId').merge(prepared_table_1, how='inner', on='driverId').merge(prepared_table_4, how='left', on='statusId')
# Filter to Japanese drivers and years 2007-2009 (broaden with contains if exact match yields none)
mask_year = (integrated['year'] >= 2007) & (integrated['year'] <= 2009)
mask_nat = integrated['nationality'].str.lower() == 'japanese'
sub = integrated[mask_nat & mask_year].copy()
if sub.empty:
    mask_nat2 = integrated['nationality'].str.lower().str.contains('japan', na=False)
    sub = integrated[mask_nat2 & mask_year].copy()
# Determine completion: Finished by status OR classified numeric position
status_lower = sub['status'].str.lower()
finished_by_status = status_lower == 'finished'
pos_text = sub['positionText'].astype(str)
finished_by_postext = pos_text.str.fullmatch(r'\d+').fillna(False)
sub['completed'] = finished_by_status | finished_by_postext
# Aggregate per driver and overall
agg = sub.groupby(['driverId', 'forename', 'surname'], as_index=False).agg(total_races=('resultId','count'), completed_races=('completed','sum'))
agg['driver_completion_pct'] = (agg['completed_races'] / agg['total_races']) * 100
if len(sub) > 0:
    overall_completed = int(sub['completed'].sum())
    overall_total = int(len(sub))
    overall_pct = (overall_completed / overall_total) * 100
else:
    overall_completed = None
    overall_total = None
    overall_pct = None
agg['overall_completed_races'] = overall_completed
agg['overall_total_races'] = overall_total
agg['overall_completion_pct'] = overall_pct
target = agg.sort_values(['driverId','surname','forename']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
