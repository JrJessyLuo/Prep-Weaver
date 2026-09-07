import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['patient_id', 'value'])
    # SelectCol
    _cols = [c for c in ['patient_id', 'value'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="patient_id", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove repeated quotes like ""1464229"" -> 1464229
    #     s = s.replace('""', '"').strip('"')
    #     # keep only digits if present
    #     m = re.search(r'(\d+)', s)
    #     return m.group(1) if m else s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # remove repeated quotes like ""1464229"" -> 1464229
        s = s.replace('""', '"').strip('"')
        # keep only digits if present
        m = re.search(r'(\d+)', s)
        return m.group(1) if m else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["patient_id"] = table_1["patient_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="sex", func="""
    # import re
    # import pandas as pd
    # def compute(row: pd.Series):
    #     v = row.get('value', None)
    #     if v is None:
    #         return None
    #     v = str(v).strip().lower()
    # 
    #     # explicit male/female patterns
    #     if re.fullmatch(r'(m|male|man|boy)', v) or 'male' in v:
    #         return 'M'
    #     if re.fullmatch(r'(f|female|woman|girl)', v) or 'female' in v:
    #         return 'F'
    # 
    #     # common encodings sometimes used in EHR extracts
    #     if v in ['1', 'm1', 'sex:1', 'sex=1']:
    #         return 'M'
    #     if v in ['0', '2', 'f2', 'sex:2', 'sex=2']:
    #         return 'F'
    # 
    #     # otherwise unknown/absent; do not infer from '+'/'-' etc.
    #     return None
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        v = row.get('value', None)
        if v is None:
            return None
        v = str(v).strip().lower()

        # explicit male/female patterns
        if re.fullmatch(r'(m|male|man|boy)', v) or 'male' in v:
            return 'M'
        if re.fullmatch(r'(f|female|woman|girl)', v) or 'female' in v:
            return 'F'

        # common encodings sometimes used in EHR extracts
        if v in ['1', 'm1', 'sex:1', 'sex=1']:
            return 'M'
        if v in ['0', '2', 'f2', 'sex:2', 'sex=2']:
            return 'F'

        # otherwise unknown/absent; do not infer from '+'/'-' etc.
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["sex"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['patient_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['patient_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['patient_id', 'sex'])
    # SelectCol
    _cols = [c for c in ['patient_id', 'sex'] if c in table_1.columns]
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
    # CastType(table_name="table_1", column="FG", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FG'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FG']
    if _dtype == "datetime64":
        table_1['FG'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FG'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FG'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FG'] = _series.astype(str)

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
    # CastType(table_name="table_1", column="WBC", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['WBC'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['WBC']
    if _dtype == "datetime64":
        table_1['WBC'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['WBC'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['WBC'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['WBC'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'WBC', 'FG'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'WBC', 'FG'] if c in table_1.columns]
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
lab_results = prepared_table_2

# Assume `patients` and `lab_results` are the prepared tables from BAT.
# 1) Standardize join keys
lab_results['ID'] = lab_results['ID'].astype(str).str.strip().str.replace('"','', regex=False)
patients['patient_id'] = patients['patient_id'].astype(str).str.strip().str.replace('"','', regex=False)

# 2) Keep only male patients
male_patients = patients[patients['sex'].str.upper().str.strip().isin(['M','MALE'])]

# 3) Join male patients to lab results
male_labs = male_patients.merge(lab_results, left_on='patient_id', right_on='ID', how='inner')

# 4) Define normal WBC range (adjust if domain knowledge specifies different)
# Common clinical adult normal WBC: 4.0 to 10.0 x10^3/µL
wbc_norm_low, wbc_norm_high = 4.0, 10.0

# 5) Determine per-patient whether they have any normal WBC measurement
wbc_ok = (
    male_labs.dropna(subset=['WBC'])
             .assign(wbc_normal=lambda df: (df['WBC'] >= wbc_norm_low) & (df['WBC'] <= wbc_norm_high))
             .groupby('patient_id', as_index=False)['wbc_normal'].max()
)

# 6) Determine per-patient whether they have any abnormal fibrinogen (FG) measurement
# Typical adult fibrinogen reference: 200–400 mg/dL (use if no dataset-specific range is provided)
fg_norm_low, fg_norm_high = 200.0, 400.0
fg_flag = (
    male_labs.dropna(subset=['FG'])
             .assign(fg_abnormal=lambda df: (df['FG'] < fg_norm_low) | (df['FG'] > fg_norm_high))
             .groupby('patient_id', as_index=False)['fg_abnormal'].max()
)

# 7) Patients who have a normal WBC (any time) and abnormal FG (any time)
per_patient = wbc_ok.merge(fg_flag, on='patient_id', how='inner')
answer_count = int(((per_patient['wbc_normal'] == True) & (per_patient['fg_abnormal'] == True)).sum())

result = answer_count

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
