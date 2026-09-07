import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Game_ID','Title']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['Player_ID','Game_ID','If_active']].copy()
    target['Player_ID'] = target['Player_ID'].astype(str).str.strip().str.strip('"').str.strip("'")
    target['Game_ID'] = pd.to_numeric(target['Game_ID'], errors='coerce').astype('Int64')
    target['If_active'] = target['If_active'].astype(str).str.strip().str.upper()
    target = target.dropna(subset=['Player_ID','Game_ID','If_active']).drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df_long = table_1.melt(id_vars=['Player_ID'], var_name='Player_ID_out', value_name='value')
    df_wide = df_long.pivot(index='Player_ID_out', columns='Player_ID', values='value').reset_index()
    df_wide = df_wide.rename(columns={'Player_ID_out': 'Player_ID'})
    target = df_wide[['Player_ID', 'Player_name', 'Rank_of_the_year']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_games = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_player_games = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_players = prepared_table_3

# prepared_games: ['Game_ID','Title'] from table_1
pg = prepared_games.copy()
# prepared_player_games: ['Player_ID','Game_ID','If_active'] from table_2
ppg = prepared_player_games.copy()
# prepared_players: ['Player_ID','Player_name','Rank_of_the_year'] from table_3 (normalized beforehand)
players = prepared_players.copy()

# Integrate
g_pg = ppg.merge(pg, on='Game_ID', how='inner')
full = g_pg.merge(players, on='Player_ID', how='inner')

# Question-specific filtering: title == 'Super Mario World'
result = full[full['Title'] == 'Super Mario World'][['Player_name', 'Rank_of_the_year']].drop_duplicates()

# Final answer dataframe in variable `result`

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
