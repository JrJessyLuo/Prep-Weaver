import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['player_api_id','player_name','birthday']].copy()
    target['birthday'] = pd.to_datetime(target['birthday'], errors='coerce')
    target = target[['player_api_id','player_name','birthday']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['mid','date','home_team_goal']].copy()
    prepared = prepared.drop_duplicates(subset=['mid'])
    target = prepared[['mid','date','home_team_goal']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_players = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_matches = prepared_table_2

# There is no column in table_2 that links specific goal scorers to player_api_id from table_1 (only team-level goal counts exist).
# Therefore, we cannot attribute home team goals to players (and thus cannot filter by players aged <= 30) with the provided tables.
# If scorer-level data (e.g., goal events with player_api_id per goal) becomes available, then:
# 1) prepare that events table with columns ['mid', 'player_api_id', 'is_home', 'is_goal']
# 2) join events -> prepared_players on 'player_api_id' to filter age <= 30
# 3) sum is_goal where is_home == True to get total home team goals by those players.


# Placeholder result indicating insufficiency of data for the requested computation
result = pd.DataFrame({"error": ["Cannot compute: no scorer-to-player linkage in selected tables."]})

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
