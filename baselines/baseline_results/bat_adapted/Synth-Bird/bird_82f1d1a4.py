import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.assign(id=table_1['id'].astype('int64'), name=table_1['name'].astype('string').str.strip()).drop_duplicates(subset=['id']).sort_values(['id']).reset_index(drop=True)[['id','name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df_long = table_1.melt(id_vars=['id'], var_name='league_col', value_name='value')
    df_wide = df_long.pivot(index='league_col', columns='id', values='value').reset_index()
    df_wide = df_wide.rename(columns={'league_col': 'league_id', 'league_id': 'draws'})
    df_wide['league_id'] = pd.to_numeric(df_wide['league_id'], errors='coerce')
    df_wide['draws'] = pd.to_numeric(df_wide['draws'], errors='coerce')
    target = df_wide[['league_id', 'season', 'draws']].dropna(subset=['league_id', 'season'])
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
countries = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
league_season_stats = prepared_table_2

# prepared inputs: league_season_stats with columns [league_id, season, draws]
# We only need league_season_stats for answering; countries are not needed unless mapping to names is available elsewhere.

# Filter to 2016 season variants. The sample shows seasons like '2015/2016'. We interpret '2016 season' as the 2015/2016 season.
target_season = '2015/2016'
ls_2016 = league_season_stats[league_season_stats['season'] == target_season]

# Find league with maximum draws
idx = ls_2016['draws'].astype(float).idxmax()
max_row = ls_2016.loc[idx]

# If a league name mapping exists elsewhere, map here. With current selected tables, only country names are available, so we return the league_id as the league identifier.
answer = max_row['league_id']

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
