import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['driverId','driverRef','forename','surname','nationality']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['raceId','year','name','date']].copy()
    target['date'] = pd.to_datetime(target['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['resultId','raceId','driverId','position','positionText','statusId','laps','points']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1.loc[:, ['statusId','status']].drop_duplicates().assign(statusId=lambda d: d['statusId'].astype('int64')).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_races = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_results = prepared_table_3
prepared_table_4 = _prep_4(tables['table_13'])
prepared_status = prepared_table_4

# Assume prepared_* DataFrames exist as per table_targets
merged = prepared_results.merge(prepared_drivers[['driverId','nationality']], on='driverId', how='inner')\
                     .merge(prepared_races[['raceId','year']], on='raceId', how='inner')\
                     .merge(prepared_status[['statusId','status']], on='statusId', how='left')

# Filter Japanese drivers and years 2007-2009
flt = (merged['nationality'].str.lower() == 'japanese') & (merged['year'].between(2007, 2009))
sub = merged.loc[flt].copy()

# Define completion: status == 'Finished' OR positionText is a digit (covers classified finishers)
finished_flag = (sub['status'].str.lower() == 'finished') | sub['positionText'].astype(str).str.fullmatch(r'\d+')

# Compute completion percentage across all their race starts in the period
num_starts = len(sub)
num_finished = int(finished_flag.sum())
completion_pct = (num_finished / num_starts * 100.0) if num_starts > 0 else float('nan')

result = pd.DataFrame({
    'metric': ['Japanese drivers completion % (2007-2009)'],
    'starts': [num_starts],
    'finishes': [num_finished],
    'completion_percentage': [completion_pct]
})

target = result

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
