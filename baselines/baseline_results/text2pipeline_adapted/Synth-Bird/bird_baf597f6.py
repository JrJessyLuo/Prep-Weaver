import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'round', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'circuitId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    # Trim but preserve original case\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'resultId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'constructorId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'grid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'positionOrder', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'statusId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'number', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'driverRef', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'code', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ming', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'xing', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'gj', 'func': 'def transform(s):\n    # preserve original casing but trim spaces\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'driverRef', 'number', 'code', 'ming', 'xing', 'dob', 'gj', 'url']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
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
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['circuitId'] = pd.to_numeric(tmp_3['circuitId'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim but preserve original case\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['name'] = tmp_4['name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['date'] = pd.to_datetime(tmp_5['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['raceId', 'year', 'round', 'circuitId', 'name', 'date', 'time', 'url']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
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
    tmp_6['statusId'] = pd.to_numeric(tmp_6['statusId'], errors='coerce').fillna(0).astype(int)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['resultId', 'raceId', 'driverId', 'constructorId', 'number', 'grid', 'position', 'positionText', 'positionOrder', 'points', 'laps', 'time', 'milliseconds', 'fastestLap', 'rank', 'fastestLapTime', 'fastestLapSpeed', 'statusId']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['number'] = pd.to_numeric(tmp_1['number'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['driverRef'] = tmp_2['driverRef'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['code'] = tmp_3['code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['ming'] = tmp_4['ming'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['xing'] = tmp_5['xing'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_5 = {}
    exec('def transform(s):\n    # preserve original casing but trim spaces\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_6['gj'] = tmp_6['gj'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['driverId', 'driverRef', 'number', 'code', 'ming', 'xing', 'dob', 'gj', 'url']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
races = prepared_table_1
results = prepared_table_2
drivers = prepared_table_3
# Join races to results
rr = results.merge(races[['raceId','year','name']], on='raceId', how='inner')
# Filter to 2008 Australian Grand Prix using robust, case-insensitive contains on name and exact year
mask_year = rr['year'] == 2008
mask_name = rr['name'].str.contains('Australian Grand Prix', case=False, na=False)
rr_2008_aus = rr[mask_year & mask_name]
# Join to drivers for nationality
rrd = rr_2008_aus.merge(drivers[['driverId','gj']], on='driverId', how='inner')
# Filter nationality equal to 'UN' robustly (case-insensitive, trim)
nat = rrd['gj'].astype(str).str.strip()
mask_un = nat.str.lower() == 'un'
subset = rrd[mask_un]
# Count distinct drivers participating under UN nationality for that race
target = subset[['driverId']].drop_duplicates().assign(count=1)
target = target.agg({'driverId':'nunique'}).to_frame(name='value').T
target = target.rename(columns={'driverId':'count_UN_drivers_2008_Australian_GP'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
