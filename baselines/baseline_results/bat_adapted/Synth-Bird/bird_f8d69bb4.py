import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['match_api_id','away_team_api_id','away_team_goal']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['team_api_id','team_long_name']].drop_duplicates(subset=['team_api_id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_matches = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_teams = prepared_table_2

# prepared_matches: columns [match_api_id, away_team_api_id, away_team_goal]
# prepared_teams:   columns [team_api_id, team_long_name]

# Join matches to teams on away team id
joined = prepared_matches.merge(prepared_teams, left_on='away_team_api_id', right_on='team_api_id', how='left')

# Aggregate total away goals by team long name
agg = joined.groupby(['away_team_api_id', 'team_long_name'], as_index=False)['away_team_goal'].sum()

# Find the team with the maximum total away goals
max_goals = agg['away_team_goal'].max()
result = agg.loc[agg['away_team_goal'] == max_goals, ['team_long_name']]

# If multiple teams tie, return all their full names (unique)
answer = result['team_long_name'].dropna().unique().tolist()

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
