import pandas as pd
import numpy as np

def _prep_1(table_1):
    name_row = table_1.loc[table_1['Club_ID'].eq('Name')].iloc[0]
    wide = name_row.drop(labels=['Club_ID'])
    target = wide.reset_index()
    target.columns = ['Club_ID','Club_Name']
    target['Club_ID'] = target['Club_ID'].astype(str)
    target = target[['Club_ID','Club_Name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['Club_ID','Player_ID']].copy()
    df['Club_ID'] = pd.to_numeric(df['Club_ID'], errors='coerce').astype('Int64')
    df['Player_ID'] = pd.to_numeric(df['Player_ID'], errors='coerce').astype('Int64')
    target = df[['Club_ID','Player_ID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_clubs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_players = prepared_table_2

clubs = prepared_clubs.copy()
players = prepared_players.copy()
# Ensure Club_ID types align
clubs['Club_ID'] = clubs['Club_ID'].astype(str)
players['Club_ID'] = players['Club_ID'].astype(str)
# Left join to find clubs without any matching players
merged = clubs.merge(players[['Club_ID','Player_ID']], on='Club_ID', how='left')
no_player_clubs = merged[merged['Player_ID'].isna()]
answer = no_player_clubs[['Club_Name']].drop_duplicates().rename(columns={'Club_Name': 'Club'})

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
