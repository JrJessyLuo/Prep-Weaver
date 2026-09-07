import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="player_fifa_api_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['player_fifa_api_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['player_fifa_api_id']
    if _dtype == "datetime64":
        table_1['player_fifa_api_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['player_fifa_api_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['player_fifa_api_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['player_fifa_api_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d %H:%M:%S")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['date'] = table_1['date'].apply(_sd_parse)
    if '%Y-%m-%d %H:%M:%S':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['player_api_id', 'player_fifa_api_id', 'date'])
    # SelectCol
    _cols = [c for c in ['player_api_id', 'player_fifa_api_id', 'date'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['team_long_name'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['team_long_name'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['team_api_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['team_api_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name'])
    # SelectCol
    _cols = [c for c in ['team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
prepared_players = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_teams = prepared_table_2

# The selected tables do not contain match events or goals, nor player names needed to identify Daan Smith or Filipe Ferreira, nor any away-goal columns.
# Therefore, the sum of away team goals by those players cannot be computed from these tables alone.
# Expected additional tables/fields for a workable plan (not provided here):
# - A matches or events table with columns like match_id, away_team_api_id, away_player_X_name/id, away_goal_details or an events log with player_id and is_away flag or team_id per event.
# - A players table mapping player_api_id to player_name to locate Daan Smith and Filipe Ferreira.
# If such tables existed, a typical outline would be:
# players = prepared_players.merge(players_dim[['player_api_id','player_name']], on='player_api_id', how='right')
# events = match_events[(match_events['event_type']=='goal')]
# goals_with_team = events.merge(matches[['match_id','home_team_api_id','away_team_api_id']], on='match_id')
# goals_with_player = goals_with_team.merge(players_dim[['player_api_id','player_name']], on='player_api_id')
# target_players = goals_with_player[goals_with_player['player_name'].isin(['Daan Smith','Filipe Ferreira'])]
# away_goals = target_players[target_players['team_api_id']==target_players['away_team_api_id']]
# answer = away_goals.shape[0]
# print(answer)

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
