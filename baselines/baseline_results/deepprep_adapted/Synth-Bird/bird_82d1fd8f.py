import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Admission", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s2 = str(s).strip()
    #     if s2.lower() in {"nan", "none", ""}:
    #         return None
    #     # normalize common outpatient marker
    #     if s2 in {"-", "–", "—"}:
    #         return "-"
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s2 = str(s).strip()
        if s2.lower() in {"nan", "none", ""}:
            return None
        # normalize common outpatient marker
        if s2 in {"-", "–", "—"}:
            return "-"
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Admission"] = table_1["Admission"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ID']
    if _dtype == "datetime64":
        table_1['ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Admission'])
    # SelectCol
    _cols = [c for c in ['ID', 'Admission'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID'], keep='last').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="RBC", mode="median")
    # MissingValueImputation
    table_1["RBC"] = table_1["RBC"].fillna(table_1["RBC"].median())

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
    # CastType(table_name="table_1", column="RBC", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['RBC'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['RBC']
    if _dtype == "datetime64":
        table_1['RBC'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['RBC'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['RBC'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['RBC'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'RBC'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'RBC'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
patients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs = prepared_table_2

# Assume prepared tables are provided as dataframes: patients, labs
# 1) Join patients with labs on patient ID
joined = labs.merge(patients, on='ID', how='inner')

# 2) Identify outpatient follow-up. Here, we assume Admission == '-' indicates outpatient clinic
outpatient = joined[joined['Admission'] == '-']

# 3) Determine abnormal RBC. Without reference ranges, use a generic adult threshold example or mark non-null extremes; here we flag RBC outside [3.8, 5.8] (x10^6/µL)
# If units differ, adjust outside this code.
abnormal = outpatient[(outpatient['RBC'].notna()) & ((outpatient['RBC'] < 3.8) | (outpatient['RBC'] > 5.8))]

# 4) List unique patient IDs meeting both conditions
answer = abnormal[['ID']].drop_duplicates().sort_values('ID').reset_index(drop=True)
answer

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
