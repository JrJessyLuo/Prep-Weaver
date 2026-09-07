import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['team_api_id','team_long_name','team_short_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.set_index('id').T
    df = df.rename_axis(None, axis=0).reset_index(drop=True)
    target = df[['season','home_team_api_id','away_team_api_id','home_team_goal','away_team_goal']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_teams = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_matches = prepared_table_2

# prepared_teams: columns ['team_api_id','team_long_name','team_short_name']
# prepared_matches: columns ['season','home_team_api_id','away_team_api_id','home_team_goal','away_team_goal']

# 1) Filter to the 2016 season (string formats may vary like '2016/2017' or '2016')
season_mask = prepared_matches['season'].astype(str).str.contains('2016')
matches_2016 = prepared_matches.loc[season_mask].copy()

# 2) Determine home losses
matches_2016['home_loss'] = (matches_2016['home_team_goal'] < matches_2016['away_team_goal']).astype(int)

# 3) Aggregate losses by home team
home_losses = (
    matches_2016.groupby('home_team_api_id', as_index=False)['home_loss']
    .sum()
    .rename(columns={'home_loss':'home_losses_2016'})
)

# 4) Join to team names
result = home_losses.merge(prepared_teams, left_on='home_team_api_id', right_on='team_api_id', how='left')

# 5) Find the fewest home losses and corresponding team(s)
min_losses = result['home_losses_2016'].min()
answer_rows = result[result['home_losses_2016'] == min_losses][['team_long_name','home_losses_2016']]

# 'answer_rows' contains the home team(s) with the fewest home losses in 2016 and the loss count.

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
