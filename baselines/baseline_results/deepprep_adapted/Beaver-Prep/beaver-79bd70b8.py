import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="MAX_ENROLLMENT", mode="median")
    # MissingValueImputation
    table_1["MAX_ENROLLMENT"] = table_1["MAX_ENROLLMENT"].fillna(table_1["MAX_ENROLLMENT"].median())

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FEE", mode="median")
    # MissingValueImputation
    table_1["FEE"] = table_1["FEE"].fillna(table_1["FEE"].median())

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
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

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'MAX_ENROLLMENT', 'FEE', 'IS_CANCELLED'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'MAX_ENROLLMENT', 'FEE', 'IS_CANCELLED'] if c in table_1.columns]
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
    # DropNulls(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_SUBJECT_SPONSOR_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding double quotes if present
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding double quotes if present
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1].strip()
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IAP_SUBJECT_SPONSOR_KEY"] = table_1["IAP_SUBJECT_SPONSOR_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SPONSOR_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding double quotes if present
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1].strip()
    #     # collapse repeated internal whitespace
    #     s = " ".join(s.split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding double quotes if present
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1].strip()
        # collapse repeated internal whitespace
        s = " ".join(s.split())
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SPONSOR_NAME"] = table_1["SPONSOR_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SPONSOR_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="HAS_SESSION_INFO", func="""
    # def is_valid(val):
    #     if val is None:
    #         return False
    #     return str(val).strip().upper() in ["Y","N"]
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None:
            return False
        return str(val).strip().upper() in ["Y","N"]
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['HAS_SESSION_INFO'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="HAS_SESSION_INFO", func="""
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     v = str(s).strip().upper()
    #     if v in ["Y", "N"]:
    #         return v
    #     return None
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        v = str(s).strip().upper()
        if v in ["Y", "N"]:
            return v
        return None
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["HAS_SESSION_INFO"] = table_1["HAS_SESSION_INFO"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['iap_subject_session_key'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['iap_subject_session_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key', 'HAS_SESSION_INFO'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key', 'HAS_SESSION_INFO'] if c in table_1.columns]
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
iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
iap_sponsors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
iap_sessions = prepared_table_3

# Assume prepared tables: iap_subjects, iap_sponsors, iap_sessions
# 1) Join subjects to sponsors for names
sub_with_names = iap_subjects.merge(iap_sponsors, on='IAP_SUBJECT_SPONSOR_KEY', how='left')

# 2) Join subjects to sessions to get HAS_SESSION_INFO per session key
sub_with_sess = sub_with_names.merge(iap_sessions, left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key', how='left')

# 3) Derive helper flags
# Consider a session to have info if HAS_SESSION_INFO == 'Y'
sub_with_sess['has_info_flag'] = (sub_with_sess['HAS_SESSION_INFO'] == 'Y').astype(int)
sub_with_sess['no_info_flag'] = ((sub_with_sess['HAS_SESSION_INFO'] == 'N') | sub_with_sess['HAS_SESSION_INFO'].isna()).astype(int)

# 4) Aggregate per sponsor name
agg = sub_with_sess.groupby(['IAP_SUBJECT_SPONSOR_KEY','SPONSOR_NAME'], dropna=False).agg(
    sessions_held = ('IAP_SUBJECT_SESSION_KEY','nunique'),
    total_enrollment = ('MAX_ENROLLMENT', lambda s: pd.to_numeric(s, errors='coerce').sum(min_count=1)),
    min_fee = ('FEE', lambda s: pd.to_numeric(s, errors='coerce').min()),
    max_fee = ('FEE', lambda s: pd.to_numeric(s, errors='coerce').max()),
    sessions_with_info = ('has_info_flag','sum'),
    sessions_without_info = ('no_info_flag','sum')
).reset_index()

# 5) Select and rename columns for output
answer = agg[['SPONSOR_NAME','sessions_held','total_enrollment','min_fee','max_fee','sessions_with_info','sessions_without_info']]

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
