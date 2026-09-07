import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['player_api_id', 'birthday'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['player_api_id', 'birthday'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="player_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["player_name"] = table_1["player_name"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="birthday", date_format="%Y-%m-%d")
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
    table_1['birthday'] = table_1['birthday'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['birthday'] = table_1['birthday'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['player_api_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['player_api_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['player_api_id', 'player_name', 'birthday'])
    # SelectCol
    _cols = [c for c in ['player_api_id', 'player_name', 'birthday'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    #     return row['mid'] is not None and row['date'] is not None and row['home_team_goal'] is not None
    # """)
    # Filter
    def filter_func(row):
        return row['mid'] is not None and row['date'] is not None and row['home_team_goal'] is not None
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="date", date_format="%Y-%m-%d")
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
    if '%Y-%m-%d':
        table_1['date'] = table_1['date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['mid', 'date', 'home_team_goal'])
    # SelectCol
    _cols = [c for c in ['mid', 'date', 'home_team_goal'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['mid'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['mid'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
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
prepared_players = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_matches = prepared_table_2

# There is no column in table_2 that links specific goal scorers to player_api_id from table_1 (only team-level goal counts exist).
# Therefore, we cannot attribute home team goals to players (and thus cannot filter by players aged <= 30) with the provided tables.
# If scorer-level data (e.g., goal events with player_api_id per goal) becomes available, then:
# 1) prepare that events table with columns ['mid', 'player_api_id', 'is_home', 'is_goal']
# 2) join events -> prepared_players on 'player_api_id' to filter age <= 30
# 3) sum is_goal where is_home == True to get total home team goals by those players.


# Placeholder result indicating insufficiency of data for the requested computation
result = pd.DataFrame({"error": ["Cannot compute: no scorer-to-player linkage in selected tables."]})

target = result

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
