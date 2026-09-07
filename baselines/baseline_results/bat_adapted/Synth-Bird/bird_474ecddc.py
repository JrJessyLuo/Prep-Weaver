import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['event_id','event_name','building','room','status']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['amount'] = df['amount'].astype(str).str.replace('"', '', regex=False)
    df['spent'] = pd.to_numeric(df['spent'], errors='coerce')
    df['remaining'] = pd.to_numeric(df['remaining'], errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    target = df[['link_to_event','spent','remaining','amount','event_status']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_events = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_budgets = prepared_table_2

target = prepared_events.merge(prepared_budgets, left_on='event_id', right_on='link_to_event', how='inner')
# underspend means spent < amount; amount is a quoted string, coerce to float
amt = pd.to_numeric(target['amount'].astype(str).str.replace('"',''), errors='coerce')
spent = pd.to_numeric(target['spent'], errors='coerce')
underspend_mask = (spent < amt)
result = target.loc[underspend_mask, ['event_name', 'building', 'room']]
result = result.rename(columns={'building':'location_building', 'room':'location_room'})

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
