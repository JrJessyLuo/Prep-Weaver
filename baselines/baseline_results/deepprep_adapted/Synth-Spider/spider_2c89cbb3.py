import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Item", mode="mode")
    # MissingValueImputation
    table_1["Item"] = table_1["Item"].fillna(table_1["Item"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Item", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    # 
    #     # normalize dash variants to a simple hyphen
    #     s = s.replace('—', '-').replace('–', '-').replace('−', '-')
    # 
    #     # normalize spacing around hyphens: "90 - APIE - 10"
    #     s = re.sub(r'\s*-\s*', '-', s)           # first collapse to no-space hyphens
    #     s = re.sub(r'-', '-', s)                   # (kept for clarity)
    #     s = re.sub(r'\s+', ' ', s).strip()        # collapse multiple spaces
    # 
    #     # keep canonical display with single hyphen separators (no extra spaces)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if (len(s) >= 2) and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()

        # normalize dash variants to a simple hyphen
        s = s.replace('—', '-').replace('–', '-').replace('−', '-')

        # normalize spacing around hyphens: "90 - APIE - 10"
        s = re.sub(r'\s*-\s*', '-', s)           # first collapse to no-space hyphens
        s = re.sub(r'-', '-', s)                   # (kept for clarity)
        s = re.sub(r'\s+', ' ', s).strip()        # collapse multiple spaces

        # keep canonical display with single hyphen separators (no extra spaces)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Item"] = table_1["Item"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Receipt", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Receipt'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Receipt']
    if _dtype == "datetime64":
        table_1['Receipt'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Receipt'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Receipt'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Receipt'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Ordinal", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Ordinal'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Ordinal']
    if _dtype == "datetime64":
        table_1['Ordinal'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Ordinal'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Ordinal'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Ordinal'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Receipt', 'Ordinal', 'Item'])
    # SelectCol
    _cols = [c for c in ['Receipt', 'Ordinal', 'Item'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['Receipt', 'Ordinal'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['Receipt', 'Ordinal'], ascending=[True, True])

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['Receipt', 'Ordinal', 'Item'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['Receipt', 'Ordinal', 'Item'], keep='first').reset_index(drop=True)

    # ---------------- Step 8 ----------------
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
    # SelectCol(table_name="table_1", columns=['sjb', 'khid'])
    # SelectCol
    _cols = [c for c in ['sjb', 'khid'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['sjb', 'khid'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['sjb', 'khid'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="sjb", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['sjb'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['sjb']
    if _dtype == "datetime64":
        table_1['sjb'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['sjb'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['sjb'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['sjb'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="khid", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['khid'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['khid']
    if _dtype == "datetime64":
        table_1['khid'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['khid'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['khid'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['khid'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['sjb'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['sjb'], keep='last').reset_index(drop=True)

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
prepared_receipt_items = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sales_headers = prepared_table_2

target = prepared_sales_headers.merge(prepared_receipt_items, left_on='sjb', right_on='Receipt', how='inner')
# Filter for the requested customer id
customer_items = target[target['khid'] == 15]
# Get distinct items bought by this customer
answer = sorted(customer_items['Item'].dropna().unique().tolist())

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
