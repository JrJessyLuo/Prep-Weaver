import pandas as pd
import numpy as np

def _prep_1(table_1):
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
    # SelectCol(table_name="table_1", columns=['IdClient', 'Name'])
    # SelectCol
    _cols = [c for c in ['IdClient', 'Name'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="IdClient", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IdClient'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IdClient']
    if _dtype == "datetime64":
        table_1['IdClient'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IdClient'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IdClient'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IdClient'] = _series.astype(str)

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
    # CastType(table_name="table_1", column="IdOrder", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['IdOrder'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['IdOrder']
    if _dtype == "datetime64":
        table_1['IdOrder'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['IdOrder'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['IdOrder'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['IdOrder'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IdOrder', 'KH'])
    # SelectCol
    _cols = [c for c in ['IdOrder', 'KH'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'KH', 'new_name': 'IdClient'}])
    # Rename
    table_1 = table_1.rename(columns={'KH': 'IdClient'})

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IdOrder'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IdOrder'], keep='first').reset_index(drop=True)

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
    # GroupBy(table_name="table_1", by=['IdOrder'], agg=[{'column': 'amount', 'agg_func': 'sum'}])
    # GroupBy
    table_1 = table_1.groupby(['IdOrder'], as_index=False).agg({'amount': 'sum'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IdOrder'])
    # SelectCol
    _cols = [c for c in ['IdOrder'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IdOrder'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IdOrder'], keep='first').reset_index(drop=True)

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
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_orders = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_order_lines = prepared_table_3

# prepared_clients columns: IdClient (as string or int consistent with prepared_orders), Name
# prepared_orders columns: IdOrder, IdClient
# prepared_order_lines columns: IdOrder

# Optionally validate orders have at least one line; if not needed, skip this block
orders_with_lines = prepared_orders.merge(prepared_order_lines[['IdOrder']].drop_duplicates(), on='IdOrder', how='inner')

# Count orders per client
order_counts = orders_with_lines.groupby('IdClient', as_index=False).agg(OrderCount=('IdOrder', 'nunique'))

# Join client names
result = prepared_clients.merge(order_counts, on='IdClient', how='left')
result['OrderCount'] = result['OrderCount'].fillna(0).astype(int)

# Final projection: client name and number of orders
answer = result[['Name', 'OrderCount']]

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
