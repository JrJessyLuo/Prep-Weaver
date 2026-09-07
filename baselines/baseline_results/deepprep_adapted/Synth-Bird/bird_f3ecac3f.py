import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TransactionID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TransactionID'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TransactionID', 'CustomerID', 'ProductID'])
    # SelectCol
    _cols = [c for c in ['TransactionID', 'CustomerID', 'ProductID'] if c in table_1.columns]
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
    # Rename(table_name="table_1", rename_map=[{'old_name': 'ProductID', 'new_name': 'ProductID'}, {'old_name': 'Description', 'new_name': 'Description'}])
    # Rename
    table_1 = table_1.rename(columns={'ProductID': 'ProductID', 'Description': 'Description'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ProductID", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes like ""1"" or "1"
    #     s = re.sub(r'^("+)(.*?)("+)$', r'\2', s)
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes like ""1"" or "1"
        s = re.sub(r'^("+)(.*?)("+)$', r'\2', s)
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ProductID"] = table_1["ProductID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ProductID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ProductID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ProductID']
    if _dtype == "datetime64":
        table_1['ProductID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ProductID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ProductID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ProductID'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Description", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Description"] = table_1["Description"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ProductID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ProductID'], keep='first').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ProductID', 'Description'])
    # SelectCol
    _cols = [c for c in ['ProductID', 'Description'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['CustomerID'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['CustomerID'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="CustomerID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['CustomerID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['CustomerID']
    if _dtype == "datetime64":
        table_1['CustomerID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['CustomerID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['CustomerID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="huobi", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().upper()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().upper()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["huobi"] = table_1["huobi"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['CustomerID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['CustomerID'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['CustomerID', 'huobi'])
    # SelectCol
    _cols = [c for c in ['CustomerID', 'huobi'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_3'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_products = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_customers = prepared_table_3

target = prepared_transactions.merge(prepared_customers, on='CustomerID', how='left').merge(prepared_products, on='ProductID', how='left'); euro = target[target['huobi'].astype(str).str.upper().str.strip()=='EUR']; result = euro[['Description']].dropna().drop_duplicates().reset_index(drop=True)

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
