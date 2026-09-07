import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['circuitId','circuitRef','name','location','Austria']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[table_1['mingcheng'].astype(str).str.contains('Austrian Grand Prix', case=False, na=False), ['raceId','year','round','luquId','mingcheng','date','time','url']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    target = target.assign(raceId=pd.to_numeric(target['raceId'], errors='coerce'), driverId=pd.to_numeric(target['driverId'], errors='coerce'), lap=pd.to_numeric(target['lap'], errors='coerce'), position=pd.to_numeric(target['position'], errors='coerce'), milliseconds=pd.to_numeric(target['milliseconds'], errors='coerce'))
    target = target.assign(time=target['time'].astype('string').str.strip())
    target = target.dropna(subset=['raceId','driverId','lap','position','milliseconds','time'])
    target = target[target['time'].ne('')].copy()
    target = target.drop_duplicates(subset=['raceId','driverId','lap'], keep='last')
    target = target.astype({'raceId':'int64','driverId':'int64','lap':'int64','position':'int64','milliseconds':'int64'})
    target = target[['raceId','driverId','lap','position','time','milliseconds']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_circuits = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_races = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_lap_times = prepared_table_3

# Assume prepared_* dataframes already exist
# 1) Join races to circuits to identify Austrian GP races
races_with_circuit = prepared_races.merge(prepared_circuits, left_on='luquId', right_on='circuitId', how='inner', suffixes=('_race','_circuit'))

# 2) Filter to Austrian Grand Prix by race name containing 'Austrian Grand Prix' (case-insensitive)
austrian_races = races_with_circuit[races_with_circuit['mingcheng'].str.contains('Austrian Grand Prix', case=False, na=False)]

# 3) Join lap times to the filtered Austrian races
at_laps = prepared_lap_times.merge(austrian_races[['raceId']], on='raceId', how='inner')

# 4) Find overall minimum lap time (lap record) among all Austrian GP laps
if len(at_laps) == 0:
    target = pd.DataFrame([])
else:
    min_ms = at_laps['milliseconds'].min()
    record_rows = at_laps[at_laps['milliseconds'] == min_ms]
    # Keep the time string and milliseconds as the record; include raceId/driverId for evidence
    target = record_rows[['raceId','driverId','lap','time','milliseconds']].drop_duplicates()

# 'target' now contains the lap record(s) for the Austrian Grand Prix Circuit with evidence columns.

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
