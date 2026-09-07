import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="rtg", mode="mean")
    # MissingValueImputation
    table_1["rtg"] = table_1["rtg"].fillna(table_1["rtg"].mean())

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['s_id', 'name', 'rtg'])
    # SelectCol
    _cols = [c for c in ['s_id', 'name', 'rtg'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="sid", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['sid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['sid']
    if _dtype == "datetime64":
        table_1['sid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['sid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['sid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['sid'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="bid", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['bid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['bid']
    if _dtype == "datetime64":
        table_1['bid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['bid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['bid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['bid'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="day", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     # remove all whitespace and normalize quotes if present
    #     s = str(s).strip().strip('"').strip("'")
    #     s = re.sub(r'\s+', '', s)   # "9 /14" -> "9/14"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        # remove all whitespace and normalize quotes if present
        s = str(s).strip().strip('"').strip("'")
        s = re.sub(r'\s+', '', s)   # "9 /14" -> "9/14"
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["day"] = table_1["day"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['sid', 'bid', 'day'])
    # SelectCol
    _cols = [c for c in ['sid', 'bid', 'day'] if c in table_1.columns]
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
prepared_sailors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_reservations = prepared_table_2

target = prepared_sailors.merge(prepared_reservations, left_on='s_id', right_on='sid', how='inner')
answer = target[target['rtg'] >= 3][['s_id','name']].drop_duplicates()

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
