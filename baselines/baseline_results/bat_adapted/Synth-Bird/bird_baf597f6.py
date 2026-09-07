import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['raceId','year','name','date']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.loc[:, ['raceId', 'driverId']]
    prepared = prepared.drop_duplicates(subset=['raceId', 'driverId'])
    target = prepared[['raceId', 'driverId']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['driverId','gj']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_races = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_results = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_drivers = prepared_table_3

# Assume prepared_races, prepared_results, prepared_drivers are dataframes created from the respective table_targets.

# 1) Locate the 2008 Australian Grand Prix raceId
race_mask = (prepared_races['year'] == 2008) & (prepared_races['name'] == 'Australian Grand Prix')
selected_races = prepared_races.loc[race_mask, ['raceId']].drop_duplicates()

# 2) Get participating drivers for that race
res = prepared_results.merge(selected_races, on='raceId', how='inner')

# 3) Join driver nationalities
res = res.merge(prepared_drivers, on='driverId', how='left')

# 4) Filter drivers from the UN and count unique drivers
# Note: Interpret 'from the UN' as nationality exactly equal to 'UN' in column 'gj'.
count = res.loc[res['gj'] == 'UN', 'driverId'].nunique()

answer = int(count)

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
