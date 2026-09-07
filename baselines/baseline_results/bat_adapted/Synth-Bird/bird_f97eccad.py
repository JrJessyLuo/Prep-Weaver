import pandas as pd
import numpy as np

def _prep_1(table_1):
    drivers = table_1[['driverId','code','dob']].copy()
    drivers['dob'] = pd.to_datetime(drivers['dob'], errors='coerce')
    target = drivers[['driverId','code','dob']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['raceId','driverId','lap','milliseconds','time']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_8'])
prepared_lap_times = prepared_table_2

# Assume prepared_drivers and prepared_lap_times are dataframes produced per targets above
# 1) Filter drivers born in 1971
prepared_drivers['dob'] = pd.to_datetime(prepared_drivers['dob'], errors='coerce')
drivers_1971 = prepared_drivers[prepared_drivers['dob'].dt.year == 1971][['driverId','code']]

# 2) Join lap times to these drivers
lap_1971 = prepared_lap_times.merge(drivers_1971, on='driverId', how='inner')

# 3) For each race, find the minimum lap time (fastest lap) and the drivers who achieved it
race_min = lap_1971.groupby('raceId', as_index=False)['milliseconds'].min().rename(columns={'milliseconds':'min_ms'})
lap_with_min = lap_1971.merge(race_min, on='raceId', how='inner')
fastest_rows = lap_with_min[lap_with_min['milliseconds'] == lap_with_min['min_ms']]

# 4) Return unique drivers (id and code) among those who set the fastest lap in their race
answer = fastest_rows[['driverId','code']].drop_duplicates().sort_values(['driverId','code']).reset_index(drop=True)

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
