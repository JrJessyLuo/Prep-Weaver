import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
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
    # CastType(table_name="table_1", column="day", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['day'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['day']
    if _dtype == "datetime64":
        table_1['day'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['day'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['day'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['day'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="sid_bid", target_columns=['sid', 'bid'], func="""
    # def split(val):
    #     if val is None:
    #         return {"sid": None, "bid": None}
    #     s = str(val).strip()
    #     parts = s.split('_')
    #     if len(parts) != 2:
    #         return {"sid": None, "bid": None}
    #     return {"sid": parts[0].strip(), "bid": parts[1].strip()}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"sid": None, "bid": None}
        s = str(val).strip()
        parts = s.split('_')
        if len(parts) != 2:
            return {"sid": None, "bid": None}
        return {"sid": parts[0].strip(), "bid": parts[1].strip()}
    for _c in ['sid', 'bid']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['sid_bid']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['sid', 'bid']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['sid_bid'])

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['sid', 'bid', 'day'])
    # SelectCol
    _cols = [c for c in ['sid', 'bid', 'day'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_sailors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_reservations = prepared_table_2

# prepared_sailors: columns [sid]
# prepared_reservations: columns [sid, bid, day]
# Decompose sid_bid during preparation (example):
# prepared_reservations[['sid','bid']] = prepared_reservations['sid_bid'].str.split('_', expand=True)
# prepared_reservations['sid'] = prepared_reservations['sid'].astype(int)

# Find sailors who have not reserved any boat
reservers = prepared_reservations[['sid']].drop_duplicates()
result = prepared_sailors.merge(reservers, on='sid', how='left', indicator=True)
answer = result.loc[result['_merge'] == 'left_only', ['sid']]
answer = answer.sort_values('sid').reset_index(drop=True)
answer

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
