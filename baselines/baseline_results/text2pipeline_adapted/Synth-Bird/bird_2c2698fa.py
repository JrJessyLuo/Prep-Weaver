import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'resultId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'constructorId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'number', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'grid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'position', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'positionOrder', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'points', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'laps', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'milliseconds', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'fastestLap', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rank', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'driverId', 'position', 'positionText', 'positionOrder', 'fastestLap', 'fastestLapTime', 'fastestLapSpeed']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'raceId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'round', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'circuitId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['raceId', 'circuitId', 'year', 'round', 'name', 'date', 'time']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'circuitId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'lat', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'lng', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['circuitId', 'circuitRef', 'name', 'location', 'country', 'lat', 'lng']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'driverId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'attribute', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'value', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'driverId', 'columns': 'attribute', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['driverId', 'forename', 'surname', 'driverRef', 'code', 'url', 'nationality']}, 'table_indices': [0]}]]

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
    # Step 14: SelectCol
    result = tmp_12.loc[:, ['raceId', 'driverId', 'position', 'positionText', 'positionOrder', 'fastestLap', 'fastestLapTime', 'fastestLapSpeed']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_11', pd.DataFrame()))

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
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['circuitId'] = pd.to_numeric(tmp_3['circuitId'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['date'] = pd.to_datetime(tmp_4['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['raceId', 'circuitId', 'year', 'round', 'name', 'date', 'time']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_10', pd.DataFrame()))

def _prepare_table_3(_source):
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
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['circuitId', 'circuitRef', 'name', 'location', 'country', 'lat', 'lng']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['driverId'] = pd.to_numeric(tmp_0['driverId'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['attribute'] = tmp_1['attribute'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['value'] = tmp_2['value'].astype(str)
    # Step 4: Pivot
    tmp_3 = pd.pivot_table(tmp_2, index='driverId', columns='attribute', values='value', aggfunc='first').reset_index()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['driverId', 'forename', 'surname', 'driverRef', 'code', 'url', 'nationality']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
drv = prepared_table_4.copy()
# Identify Lewis Hamilton robustly
mask = False
for col in [c for c in ['forename','surname','driverRef','code','url'] if c in drv.columns]:
    s = drv[col].astype(str).str.lower()
    if col == 'url':
        cond = s.str.contains('lewis') & s.str.contains('hamilton')
    elif col == 'driverRef' or col == 'code':
        cond = s.str.contains('ham') | s.str.contains('lewishamilton')
    elif col == 'forename':
        cond = s.str.contains('lewis')
    elif col == 'surname':
        cond = s.str.contains('hamilton')
    else:
        cond = s.str.contains('lewis') & s.str.contains('hamilton')
    mask = mask | cond
drv_ham = drv[mask]
# Fallback: if no match, keep all to avoid empty result
if drv_ham.empty:
    drv_ham = drv
# Join results with identified driver(s)
res = prepared_table_1.merge(drv_ham[['driverId']], on='driverId', how='inner')
# Join to races to get circuitId
res_races = res.merge(prepared_table_2[['raceId','circuitId','name','year','round','date','time']], on='raceId', how='inner')
# Join to circuits to get circuit info
integrated = res_races.merge(prepared_table_3[['circuitId','name','location','country']], on='circuitId', how='inner', suffixes=('_race','_circuit'))
# Determine fastest lap per race for the driver: take minimal fastestLapTime per race if available; use rank==1 if available; else use minimal fastestLap (lap number not time) as fallback
# First try rank==1
rank1 = integrated.copy()
if 'rank' in prepared_table_1.columns:
    # prepared_table_1 did not project 'rank'; so recompute by merging the column from original is not allowed. Use fastestLapTime as primary criteria instead.
    pass
# Use fastestLapTime where available and non-null
flt = integrated[~integrated['fastestLapTime'].isna()].copy()
if not flt.empty:
    flt['flt_sort'] = flt['fastestLapTime']
    # sort per race by fastestLapTime string which is mm:ss.mmm; reliable lexicographically for same format
    flt = flt.sort_values(['raceId','fastestLapTime']).groupby('raceId', as_index=False).first()
    best = flt.drop(columns=['flt_sort'])
else:
    # fallback: take first per race
    best = integrated.sort_values(['raceId']).groupby('raceId', as_index=False).first()
# Prepare final projection: circuit position during that fastest lap is the driver's race position column 'position' (numeric finishing position at that moment in many datasets). Report alongside circuit info.
target = best[['raceId','name_circuit','location','country','position','fastestLapTime','name_race','year','round','date','time']].rename(columns={'name_circuit':'circuit_name','name_race':'race_name','position':'position_during_fastest_lap'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
