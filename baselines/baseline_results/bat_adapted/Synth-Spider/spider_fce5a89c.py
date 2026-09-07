import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['s_id','name','rtg']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['sid','bid','day']].copy()
    target['day'] = target['day'].astype(str).str.strip().str.replace(r'\s*/\s*', '/', regex=True)
    target = target[['sid','bid','day']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_sailors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_reservations = prepared_table_2

target = prepared_sailors.merge(prepared_reservations, left_on='s_id', right_on='sid', how='inner')
answer = target[target['rtg'] >= 3][['s_id','name']].drop_duplicates()

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
