import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="invoice_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes like ""1"" or "1"
    #     if (s.startswith('""') and s.endswith('""') and len(s) >= 4):
    #         s = s[2:-2]
    #     if (s.startswith('"') and s.endswith('"') and len(s) >= 2):
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes like ""1"" or "1"
        if (s.startswith('""') and s.endswith('""') and len(s) >= 4):
            s = s[2:-2]
        if (s.startswith('"') and s.endswith('"') and len(s) >= 2):
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["invoice_id"] = table_1["invoice_id"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['invoice_id'])
    # SelectCol
    _cols = [c for c in ['invoice_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     v = row[\"invoice_id\"]
    #     if v is None:
    #         return False
    #     v = str(v).strip()
    #     return v != \"\" and v.lower() != \"nan\"
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        v = row[\"invoice_id\"]
        if v is None:
            return False
        v = str(v).strip()
        return v != \"\" and v.lower() != \"nan\"
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['invoice_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['invoice_id'], keep='first').reset_index(drop=True)

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="value", func="""
    # def is_valid_value(val):
    #     if val is None:
    #         return False
    #     s = str(val)
    #     left, sep, right = s.partition('-')
    #     return bool(sep) and left.strip() != '' and right.strip() != ''
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_value(val):
        if val is None:
            return False
        s = str(val)
        left, sep, right = s.partition('-')
        return bool(sep) and left.strip() != '' and right.strip() != ''
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_value(val))
        except Exception:
            return False
    table_1 = table_1[table_1['value'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['column']).strip().strip('\"').strip(\"'\") == 'invoice_payment'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['column']).strip().strip('\"').strip(\"'\") == 'invoice_payment'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="value", target_columns=['invoice_id', 'payment_status'], func="""
    # def split(val):
    #     if val is None:
    #         return {"invoice_id": None, "payment_status": None}
    #     s = str(val)
    #     left, sep, right = s.partition('-')  # first '-' only
    #     return {"invoice_id": left.strip(), "payment_status": right.strip()}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"invoice_id": None, "payment_status": None}
        s = str(val)
        left, sep, right = s.partition('-')  # first '-' only
        return {"invoice_id": left.strip(), "payment_status": right.strip()}
    for _c in ['invoice_id', 'payment_status']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['value']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['invoice_id', 'payment_status']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['value'])

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="invoice_id", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['invoice_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['invoice_id']
    if _dtype == "datetime64":
        table_1['invoice_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['invoice_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['invoice_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['invoice_id'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['invoice_id', 'payment_status'])
    # SelectCol
    _cols = [c for c in ['invoice_id', 'payment_status'] if c in table_1.columns]
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
prepared_invoices = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_payments = prepared_table_2

# prepared_invoices: columns -> ['invoice_id']
# prepared_payments: columns -> ['invoice_id','payment_status']

# Join invoices to payments on invoice_id
joined = prepared_invoices.merge(prepared_payments, on='invoice_id', how='inner')

# Select distinct invoice ids and payment statuses
result = joined[['invoice_id','payment_status']].drop_duplicates()

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
