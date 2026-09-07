import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['driverId','attribute','value']].copy()
    target['driverId'] = pd.to_numeric(target['driverId'], errors='coerce').astype('Int64')
    target['attribute'] = target['attribute'].astype('string').str.strip()
    target['value'] = target['value'].astype('string').str.strip()
    target = target.dropna(subset=['driverId','attribute','value'])
    target = target[(target['attribute'] != '') & (target['value'] != '')]
    target = target.drop_duplicates(subset=['driverId','attribute','value']).reset_index(drop=True)
    target['driverId'] = target['driverId'].astype('int64')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['resultId','raceId','driverId','fastestLap','rank','fastestLapTime']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['raceId','circuitId','name','year','round','date']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['circuitId','name','location','country','lat','lng']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
drivers_kv = prepared_table_1
prepared_table_2 = _prep_2(tables['table_11'])
race_results = prepared_table_2
prepared_table_3 = _prep_3(tables['table_10'])
races = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
circuits = prepared_table_4

# Assume prepared tables exist: drivers_kv, race_results, races, circuits
# 1) Identify Lewis Hamilton's driverId from drivers_kv
h_surname = drivers_kv[(drivers_kv['attribute'].str.lower()=='surname') & (drivers_kv['value'].str.lower()=='hamilton')][['driverId']].drop_duplicates()
# If multiple, keep unique ids
ham_driver_ids = set(h_surname['driverId'].astype(int))

# 2) Filter race_results for Hamilton
rr_ham = race_results[race_results['driverId'].astype(int).isin(ham_driver_ids)].copy()

# 3) Determine races where Hamilton set the fastest lap
# In many F1 results schemas, 'rank' == 1 on the row of the driver who recorded the fastest lap
rr_ham_fastest = rr_ham[(rr_ham['rank'].notna()) & (rr_ham['rank'].astype(float)==1.0)].copy()

# 4) Join to races to get circuitId, then to circuits to get circuit position (location/lat/lng)
rr_ham_fastest = rr_ham_fastest.merge(races[['raceId','circuitId','name','year','date']], on='raceId', how='left')
result = rr_ham_fastest.merge(circuits[['circuitId','name','location','country','lat','lng']], on='circuitId', how='left', suffixes=('_race','_circuit'))

# 5) Select the position information of circuits during Hamilton's fastest laps
# Interpreting 'position of the circuits' as their geographical position (location and coordinates)
answer = result[['name_circuit','location','country','lat','lng','name_race','year','date','fastestLapTime']].rename(columns={'name_circuit':'circuit_name','name_race':'race_name'})

target = answer

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
