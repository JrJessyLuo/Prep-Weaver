import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['ISBN'], ascending=[True])
    # Sort
    table_1 = table_1.sort_values(by=['ISBN'], ascending=[True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ISBN'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ISBN'], keep='last').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ISBN', 'Title'])
    # SelectCol
    _cols = [c for c in ['ISBN', 'Title'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="ISBN", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ISBN'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ISBN']
    if _dtype == "datetime64":
        table_1['ISBN'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ISBN'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ISBN'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ISBN'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ISBN', 'oid', 'amt'])
    # SelectCol
    _cols = [c for c in ['ISBN', 'oid', 'amt'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="oid", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['oid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['oid']
    if _dtype == "datetime64":
        table_1['oid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['oid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['oid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['oid'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="amt", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['amt'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['amt']
    if _dtype == "datetime64":
        table_1['amt'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['amt'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['amt'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['amt'] = _series.astype(str)

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
books_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
orders_prepared = prepared_table_2

target = books_prepared.merge(orders_prepared, on='ISBN', how='inner'); result = target.loc[target['Title'] == 'Pride and Prejudice']; answer = int(result['oid'].nunique())

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
