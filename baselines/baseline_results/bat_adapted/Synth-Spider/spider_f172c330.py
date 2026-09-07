import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Player_ID','First_part','Last_part']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import numpy as np
    target = table_1[['Player_ID','If_active_1','If_active_2','If_active_3','If_active_4']].copy()
    target[['If_active_1','If_active_2','If_active_3','If_active_4']] = target[['If_active_1','If_active_2','If_active_3','If_active_4']].replace(['nan','NaN','None',''], np.nan)
    target[['If_active_1','If_active_2','If_active_3','If_active_4']] = target[['If_active_1','If_active_2','If_active_3','If_active_4']].where(target[['If_active_1','If_active_2','If_active_3','If_active_4']].eq('T'), np.nan)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
players = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
player_activity_flags = prepared_table_2

prepared = players.merge(player_activity_flags, on='Player_ID', how='left')
active_cols = ['If_active_1','If_active_2','If_active_3','If_active_4']
# Treat 'T' as active; anything else (F or NaN) as not active
is_active = prepared[active_cols].eq('T').any(axis=1)
no_game = prepared.loc[~is_active]
# Build full name from parts, keeping names even if last part is missing or placeholder
no_game['Player_Name'] = no_game[['First_part','Last_part']].fillna('').agg(' '.join, axis=1).str.strip()
answer = no_game[['Player_Name']].drop_duplicates()

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
