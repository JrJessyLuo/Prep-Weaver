import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['player_api_id','player_fifa_api_id','xm','weight']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['player_api_id','player_fifa_api_id','date']].copy()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    target = df[['player_api_id','player_fifa_api_id','date']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['country_id','name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
players = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
player_ratings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
leagues = prepared_table_3

# Assume prepared tables are provided as DataFrames: players, player_ratings, leagues
# 1) Join players to ratings to enable potential linkage to any country info (none available here), but primarily to deduplicate via player identity if multiple rows exist in ratings.
player_with_ratings = players.merge(player_ratings[['player_api_id']].drop_duplicates(), on='player_api_id', how='left')

# 2) Since no country column exists in any selected table and no reliable join key links players to a country/league table, we cannot compute country-level averages from the provided data.
# If a players->countries mapping existed (e.g., players.country or players.nationality or a team->league->country chain), we would group by that and compute mean weight.

# Placeholder to indicate insufficiency of data for the requested aggregation.
result = pd.DataFrame({
    'error': [
        'No country/nationality or team->league->country linkage available in the selected tables to compute average player weights by country.'
    ]
})

target = result

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
