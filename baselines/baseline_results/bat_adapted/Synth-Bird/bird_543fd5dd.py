import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['raceId','year','name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['raceId','driverId','position','positionText','statusId']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_races = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_results = prepared_table_2

target = prepared_races.merge(prepared_results, on='raceId', how='inner')
# Filter to the 2008 Chinese Grand Prix
target_2008_china = target[(target['year'] == 2008) & (target['name'] == 'Chinese Grand Prix')]
# Finished drivers: positionText should be a numeric finish (not 'R','DNF','DSQ','N', etc). Use positionOrder/positionText proxy via position: non-null numeric means classified finish.
finished = target_2008_china[target_2008_china['position'].notna()]
# Count unique drivers who finished
answer = finished['driverId'].nunique()

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
