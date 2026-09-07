import pandas as pd
import numpy as np

def _prep_1(table_1):
    institutions = table_1[['Institution_ID','Name']].copy()
    institutions = institutions.dropna(subset=['Institution_ID'])
    institutions['Institution_ID'] = institutions['Institution_ID'].astype('int64')
    institutions = institutions.groupby('Institution_ID', as_index=False).agg({'Name':'first'})
    target = institutions[['Institution_ID','Name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Institution_ID','Nickname']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
institutions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
institution_nicknames = prepared_table_2

target = institutions.drop_duplicates(subset=['Institution_ID']).merge(institution_nicknames.drop_duplicates(subset=['Institution_ID','Nickname']), on='Institution_ID', how='inner')[['Name','Nickname']]

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
