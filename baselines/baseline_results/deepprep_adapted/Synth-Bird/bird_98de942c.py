import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Diagnosis", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     s = re.sub(r'\s+', ' ', s)
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        s = re.sub(r'\s+', ' ', s)
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Diagnosis"] = table_1["Diagnosis"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Examination Date", date_format="%Y-%m-%d")
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
    table_1['Examination Date'] = table_1['Examination Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Examination Date'] = table_1['Examination Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Examination Date', 'Diagnosis'])
    # SelectCol
    _cols = [c for c in ['ID', 'Examination Date', 'Diagnosis'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
    # SelectCol(table_name="table_1", columns=['ID', 'Date'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date'] if c in table_1.columns]
    table_1 = table_1[_cols]

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

prepared_table_1 = _prep_1(tables['table_3'])
patients_diagnosis = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
lab_results = prepared_table_2

# Ensure consistent ID typing (table_1 had float-like strings, table_2 had ints)
patients_diagnosis['ID'] = patients_diagnosis['ID'].astype(str).str.replace('.0$', '', regex=True).str.strip()
lab_results['ID'] = lab_results['ID'].astype(str).str.strip()

# Filter for the specific patient
pid = '30609'
pat = patients_diagnosis[patients_diagnosis['ID'] == pid]

# Get all lab test dates for this patient
labs = lab_results[lab_results['ID'] == pid][['Date']].dropna().drop_duplicates().sort_values('Date')

# Extract diagnosis (could be multiple rows; collect unique non-null values)
diagnosis_vals = pat['Diagnosis'].dropna().astype(str).str.strip().unique().tolist()
diagnosis = ', '.join([d for d in diagnosis_vals if d]) if diagnosis_vals else ''

# Prepare final answer structure
answer = {
    'patient_id': pid,
    'diagnosis': diagnosis,
    'lab_test_dates': labs['Date'].tolist()
}

target = pd.DataFrame([answer])

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
