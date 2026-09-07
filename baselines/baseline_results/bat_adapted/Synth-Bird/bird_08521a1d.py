import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.loc[:, ['player_api_id', 'preferred_foot', 'date']].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['player_api_id', 'preferred_foot', 'date'])
    target = df[['player_api_id', 'preferred_foot', 'date']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['player_api_id','birthday']].copy()
    prepared['birthday'] = pd.to_datetime(prepared['birthday'], errors='coerce').dt.normalize()
    target = prepared[['player_api_id','birthday']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_player_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_players = prepared_table_2

# prepared_player_attributes and prepared_players are the synthesized per-table outputs
merged = prepared_player_attributes.merge(prepared_players, on='player_api_id', how='inner')

# Derive birth year
merged['birthday'] = pd.to_datetime(merged['birthday'], errors='coerce')
merged['birth_year'] = merged['birthday'].dt.year

# Filter birth year range
eligible = merged[(merged['birth_year'] >= 1987) & (merged['birth_year'] <= 1992)]

# If multiple attribute rows per player, reduce to one per player (e.g., most recent record)
eligible['date'] = pd.to_datetime(eligible['date'], errors='coerce')
eligible_sorted = eligible.sort_values(['player_api_id', 'date'], ascending=[True, False])
per_player = eligible_sorted.drop_duplicates(subset=['player_api_id'], keep='first')

# Compute percentage preferring left foot
denom = len(per_player)
if denom == 0:
    result = 0.0
else:
    num_left = (per_player['preferred_foot'].str.lower() == 'left').sum()
    result = 100.0 * num_left / denom

answer = result

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
