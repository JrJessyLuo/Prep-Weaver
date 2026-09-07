import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     val = row.get('ENROLLMENT_TYPE')
    #     if val is None:
    #         return False
    #     return str(val).strip().lower() == 'independent'
    # """)
    # Filter
    def filter_func(row):
        val = row.get('ENROLLMENT_TYPE')
        if val is None:
            return False
        return str(val).strip().lower() == 'independent'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ACTIVITY_TITLE', 'ENROLLMENT_TYPE', 'IAP_SUBJECT_PERSON_KEY'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ACTIVITY_TITLE', 'ENROLLMENT_TYPE', 'IAP_SUBJECT_PERSON_KEY'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ACTIVITY_TITLE', 'ENROLLMENT_TYPE', 'IAP_SUBJECT_PERSON_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ACTIVITY_TITLE', 'ENROLLMENT_TYPE', 'IAP_SUBJECT_PERSON_KEY'], keep='first').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="SESSION_END_TIME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     if s in ["NAN","NONE","NULL",""]:
    #         return None
    #     s = re.sub(r"\s+", "", s)
    #     m = re.match(r"^(\d{1,2})(?::?(\d{2}))?(AM|PM)$", s)
    #     if not m:
    #         return s
    #     hh, mm, ap = m.group(1), m.group(2) or "00", m.group(3)
    #     return f"{int(hh):02d}:{mm} {ap}"
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        if s in ["NAN","NONE","NULL",""]:
            return None
        s = re.sub(r"\s+", "", s)
        m = re.match(r"^(\d{1,2})(?::?(\d{2}))?(AM|PM)$", s)
        if not m:
            return s
        hh, mm, ap = m.group(1), m.group(2) or "00", m.group(3)
        return f"{int(hh):02d}:{mm} {ap}"
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_END_TIME"] = table_1["SESSION_END_TIME"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_START_TIME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip().upper()
    #     if s in ["NAN","NONE","NULL",""]:
    #         return None
    #     s = re.sub(r"\s+", "", s)
    #     m = re.match(r"^(\d{1,2})(?::?(\d{2}))?(AM|PM)$", s)
    #     if not m:
    #         return s
    #     hh, mm, ap = m.group(1), m.group(2) or "00", m.group(3)
    #     return f"{int(hh):02d}:{mm} {ap}"
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip().upper()
        if s in ["NAN","NONE","NULL",""]:
            return None
        s = re.sub(r"\s+", "", s)
        m = re.match(r"^(\d{1,2})(?::?(\d{2}))?(AM|PM)$", s)
        if not m:
            return s
        hh, mm, ap = m.group(1), m.group(2) or "00", m.group(3)
        return f"{int(hh):02d}:{mm} {ap}"
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_START_TIME"] = table_1["SESSION_START_TIME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_LOCATION", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s == "" or s.upper() in ["NAN","NONE","NULL"]:
    #         return None
    #     # collapse internal whitespace
    #     s_clean = re.sub(r"\s+", " ", s).strip()
    #     low = s_clean.lower()
    #     # normalize common virtual/zoom variants
    #     if "zoom" in low:
    #         return "Zoom"
    #     if "virtual" in low:
    #         return "Virtual"
    #     return s_clean
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.upper() in ["NAN","NONE","NULL"]:
            return None
        # collapse internal whitespace
        s_clean = re.sub(r"\s+", " ", s).strip()
        low = s_clean.lower()
        # normalize common virtual/zoom variants
        if "zoom" in low:
            return "Zoom"
        if "virtual" in low:
            return "Virtual"
        return s_clean
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_LOCATION"] = table_1["SESSION_LOCATION"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="SESSION_DATE", date_format="%Y-%m-%d")
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
    table_1['SESSION_DATE'] = table_1['SESSION_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['SESSION_DATE'] = table_1['SESSION_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['iap_subject_session_key'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['iap_subject_session_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 7 ----------------
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
    # Deduplicate(table_name="table_1", subset=['term_code'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['term_code'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="TERM_START_DATE", date_format="%Y-%m-%d")
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
    table_1['TERM_START_DATE'] = table_1['TERM_START_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['TERM_START_DATE'] = table_1['TERM_START_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'TERM_START_DATE'])
    # SelectCol
    _cols = [c for c in ['term_code', 'TERM_START_DATE'] if c in table_1.columns]
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_iap_sessions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_8'])
prepared_terms = prepared_table_3

# Assume prepared_iap_subjects, prepared_iap_sessions, prepared_terms are dataframes built per table_targets

# 1) Join subjects to sessions on session key
s = prepared_iap_subjects.merge(
    prepared_iap_sessions,
    left_on='IAP_SUBJECT_SESSION_KEY',
    right_on='iap_subject_session_key',
    how='left'
)

# 2) Join to terms on term_code to get term start date
s = s.merge(
    prepared_terms[['term_code', 'TERM_START_DATE']],
    left_on='TERM_CODE',
    right_on='term_code',
    how='left'
)

# 3) Filter to independent activities (case-insensitive contains 'independent' in ENROLLMENT_TYPE)
mask = s['ENROLLMENT_TYPE'].astype(str).str.contains('independent', case=True, na=False)
s = s[mask]

# 4) Select and rename output columns
out = s[[
    'ACTIVITY_TITLE',
    'SESSION_LOCATION',
    'TERM_START_DATE',
    'IAP_SUBJECT_PERSON_KEY'
]].rename(columns={
    'ACTIVITY_TITLE': 'activity_title',
    'SESSION_LOCATION': 'location',
    'TERM_START_DATE': 'term_start_date',
    'IAP_SUBJECT_PERSON_KEY': 'supervisor_name'  # Placeholder: actual name lookup would require a person dimension not provided here
})

# 5) Deduplicate and sort by ascending term_start_date
out = out.drop_duplicates().sort_values(by=['term_start_date', 'activity_title'], ascending=[True, True])

# Final result in 'out'
target = out

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
