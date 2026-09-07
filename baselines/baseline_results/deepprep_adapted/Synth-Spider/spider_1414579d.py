import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['customer_number'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['customer_number'], keep='last').reset_index(drop=True)

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
    # CastType(table_name="table_1", column="customer_number", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['customer_number'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['customer_number']
    if _dtype == "datetime64":
        table_1['customer_number'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['customer_number'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['customer_number'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['customer_number'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="customer_name", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping single/double quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping single/double quotes if present
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
    table_1["customer_name"] = table_1["customer_name"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['customer_id', 'customer_number', 'customer_name'])
    # SelectCol
    _cols = [c for c in ['customer_id', 'customer_number', 'customer_name'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['order_id', 'customer_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['order_id', 'customer_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['order_id', 'customer_id'])
    # SelectCol
    _cols = [c for c in ['order_id', 'customer_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['order_id', 'customer_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['order_id', 'customer_id'], how='any').reset_index(drop=True)

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
prepared_customers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_orders = prepared_table_2

integrated = prepared_customers.merge(prepared_orders, how='left', left_on='customer_id', right_on='customer_id'); target = (integrated['order_id'].isna()).sum()

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
