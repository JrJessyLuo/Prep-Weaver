import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Count(table_name="table_1")
    # Count -> statistic_table
    _stat_row = pd.DataFrame({'operator': ['Count(table_name="table_1")'], 'statistic_name': ['count'], 'value': [len(table_1)]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['customer_id'])
    # SelectCol
    _cols = [c for c in ['customer_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['customer_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['customer_id'], keep='first').reset_index(drop=True)

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
    # SelectCol(table_name="table_1", columns=['customer_id', 'order_id'])
    # SelectCol
    _cols = [c for c in ['customer_id', 'order_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="customer_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['customer_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['customer_id']
    if _dtype == "datetime64":
        table_1['customer_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['customer_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['customer_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['customer_id'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="order_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['order_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['order_id']
    if _dtype == "datetime64":
        table_1['order_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['order_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['order_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['order_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['customer_id', 'order_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['customer_id', 'order_id'], keep='first').reset_index(drop=True)

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
customers_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
orders_prepared = prepared_table_2

target = customers_prepared.merge(orders_prepared[['customer_id','order_id']].drop_duplicates(), on='customer_id', how='left', indicator=True)
answer = target.loc[target['order_id'].isna(), ['customer_id']].drop_duplicates().sort_values('customer_id')

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
