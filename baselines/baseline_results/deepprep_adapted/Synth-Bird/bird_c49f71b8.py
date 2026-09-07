import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="team_fifa_api_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['team_fifa_api_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['team_fifa_api_id']
    if _dtype == "datetime64":
        table_1['team_fifa_api_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['team_fifa_api_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['team_fifa_api_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['team_fifa_api_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name'])
    # SelectCol
    _cols = [c for c in ['team_api_id', 'team_fifa_api_id', 'team_long_name', 'team_short_name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['team_api_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['team_api_id'], keep='last').reset_index(drop=True)

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
    # Filter(table_name="table_1", func="""
    # import pandas as pd
    # def filter_func(row: pd.Series) -> bool:
    #     return pd.notnull(row['team_api_id']) and pd.notnull(row['date'])
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return pd.notnull(row['team_api_id']) and pd.notnull(row['date'])
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
    # CastType(table_name="table_1", column="buildUpPlaySpeed", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['buildUpPlaySpeed'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['buildUpPlaySpeed']
    if _dtype == "datetime64":
        table_1['buildUpPlaySpeed'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['buildUpPlaySpeed'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['buildUpPlaySpeed'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['buildUpPlaySpeed'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['team_api_id', 'team_fifa_api_id', 'date', 'buildUpPlaySpeed'])
    # SelectCol
    _cols = [c for c in ['team_api_id', 'team_fifa_api_id', 'date', 'buildUpPlaySpeed'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_teams = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_team_attributes = prepared_table_2

merged = prepared_teams.merge(prepared_team_attributes, on='team_api_id', how='inner')
hearts = merged[merged['team_long_name'].str.lower() == 'heart of midlothian']
result = hearts['buildUpPlaySpeed'].astype('float').mean()
answer = float(result) if hearts.shape[0] > 0 else None

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
