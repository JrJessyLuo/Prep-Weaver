import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['circuitId', 'circuitRef', 'name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['raceId','circuitId','name','date','time']].copy()
    df['raceId'] = df['raceId'].astype(str).str.strip().str.strip('"').astype('int64')
    df['circuitId'] = pd.to_numeric(df['circuitId'], errors='coerce').astype('int64')
    df['date'] = pd.to_datetime(df['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['time'] = pd.to_datetime(df['time'], format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M:%S')
    target = df[['raceId','circuitId','name','date','time']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_circuits = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_races = prepared_table_2

target = prepared_races.merge(prepared_circuits, on='circuitId', how='inner')
ans = target[(target['name_y'] == 'Sepang International Circuit') | (target['circuitRef'] == 'sepang')]
result = ans[['date', 'time']].dropna(subset=['time']).drop_duplicates().sort_values(['date', 'time'])

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
