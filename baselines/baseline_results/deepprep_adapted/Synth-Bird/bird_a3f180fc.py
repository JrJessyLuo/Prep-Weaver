import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['client_id', 'district_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['client_id', 'district_id'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'district_id'])
    # SelectCol
    _cols = [c for c in ['client_id', 'district_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="client_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['client_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['client_id']
    if _dtype == "datetime64":
        table_1['client_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['client_id'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="district_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['district_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['district_id']
    if _dtype == "datetime64":
        table_1['district_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['district_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['district_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['district_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['client_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['client_id'], keep='last').reset_index(drop=True)

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
    # ErrorDetection(table_name="table_1", column_name="attribute", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     v = str(val).strip().strip('"').strip("'").lower()
    #     return len(v) > 0
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        v = str(val).strip().strip('"').strip("'").lower()
        return len(v) > 0
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['attribute'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="attribute", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     # remove wrapping quotes
    #     v = re.sub(r'^("|')|("|')$', '', v)
    #     v = v.strip().lower()
    #     return v if v != '' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        # remove wrapping quotes
        v = re.sub(r'^("|')|("|')$', '', v)
        v = v.strip().lower()
        return v if v != '' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["attribute"] = table_1["attribute"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="value", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip()
    #     # remove wrapping quotes
    #     v = re.sub(r'^("|')|("|')$', '', v)
    #     v = v.strip().upper()
    #     return v if v != '' else None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip()
        # remove wrapping quotes
        v = re.sub(r'^("|')|("|')$', '', v)
        v = v.strip().upper()
        return v if v != '' else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["value"] = table_1["value"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="client_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['client_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['client_id']
    if _dtype == "datetime64":
        table_1['client_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['client_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['client_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="account_id", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['account_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['account_id']
    if _dtype == "datetime64":
        table_1['account_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['account_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['account_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['account_id'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['client_id', 'account_id', 'attribute', 'value'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['client_id', 'account_id', 'attribute', 'value'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['client_id', 'account_id', 'attribute', 'value'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['client_id', 'account_id', 'attribute', 'value'], keep='first').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['client_id', 'account_id', 'attribute', 'value'])
    # SelectCol
    _cols = [c for c in ['client_id', 'account_id', 'attribute', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 9 ----------------
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
    # StandardizeString(table_name="table_1", column_name="k_symbol", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s if s != "" else None
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        return s if s != "" else None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["k_symbol"] = table_1["k_symbol"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['k_symbol'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['k_symbol'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'k_symbol'])
    # SelectCol
    _cols = [c for c in ['account_id', 'k_symbol'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['account_id', 'k_symbol'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['account_id', 'k_symbol'], keep='first').reset_index(drop=True)

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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['account_id', 'loan_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['account_id', 'loan_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['account_id', 'loan_id'])
    # SelectCol
    _cols = [c for c in ['account_id', 'loan_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['account_id', 'loan_id'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['account_id', 'loan_id'], how='any').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_5'])
clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
dispositions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
orders = prepared_table_3
prepared_table_4 = _prep_4(tables['table_6'])
loans = prepared_table_4

# Start from prepared tables
clients = clients[['client_id','district_id']].drop_duplicates()
dispositions = dispositions[['client_id','account_id','attribute','value']].drop_duplicates()
orders = orders[['account_id','k_symbol']].drop_duplicates()
loans = loans[['account_id','loan_id']].drop_duplicates()

# Determine capabilities per client via accounts they are allowed to act on
# Right to issue permanent orders: evidence of any order on an account the client is linked to
has_order = dispositions.merge(orders, on='account_id', how='left')
has_order['can_orders'] = has_order['k_symbol'].notna()
can_orders = has_order.groupby('client_id', as_index=False)['can_orders'].max()

# Right to apply for loans: evidence of any loan on an account the client is linked to
has_loan = dispositions.merge(loans, on='account_id', how='left')
has_loan['can_loans'] = has_loan['loan_id'].notna()
can_loans = has_loan.groupby('client_id', as_index=False)['can_loans'].max()

# Combine capability flags
caps = clients[['client_id']].merge(can_orders, on='client_id', how='left').merge(can_loans, on='client_id', how='left')
caps['can_orders'] = caps['can_orders'].fillna(False)
caps['can_loans'] = caps['can_loans'].fillna(False)

# Clients that can only have the right to issue permanent orders or apply for loans
# Interpret as: can perform exactly one of the two capabilities (XOR)
only_one = caps[(caps['can_orders'] ^ caps['can_loans'])]

# Return client_id and district
result = only_one.merge(clients[['client_id','district_id']], on='client_id', how='left')[['client_id','district_id']].drop_duplicates().sort_values(['client_id'])

target = result

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
