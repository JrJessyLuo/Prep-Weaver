import pandas as pd
import numpy as np

def _prep_1(table_1):
    source = table_1.copy()
    target = source[['player_api_id','player_fifa_api_id','date','overall_rating']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.rename(columns={'variable':'id','id':'variable'})[['id','variable','value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_player_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_player_lookup = prepared_table_2

# Assume prepared_player_attributes (attrs) and prepared_player_lookup (lookup) are available
attrs = prepared_player_attributes.copy()
lookup = prepared_player_lookup.copy()

# Identify Aaron Doran's player_api_id using lookup if it contains a name mapping.
# Common patterns in such long tables: id could be 'player_name' with value being the name,
# and variable holding the player_api_id or vice-versa. We'll try two robust options:

# Option A: rows where id == 'player_name' (or 'name') and value == 'Aaron Doran', then take variable as player_api_id
name_keys = lookup[lookup['id'].isin(['player_name','name']) & (lookup['value'].str.lower() == 'aaron doran')]
player_ids = pd.to_numeric(name_keys['variable'], errors='coerce').dropna().astype(int)

# Option B (fallback): rows where id is 'player_api_id' and variable corresponds to name entries
if player_ids.empty:
    name_rows = lookup[lookup['id'].isin(['player_name','name']) & (lookup['value'].str.lower() == 'aaron doran')]
    # If variable in name_rows links to another table key holding player_api_id, join within lookup
    # Try to find entries where variable matches lookup['variable'] and id == 'player_api_id'
    merged = name_rows.merge(lookup[lookup['id']=='player_api_id'], on='variable', suffixes=('_name',''))
    player_ids = pd.to_numeric(merged['value'], errors='coerce').dropna().astype(int)

# If still empty, attempt fifa id path similarly
if player_ids.empty:
    fifa_rows = lookup[lookup['id'].isin(['player_name','name']) & (lookup['value'].str.lower() == 'aaron doran')]
    merged_fifa = fifa_rows.merge(lookup[lookup['id'].isin(['player_fifa_api_id','fifa_api_id'])], on='variable', suffixes=('_name',''))
    fifa_ids = pd.to_numeric(merged_fifa['value'], errors='coerce').dropna().astype(int)
    if not fifa_ids.empty:
        # Map fifa_id to attrs via player_fifa_api_id
        target_rows = attrs[attrs['player_fifa_api_id'].isin(fifa_ids)]
        result_value = float(target_rows['overall_rating'].mean()) if not target_rows.empty else None
    else:
        result_value = None
else:
    target_rows = attrs[attrs['player_api_id'].isin(player_ids)]
    result_value = float(target_rows['overall_rating'].mean()) if not target_rows.empty else None

answer = {"average_overall_rating": result_value}

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
