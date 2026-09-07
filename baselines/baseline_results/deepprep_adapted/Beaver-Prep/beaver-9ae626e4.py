import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_SUBJECT_SESSION_KEY", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IAP_SUBJECT_SESSION_KEY"] = table_1["IAP_SUBJECT_SESSION_KEY"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_CATEGORY_KEY'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_CATEGORY_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_CATEGORY_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_CATEGORY_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_CATEGORY_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'IAP_SUBJECT_CATEGORY_KEY'], keep='first').reset_index(drop=True)

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
    # DropColumn(table_name="table_1", drop_columns=['SPONSOR_TYPE'])
    # DropColumn
    table_1 = table_1.drop(columns=['SPONSOR_TYPE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_SUBJECT_SPONSOR_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
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
    #     # remove surrounding quotes if present
    #     if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
    #         s = s[1:-1].strip()
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding quotes if present
        if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
            s = s[1:-1].strip()
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
    # CalculateStatistic(table_name="table_1", statistic_name="distinct_iap_subject_session_key_count", func="""
    # def calculate_stat(df: pd.DataFrame):
    #     return df['iap_subject_session_key'].nunique(dropna=True)
    # """)
    # CalculateStatistic -> statistic_table
    def calculate_stat(df: pd.DataFrame):
        return df['iap_subject_session_key'].nunique(dropna=True)
    _stat_val = calculate_stat(table_1)
    _stat_row = pd.DataFrame({'operator': ['CalculateStatistic(table_name="table_1", statistic_name="distinct_iap_subject_session_key_count", func="""\ndef calculate_stat(df: pd.DataFrame):\n    return df[\'iap_subject_session_key\'].nunique(dropna=True)\n""")'], 'statistic_name': ['distinct_iap_subject_session_key_count'], 'value': [_stat_val]})
    try:
        statistic_table = pd.concat([statistic_table, _stat_row], ignore_index=True)
    except NameError:
        statistic_table = _stat_row

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="iap_subject_session_key", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # treat empty/NA-like strings as null
    #     if s == "" or s.lower() in {"nan", "none", "null"}:
    #         return None
    #     return s
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # treat empty/NA-like strings as null
        if s == "" or s.lower() in {"nan", "none", "null"}:
            return None
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["iap_subject_session_key"] = table_1["iap_subject_session_key"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['iap_subject_session_key'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['iap_subject_session_key'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['iap_subject_session_key'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['iap_subject_session_key'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key'] if c in table_1.columns]
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
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sponsors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_sessions = prepared_table_3

# Merge subjects with sessions to ensure we count valid sessions
sub_sess = prepared_subjects.merge(
    prepared_sessions, left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key', how='left'
)

# Aggregate per sponsor: count distinct session keys and distinct subjects (using category key as subject identifier)
agg = sub_sess.groupby('IAP_SUBJECT_SPONSOR_KEY').agg(
    num_iap_sessions=pd.NamedAgg(column='IAP_SUBJECT_SESSION_KEY', aggfunc=lambda s: s.dropna().nunique()),
    num_unique_subjects=pd.NamedAgg(column='IAP_SUBJECT_CATEGORY_KEY', aggfunc=lambda s: s.dropna().nunique())
).reset_index()

# Attach sponsor names
result = agg.merge(prepared_sponsors, on='IAP_SUBJECT_SPONSOR_KEY', how='left')[
    ['SPONSOR_NAME', 'num_iap_sessions', 'num_unique_subjects']
].sort_values('SPONSOR_NAME', kind='stable')

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
