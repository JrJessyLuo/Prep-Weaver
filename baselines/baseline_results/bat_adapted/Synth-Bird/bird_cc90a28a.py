import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['player_api_id', 'overall_rating', 'date']].copy()
    prepared['date'] = pd.to_datetime(prepared['date'], errors='coerce')
    target = prepared.loc[:, ['player_api_id', 'overall_rating', 'date']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_player_attributes = prepared_table_1

# Single-table logic: find the player with the maximum overall_rating, then fetch their birthday from a players table if available.
# Since only attributes are provided here, we compute the player_api_id with the highest overall_rating.
max_rating = prepared_player_attributes['overall_rating'].max()
candidates = prepared_player_attributes[prepared_player_attributes['overall_rating'] == max_rating]
# If multiple snapshots exist for the same player, pick any (no sorting here per instructions)
player_id = candidates.iloc[0]['player_api_id']

# If a players bio table (e.g., prepared_players with columns ['player_api_id','birthday']) exists after separate preparation, join to get birthday
# Example (guarded):
try:
    target = prepared_players.merge(candidates[['player_api_id']].drop_duplicates(), on='player_api_id', how='inner')[['birthday']]
except NameError:
    # If no bio table available, raise to indicate missing integration input
    raise ValueError('Player birthday requires a players/bio table with birthday joined on player_api_id.')

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
