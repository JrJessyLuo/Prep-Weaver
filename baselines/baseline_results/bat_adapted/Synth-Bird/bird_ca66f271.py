import pandas as pd
import numpy as np

def _prep_1(table_1):
    majors = table_1[['major_id','major_name']].copy()
    majors = majors.dropna(subset=['major_id'])
    majors = majors.groupby('major_id', as_index=False).agg({'major_name':'first'})
    target = majors[['major_id','major_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['member_id','first_name','last_name','link_to_major']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_majors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_members = prepared_table_2

target = prepared_members.merge(prepared_majors, left_on='link_to_major', right_on='major_id', how='inner')
answer_rows = target[target['major_name'] == 'Law and Constitutional Studies']
result = answer_rows[['last_name']].drop_duplicates().sort_values(by='last_name').reset_index(drop=True)

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
