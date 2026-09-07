import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['player_api_id','player_fifa_api_id','preferred_foot']].copy()
    prepared = prepared.dropna(subset=['player_api_id','player_fifa_api_id','preferred_foot'])
    prepared = prepared.drop_duplicates(subset=['player_api_id','player_fifa_api_id','preferred_foot'])
    target = prepared[['player_api_id','player_fifa_api_id','preferred_foot']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['player_api_id','player_fifa_api_id','weight']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_player_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_players = prepared_table_2

target = prepared_player_attributes.merge(prepared_players, on='player_api_id', how='inner')
# Ensure weight is numeric and filter under 130
if target['weight'].dtype == object:
    target['weight_numeric'] = pd.to_numeric(target['weight'], errors='coerce')
else:
    target['weight_numeric'] = target['weight']
filtered = target[target['weight_numeric'] < 130]
answer = (filtered['preferred_foot'].str.lower() == 'left').sum()

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
