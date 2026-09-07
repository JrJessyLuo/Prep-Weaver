import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Conference_ID','Conference_Name','Year']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['conf_id','staff_ID','r']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_conferences = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_participation = prepared_table_2

target = prepared_conferences.merge(prepared_participation, left_on='Conference_ID', right_on='conf_id', how='left')
result = target.groupby(['Conference_Name','Year'], as_index=False)['staff_ID'].nunique().rename(columns={'staff_ID':'num_participants'})
result = result[['Conference_Name','Year','num_participants']]

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
