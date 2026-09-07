import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.copy()
    target['raceId'] = target['raceId'].astype(str).str.replace('"', '', regex=False).astype('int64')
    target['year'] = pd.to_numeric(target['year'], errors='coerce').astype('int64')
    target['round'] = pd.to_numeric(target['round'], errors='coerce').astype('int64')
    target['circuitId'] = pd.to_numeric(target['circuitId'], errors='coerce').astype('int64')
    target['date'] = pd.to_datetime(target['date'], errors='coerce').dt.date
    target['time'] = pd.to_datetime(target['time'], format='%H:%M:%S', errors='coerce').dt.time
    target = target[['raceId','year','round','circuitId','name','date','time','url']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['circuitId','circuitRef','name','location','country','lat','lng','url']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_races = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_circuits = prepared_table_2

target = prepared_races.merge(prepared_circuits, on='circuitId', how='inner')
answer_rows = target[target['name_x'].str.lower().str.contains('malaysian grand prix')][['location', 'country', 'lat', 'lng']].drop_duplicates()

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
