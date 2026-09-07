import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Game_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Game_ID'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Game_ID', 'Title'])
    # SelectCol
    _cols = [c for c in ['Game_ID', 'Title'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # CastType(table_name="table_1", column="Game_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Game_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Game_ID']
    if _dtype == "datetime64":
        table_1['Game_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Game_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Game_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Game_ID'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Player_ID", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # remove surrounding quotes (single/double) and whitespace
    #     s2 = str(s).strip()
    #     s2 = s2.replace('""', '"')
    #     s2 = s2.strip('"').strip("'").strip()
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # remove surrounding quotes (single/double) and whitespace
        s2 = str(s).strip()
        s2 = s2.replace('""', '"')
        s2 = s2.strip('"').strip("'").strip()
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Player_ID"] = table_1["Player_ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Player_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Player_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Player_ID']
    if _dtype == "datetime64":
        table_1['Player_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Player_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Player_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Player_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Player_ID', 'Game_ID', 'If_active'])
    # SelectCol
    _cols = [c for c in ['Player_ID', 'Game_ID', 'If_active'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Transpose(table_name="table_1")
    # Transpose
    if table_1.empty or len(table_1.columns) == 0:
        table_1 = table_1.transpose()
    else:
        _t = table_1.transpose()
        _newcols = _t.iloc[0].tolist()
        _t = _t.iloc[1:]
        _first = table_1.columns[0]
        _t.insert(0, _first, _t.index)
        _t.columns = [_first] + _newcols
        table_1 = _t.reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Player_ID', 'Player_name', 'Rank_of_the_year'])
    # SelectCol
    _cols = [c for c in ['Player_ID', 'Player_name', 'Rank_of_the_year'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Rank_of_the_year", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Rank_of_the_year'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Rank_of_the_year']
    if _dtype == "datetime64":
        table_1['Rank_of_the_year'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Rank_of_the_year'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Rank_of_the_year'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Rank_of_the_year'] = _series.astype(str)

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
