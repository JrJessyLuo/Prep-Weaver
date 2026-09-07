import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # OutlierDetection(table_name="table_1", column_name="FEE", action="add_tag")
    # OutlierDetection (IQR method)
    _q1 = table_1['FEE'].quantile(0.25)
    _q3 = table_1['FEE'].quantile(0.75)
    _iqr = _q3 - _q1
    _low = _q1 - 1.5 * _iqr
    _high = _q3 + 1.5 * _iqr
    table_1['table_1_FEE_is_outlier'] = table_1['FEE'].apply(lambda x: True if x < _low or x > _high else False)
    if 'add_tag' == 'delete':
        table_1 = table_1[table_1['table_1_FEE_is_outlier'] == False]
        table_1.drop(columns=['table_1_FEE_is_outlier'], inplace=True)
    elif 'add_tag' == 'add_tag':
        table_1['table_1_FEE_is_outlier'] = table_1['table_1_FEE_is_outlier'].astype(bool)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ENROLLMENT_TYPE', 'FEE', 'IS_CANCELLED', 'IS_MULTIPLE_SESSION'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ENROLLMENT_TYPE', 'FEE', 'IS_CANCELLED', 'IS_MULTIPLE_SESSION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ENROLLMENT_TYPE', 'FEE', 'IS_CANCELLED', 'IS_MULTIPLE_SESSION'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'ENROLLMENT_TYPE', 'FEE', 'IS_CANCELLED', 'IS_MULTIPLE_SESSION'], keep='first').reset_index(drop=True)

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
    # StandardizeString(table_name="table_1", column_name="SESSION_LOCATION", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    #     s = re.sub(r"\s+", " ", s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", ""]:
            return None
        s = re.sub(r"\s+", " ", s)
        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_LOCATION"] = table_1["SESSION_LOCATION"].apply(_std_apply)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_START_TIME", func="""
    # import re
    # from datetime import datetime
    # 
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    # 
    #     # Normalize common patterns like 1100AM, 0500PM, 10:30AM, 1030 AM
    #     s_norm = re.sub(r"\s+", "", s.upper())
    #     s_norm = s_norm.replace(".", "")
    # 
    #     # If already HH:MM (24h), keep
    #     if re.fullmatch(r"\d{2}:\d{2}", s_norm):
    #         return s_norm
    # 
    #     # Parse 12-hour formats with AM/PM
    #     for fmt in ("%I%M%p", "%I:%M%p", "%I%p"):
    #         try:
    #             dt = datetime.strptime(s_norm, fmt)
    #             return dt.strftime("%H:%M")
    #         except Exception:
    #             pass
    # 
    #     return s
    # """)
    # StandardizeString

    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", ""]:
            return None

        # Normalize common patterns like 1100AM, 0500PM, 10:30AM, 1030 AM
        s_norm = re.sub(r"\s+", "", s.upper())
        s_norm = s_norm.replace(".", "")

        # If already HH:MM (24h), keep
        if re.fullmatch(r"\d{2}:\d{2}", s_norm):
            return s_norm

        # Parse 12-hour formats with AM/PM
        for fmt in ("%I%M%p", "%I:%M%p", "%I%p"):
            try:
                dt = datetime.strptime(s_norm, fmt)
                return dt.strftime("%H:%M")
            except Exception:
                pass

        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_START_TIME"] = table_1["SESSION_START_TIME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_END_TIME", func="""
    # import re
    # from datetime import datetime
    # 
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s.lower() in ["nan", "none", ""]:
    #         return None
    # 
    #     s_norm = re.sub(r"\s+", "", s.upper())
    #     s_norm = s_norm.replace(".", "")
    # 
    #     if re.fullmatch(r"\d{2}:\d{2}", s_norm):
    #         return s_norm
    # 
    #     for fmt in ("%I%M%p", "%I:%M%p", "%I%p"):
    #         try:
    #             dt = datetime.strptime(s_norm, fmt)
    #             return dt.strftime("%H:%M")
    #         except Exception:
    #             pass
    # 
    #     return s
    # """)
    # StandardizeString

    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        if s.lower() in ["nan", "none", ""]:
            return None

        s_norm = re.sub(r"\s+", "", s.upper())
        s_norm = s_norm.replace(".", "")

        if re.fullmatch(r"\d{2}:\d{2}", s_norm):
            return s_norm

        for fmt in ("%I%M%p", "%I:%M%p", "%I%p"):
            try:
                dt = datetime.strptime(s_norm, fmt)
                return dt.strftime("%H:%M")
            except Exception:
                pass

        return s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_END_TIME"] = table_1["SESSION_END_TIME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_START_TIME', 'SESSION_END_TIME', 'SESSION_DATE', 'HAS_SESSION_INFO'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_START_TIME', 'SESSION_END_TIME', 'SESSION_DATE', 'HAS_SESSION_INFO'] if c in table_1.columns]
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
prepared_sessions = prepared_table_2

# Assume prepared_subjects and prepared_sessions are already materialized per the target schemas.

# Join subjects to sessions on the session key
joined = prepared_subjects.merge(
    prepared_sessions,
    left_on='IAP_SUBJECT_SESSION_KEY',
    right_on='iap_subject_session_key',
    how='inner'
)

# Filter to IAP term codes (TERM_CODE ending with 'JA' commonly denotes IAP) and non-cancelled subjects
joined = joined[(joined['TERM_CODE'].astype(str).str.contains('JA', na=False)) & (joined['IS_CANCELLED'] != 'Y')]

# Identify virtual sessions by location text
loc = joined['SESSION_LOCATION'].astype(str).str.lower()
virtual_mask = loc.str.contains('virtual', na=False) | loc.str.contains('zoom', na=False) | loc.str.contains('online', na=False)
virt = joined[virtual_mask].copy()

# Parse times to compute duration in minutes; coerce errors to NaT
# Normalize times like '1100AM', '1200PM', '1030AM'
def parse_time(s):
    s = str(s).strip().upper()
    if s == 'NAN' or s == '' or s == 'NA':
        return pd.NaT
    # Insert colon before last two digits if missing
    m = re.match(r'^(\d{1,2})(\d{2})(AM|PM)$', s)
    if m:
        h, mnt, ap = m.groups()
        return pd.to_datetime(f"{h}:{mnt} {ap}", format='%I:%M %p', errors='coerce')
    # Try generic parser
    return pd.to_datetime(s, format='%I:%M%p', errors='coerce')

start_ts = virt['SESSION_START_TIME'].map(parse_time)
end_ts = virt['SESSION_END_TIME'].map(parse_time)

# Compute duration in minutes, dropping rows without valid times
valid = start_ts.notna() & end_ts.notna()
virt_valid = virt[valid].copy()
virt_valid['duration_min'] = (end_ts[valid] - start_ts[valid]).dt.total_seconds() / 60.0

# Total number of subjects involved in virtual sessions (distinct IAP subject session keys)
num_subjects = virt_valid['IAP_SUBJECT_SESSION_KEY'].nunique()

# Total fee across those subjects; treat missing as 0, sum distinct per subject to avoid double-counting across multiple session rows
fees = virt_valid[['IAP_SUBJECT_SESSION_KEY', 'FEE']].drop_duplicates('IAP_SUBJECT_SESSION_KEY').copy()
fees['FEE'] = pd.to_numeric(fees['FEE'], errors='coerce').fillna(0)
total_fee = float(fees['FEE'].sum())

# Shortest and longest session durations among virtual sessions (in minutes)
shortest = float(virt_valid['duration_min'].min()) if not virt_valid.empty else None
longest = float(virt_valid['duration_min'].max()) if not virt_valid.empty else None

answer = {
    'total_subjects': int(num_subjects),
    'total_fee': total_fee,
    'shortest_session_minutes': shortest,
    'longest_session_minutes': longest
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
