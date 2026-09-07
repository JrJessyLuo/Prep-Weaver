import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Contents", mode="mode")
    # MissingValueImputation
    table_1["Contents"] = table_1["Contents"].fillna(table_1["Contents"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Contents", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove wrapping quotes if present
    #     if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
    #         s = s[1:-1].strip()
    #     # normalize common placeholder variants
    #     if re.fullmatch(r'undeclared|un-declared|not\s*declared|unknown', s.strip(), flags=re.IGNORECASE):
    #         return "Undeclared"
    #     # collapse internal whitespace
    #     s = re.sub(r'\s+', ' ', s).strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove wrapping quotes if present
        if (len(s) >= 2) and ((s[0] == s[-1]) and s[0] in ['"', "'"]):
            s = s[1:-1].strip()
        # normalize common placeholder variants
        if re.fullmatch(r'undeclared|un-declared|not\s*declared|unknown', s.strip(), flags=re.IGNORECASE):
            return "Undeclared"
        # collapse internal whitespace
        s = re.sub(r'\s+', ' ', s).strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Contents"] = table_1["Contents"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Shipment", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Shipment'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Shipment']
    if _dtype == "datetime64":
        table_1['Shipment'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Shipment'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Shipment'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Shipment'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BaoZhuangHao", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BaoZhuangHao'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BaoZhuangHao']
    if _dtype == "datetime64":
        table_1['BaoZhuangHao'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BaoZhuangHao'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BaoZhuangHao'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BaoZhuangHao'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FaSongRen", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FaSongRen'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FaSongRen']
    if _dtype == "datetime64":
        table_1['FaSongRen'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FaSongRen'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FaSongRen'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FaSongRen'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ShouHuoRen", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ShouHuoRen'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ShouHuoRen']
    if _dtype == "datetime64":
        table_1['ShouHuoRen'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ShouHuoRen'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ShouHuoRen'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ShouHuoRen'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Weight", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Weight'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Weight']
    if _dtype == "datetime64":
        table_1['Weight'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Weight'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Weight'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Weight'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['Shipment', 'BaoZhuangHao', 'Contents', 'Weight', 'FaSongRen', 'ShouHuoRen'])
    # SelectCol
    _cols = [c for c in ['Shipment', 'BaoZhuangHao', 'Contents', 'Weight', 'FaSongRen', 'ShouHuoRen'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_shipments = prepared_table_1

target = prepared_shipments
# Map sender names if available; here we infer 'John Zoidfarb' corresponds to sender ID values where name mapping is external.
# If a name-to-ID map is not provided, attempt exact match on a 'sender_name' column if present.
if 'sender_name' in target.columns:
    answer_rows = target[target['sender_name'].str.lower() == 'john zoidfarb']
else:
    # Fallback heuristic: if question implies a specific sender ID mapping is known elsewhere, replace 'john_zoidfarb_id' accordingly.
    john_zoidfarb_id = None  # set by upstream name resolution if available
    if john_zoidfarb_id is not None and 'FaSongRen' in target.columns:
        answer_rows = target[target['FaSongRen'] == john_zoidfarb_id]
    else:
        # Without a name-to-ID mapping, cannot filter reliably; return empty.
        answer_rows = target.iloc[0:0]

# The final answer requires the 'Contents' values for John's packages.
final_answer = list(answer_rows['Contents'])

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
