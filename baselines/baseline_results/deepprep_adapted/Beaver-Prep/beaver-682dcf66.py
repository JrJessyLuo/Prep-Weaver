import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['TERM_CODE', 'IAP_SUBJECT_SESSION_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['TERM_CODE', 'IAP_SUBJECT_SESSION_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['TERM_CODE', 'IAP_SUBJECT_SESSION_KEY', 'FEE', 'MAX_ENROLLMENT'])
    # SelectCol
    _cols = [c for c in ['TERM_CODE', 'IAP_SUBJECT_SESSION_KEY', 'FEE', 'MAX_ENROLLMENT'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FEE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FEE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FEE']
    if _dtype == "datetime64":
        table_1['FEE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FEE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FEE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FEE'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="MAX_ENROLLMENT", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['MAX_ENROLLMENT'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['MAX_ENROLLMENT']
    if _dtype == "datetime64":
        table_1['MAX_ENROLLMENT'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['MAX_ENROLLMENT'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['MAX_ENROLLMENT'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['MAX_ENROLLMENT'] = _series.astype(str)

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
    # StandardizeString(table_name="table_1", column_name="TERM_DESCRIPTION", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["TERM_DESCRIPTION"] = table_1["TERM_DESCRIPTION"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="term_code", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
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
    table_1["term_code"] = table_1["term_code"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'TERM_DESCRIPTION'])
    # SelectCol
    _cols = [c for c in ['term_code', 'TERM_DESCRIPTION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['term_code', 'TERM_DESCRIPTION'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['term_code', 'TERM_DESCRIPTION'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['term_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['term_code'], keep='last').reset_index(drop=True)

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
iap_sessions_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
terms_prepared = prepared_table_2

# Assume iap_sessions_prepared and terms_prepared are dataframes created from the respective table_targets
# Clean and ensure correct dtypes
s = iap_sessions_prepared.copy()
# Convert FEE and MAX_ENROLLMENT to numeric, coerce errors to NaN
s['FEE'] = pd.to_numeric(s['FEE'], errors='coerce')
s['MAX_ENROLLMENT'] = pd.to_numeric(s['MAX_ENROLLMENT'], errors='coerce')

# Aggregate per term
agg = s.groupby('TERM_CODE', as_index=False).agg(
    TOTAL_IAP_SESSIONS=('IAP_SUBJECT_SESSION_KEY', 'nunique'),
    TOTAL_FEE_COLLECTED=('FEE', 'sum'),
    MIN_ENROLLMENT=('MAX_ENROLLMENT', 'min'),
    MAX_ENROLLMENT=('MAX_ENROLLMENT', 'max')
)

# Join to term descriptions
result = agg.merge(terms_prepared, left_on='TERM_CODE', right_on='term_code', how='left')

# Select and order columns as requested
result = result[[
    'TERM_CODE',
    'TERM_DESCRIPTION',
    'TOTAL_IAP_SESSIONS',
    'TOTAL_FEE_COLLECTED',
    'MIN_ENROLLMENT',
    'MAX_ENROLLMENT'
]].sort_values('TERM_CODE')

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
