import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'Club_ID', 'new_name': 'Attribute'}])
    # Rename
    table_1 = table_1.rename(columns={'Club_ID': 'Attribute'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['Attribute']).strip() == 'Name'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['Attribute']).strip() == 'Name'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Stack(table_name="table_1", id_vars=['Attribute'], value_vars=['1', '2', '3', '4', '5', '6', '7', '8', '9'], var_name="Club_ID", value_name="Club_Name")
    # Stack
    table_1 = table_1.melt(id_vars=['Attribute'], value_vars=['1', '2', '3', '4', '5', '6', '7', '8', '9'], var_name='Club_ID', value_name='Club_Name')
    table_1 = table_1.dropna(subset=['Club_Name'])

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Club_ID', 'Club_Name'])
    # SelectCol
    _cols = [c for c in ['Club_ID', 'Club_Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Club_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Club_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Club_ID']
    if _dtype == "datetime64":
        table_1['Club_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Club_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Club_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Club_ID'] = _series.astype(str)

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
    # DropNulls(table_name="table_1", subset=['Club_ID', 'Player_ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Club_ID', 'Player_ID'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Club_ID', 'Player_ID'])
    # SelectCol
    _cols = [c for c in ['Club_ID', 'Player_ID'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Club_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Club_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Club_ID']
    if _dtype == "datetime64":
        table_1['Club_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Club_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Club_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Club_ID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Player_ID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Player_ID'], keep='first').reset_index(drop=True)

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
