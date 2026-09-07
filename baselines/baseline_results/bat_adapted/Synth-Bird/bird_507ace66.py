import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['raceId','attribute','value']].copy()
    target['raceId'] = pd.to_numeric(target['raceId'], errors='coerce').astype('Int64')
    target['attribute'] = target['attribute'].astype('string')
    target['value'] = target['value'].astype('string')
    target = target.dropna(subset=['raceId','attribute'])
    target = target.drop_duplicates(subset=['raceId','attribute','value'])
    target = target.sort_values(['raceId','attribute','value'], kind='mergesort').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['raceId','driverId','statusId','positionText']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[:, ['statusId','status']].copy()
    target = target.dropna(subset=['statusId','status'])
    target['status'] = target['status'].astype(str).str.strip()
    target = target.drop_duplicates(subset=['statusId'], keep='first')
    target = target.sort_values(['statusId']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
races_long = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
results = prepared_table_2
prepared_table_3 = _prep_3(tables['table_13'])
status_lookup = prepared_table_3

# Assume races_long, results, status_lookup are the prepared tables.

# 1) Identify the raceId for the 2007 Bahrain Grand Prix from races_long.
# We expect attributes like 'year' == '2007' and 'name' containing 'Bahrain Grand Prix'.
races_2007 = races_long[(races_long['attribute'] == 'year') & (races_long['value'] == '2007')][['raceId']].drop_duplicates()

# Find raceIds whose name matches Bahrain Grand Prix
race_names = races_long[races_long['attribute'] == 'name'][['raceId','value']].rename(columns={'value':'race_name'})

candidate_races = races_2007.merge(race_names, on='raceId', how='inner')
bahrain_race_ids = candidate_races[candidate_races['race_name'].str.contains('Bahrain Grand Prix', case=False, na=False)]['raceId'].unique()

# 2) Join results and status to classify finishers vs non-finishers.
res = results[results['raceId'].isin(bahrain_race_ids)].merge(status_lookup, on='statusId', how='left')

# Define non-finishers: status != 'Finished'. (Covers Accident, Collision, Retired, Engine, etc.)
non_finishers = res[res['status'].fillna('') != 'Finished']

# 3) Count drivers who did not finish.
answer = len(non_finishers['driverId'].unique())

# Final output
target = pd.DataFrame({'non_finishers_count':[answer]})

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
