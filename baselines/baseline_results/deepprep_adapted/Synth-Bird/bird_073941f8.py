import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="team_short_name", mode="mode")
    # MissingValueImputation
    table_1["team_short_name"] = table_1["team_short_name"].fillna(table_1["team_short_name"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['team_api_id', 'team_long_name', 'team_short_name'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['team_api_id', 'team_long_name', 'team_short_name'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['team_api_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['team_api_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['team_api_id', 'team_long_name', 'team_short_name'])
    # SelectCol
    _cols = [c for c in ['team_api_id', 'team_long_name', 'team_short_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="team_api_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['team_api_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['team_api_id']
    if _dtype == "datetime64":
        table_1['team_api_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['team_api_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['team_api_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['team_api_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     s = row.get('season', None)
    #     if s is None:
    #         return False
    #     s = str(s)
    #     return ('2016' in s) or (s.strip() == '2016')
    # """)
    # Filter
    def filter_func(row):
        s = row.get('season', None)
        if s is None:
            return False
        s = str(s)
        return ('2016' in s) or (s.strip() == '2016')
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
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
