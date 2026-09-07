import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'year', 'name'])
    # SelectCol
    _cols = [c for c in ['raceId', 'year', 'name'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="driverId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['driverId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['driverId']
    if _dtype == "datetime64":
        table_1['driverId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['driverId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['driverId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['driverId'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="raceId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['raceId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['raceId']
    if _dtype == "datetime64":
        table_1['raceId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['raceId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['raceId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['raceId'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="statusId", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['statusId'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['statusId']
    if _dtype == "datetime64":
        table_1['statusId'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['statusId'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['statusId'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['statusId'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="position", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['position'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['position']
    if _dtype == "datetime64":
        table_1['position'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['position'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['position'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['position'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="positionText", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding single/double quotes if present
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
    table_1["positionText"] = table_1["positionText"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['raceId', 'driverId', 'position', 'positionText', 'statusId'])
    # SelectCol
    _cols = [c for c in ['raceId', 'driverId', 'position', 'positionText', 'statusId'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
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
prepared_races = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_results = prepared_table_2

target = prepared_races.merge(prepared_results, on='raceId', how='inner')
# Filter to the 2008 Chinese Grand Prix
target_2008_china = target[(target['year'] == 2008) & (target['name'] == 'Chinese Grand Prix')]
# Finished drivers: positionText should be a numeric finish (not 'R','DNF','DSQ','N', etc). Use positionOrder/positionText proxy via position: non-null numeric means classified finish.
finished = target_2008_china[target_2008_china['position'].notna()]
# Count unique drivers who finished
answer = finished['driverId'].nunique()

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
