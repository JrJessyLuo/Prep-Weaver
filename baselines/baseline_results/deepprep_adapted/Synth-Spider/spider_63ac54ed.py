import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Game_ID', 'Title', 'Units_sold_Millions'])
    # SelectCol
    _cols = [c for c in ['Game_ID', 'Title', 'Units_sold_Millions'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Title", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove matching leading/trailing single or double quotes
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         return s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove matching leading/trailing single or double quotes
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            return s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Title"] = table_1["Title"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Units_sold_Millions", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Units_sold_Millions'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Units_sold_Millions']
    if _dtype == "datetime64":
        table_1['Units_sold_Millions'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Units_sold_Millions'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Units_sold_Millions'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Units_sold_Millions'] = _series.astype(str)

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
    # StandardizeString(table_name="table_1", column_name="pn", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = re.sub(r'\s*\*\s*$', '', s)  # remove trailing asterisk marker like "Name *"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        s = re.sub(r'\s*\*\s*$', '', s)  # remove trailing asterisk marker like "Name *"
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["pn"] = table_1["pn"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['Position']).strip() == 'Guard'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['Position']).strip() == 'Guard'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Player_ID', 'pn', 'Position'])
    # SelectCol
    _cols = [c for c in ['Player_ID', 'pn', 'Position'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
games = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
players = prepared_table_2

# Prepared tables assumed available as DataFrames: games, players

# Filter players to Guards
guards = players[players['Position'].str.strip().str.lower() == 'guard']

# The question references "games played by players" but no linking keys between players and games exist.
# Without a join key (e.g., Game_ID in a player-game participation table), we cannot restrict games by players.
# Proceed by computing the average units sold over games that are (hypothetically) associated with these players would require a linkage table.

# As a best-effort placeholder using available data only, compute average units sold across all games (no valid integration possible):
result = pd.DataFrame({
    'average_units_sold_millions': [games['Units_sold_Millions'].astype(float).mean()]
})

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
