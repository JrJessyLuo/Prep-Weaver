import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['team_api_id','team_fifa_api_id','team_long_name','team_short_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['team_api_id','team_fifa_api_id','date','buildUpPlaySpeed']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_teams = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_team_attributes = prepared_table_2

merged = prepared_teams.merge(prepared_team_attributes, on='team_api_id', how='inner')
hearts = merged[merged['team_long_name'].str.lower() == 'heart of midlothian']
result = hearts['buildUpPlaySpeed'].astype('float').mean()
answer = float(result) if hearts.shape[0] > 0 else None

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
