import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SM'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SM'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SM", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s0 = str(s).strip().strip('"').strip("'")
    #     if s0 == "" or s0.lower() in {"nan", "none", "null"}:
    #         return None
    # 
    #     t = s0.lower().strip()
    # 
    #     # normalize common negative encodings
    #     if t in {"-", "negative", "neg", "0", "0.0", "nonreactive", "non-reactive"}:
    #         return "-"
    # 
    #     # normalize borderline / equivocal encodings
    #     if t in {"+-", "±", "+/-", "borderline", "equivocal"}:
    #         return "+-"
    # 
    #     # normalize positive encodings
    #     if t in {"+", "positive", "pos", "1", "1.0", "reactive"}:
    #         return "+"
    # 
    #     # if already one of expected, return cleaned original
    #     if s0 in {"+", "-", "+-"}:
    #         return s0
    # 
    #     # otherwise keep original (cleaned) to avoid destroying information
    #     return s0
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s0 = str(s).strip().strip('"').strip("'")
        if s0 == "" or s0.lower() in {"nan", "none", "null"}:
            return None

        t = s0.lower().strip()

        # normalize common negative encodings
        if t in {"-", "negative", "neg", "0", "0.0", "nonreactive", "non-reactive"}:
            return "-"

        # normalize borderline / equivocal encodings
        if t in {"+-", "±", "+/-", "borderline", "equivocal"}:
            return "+-"

        # normalize positive encodings
        if t in {"+", "positive", "pos", "1", "1.0", "reactive"}:
            return "+"

        # if already one of expected, return cleaned original
        if s0 in {"+", "-", "+-"}:
            return s0

        # otherwise keep original (cleaned) to avoid destroying information
        return s0
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SM"] = table_1["SM"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'SM'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'SM'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # StandardizeDatetime(table_name="table_1", column_name="riqi", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['riqi'] = table_1['riqi'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['riqi'] = table_1['riqi'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="Thrombosis", mode="mode")
    # MissingValueImputation
    table_1["Thrombosis"] = table_1["Thrombosis"].fillna(table_1["Thrombosis"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="Thrombosis", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['Thrombosis'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['Thrombosis']
    if _dtype == "datetime64":
        table_1['Thrombosis'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['Thrombosis'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['Thrombosis'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['Thrombosis'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'riqi', 'Thrombosis'])
    # SelectCol
    _cols = [c for c in ['ID', 'riqi', 'Thrombosis'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_table_2 = _prep_2(tables['table_1'])

# Assume prepared_table_1 and prepared_table_2 are provided DataFrames
# 1) Integrate on patient ID
merged = prepared_table_1.merge(prepared_table_2, on='ID', how='inner')

# 2) Define normal anti-SM: interpret SM values where a negative/normal is indicated (e.g., '-', '−', 'negative', 'neg', '0', '0.0'). Treat NaN as not-evaluable and exclude.
neg_markers = {'-', '−', 'negative', 'neg', '0', '0.0'}
sm_series = merged['SM'].astype(str).str.strip().str.lower()
normal_mask = sm_series.isin({m.lower() for m in neg_markers})

# Exclude rows where SM is missing/NaN
valid_sm_mask = merged['SM'].notna()
normal_sm = merged[valid_sm_mask & normal_mask]

# 3) Among those, count patients without thrombosis (Thrombosis == 0)
no_thrombosis = normal_sm[normal_sm['Thrombosis'] == 0]

# If multiple rows per patient exist, count unique patients
answer = no_thrombosis['ID'].nunique()

result = pd.DataFrame({'count_normal_SM_without_thrombosis': [answer]})

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
