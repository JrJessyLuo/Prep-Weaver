import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="GPT", mode="mode")
    # MissingValueImputation
    table_1["GPT"] = table_1["GPT"].fillna(table_1["GPT"].mode().iloc[0])

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
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'GPT'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'GPT'] if c in table_1.columns]
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
    # ErrorDetection(table_name="table_1", column_name="Diagnosis", func="""
    # def is_valid_diagnosis(val):
    #     if val is None:
    #         return False
    #     s = str(val).strip()
    #     return len(s) > 0 and s.lower() not in {'none','nan','null'}
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid_diagnosis(val):
        if val is None:
            return False
        s = str(val).strip()
        return len(s) > 0 and s.lower() not in {'none','nan','null'}
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid_diagnosis(val))
        except Exception:
            return False
    table_1 = table_1[table_1['Diagnosis'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ID'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ID'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="Diagnosis", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # collapse repeated whitespace
    #     s = re.sub(r'\s+', ' ', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # collapse repeated whitespace
        s = re.sub(r'\s+', ' ', s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["Diagnosis"] = table_1["Diagnosis"].apply(_std_apply)

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Diagnosis'])
    # SelectCol
    _cols = [c for c in ['ID', 'Diagnosis'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['Diagnosis'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['Diagnosis'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['ID'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_lab_results = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_patient_diagnosis = prepared_table_2

# Assume prepared_lab_results and prepared_patient_diagnosis are provided DataFrames
# 1) Clean types
labs = prepared_lab_results.copy()
# Coerce GPT to numeric
labs['GPT'] = pd.to_numeric(labs['GPT'], errors='coerce')
# Coerce Date to datetime (this is laboratory date; kept but not used for DOB ordering)
labs['Date'] = pd.to_datetime(labs['Date'], errors='coerce')
# Coerce ID to string for consistent joining
labs['ID'] = labs['ID'].astype(str)

pt = prepared_patient_diagnosis.copy()
pt['ID'] = pt['ID'].astype(str)

# 2) Determine ALT (GPT) normal range threshold. If not provided, a common adult upper limit is ~40 U/L.
ALT_ULN = 40.0

# 3) Filter lab results to ALT beyond normal range
labs_abnormal = labs[labs['GPT'] > ALT_ULN]

# 4) Integrate with diagnoses on ID
merged = labs_abnormal.merge(pt, on='ID', how='left')

# 5) If a separate date of birth column existed, we'd sort by it. Since only 'Date' exists and represents exam date, 
#    we proceed with that as the available chronological proxy. Replace 'Date_of_Birth' with actual DOB if available.
result = merged.sort_values(by=['Date'], ascending=True)[['ID', 'Diagnosis']].drop_duplicates()

# 6) The final output is the list of diagnoses (with patient IDs) for patients with ALT beyond normal range, ordered by ascending date.
answer = result

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
