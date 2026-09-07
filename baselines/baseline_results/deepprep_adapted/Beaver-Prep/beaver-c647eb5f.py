import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_LOCATION", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     # preserve NaN-like values
    #     if isinstance(s, float):
    #         return s
    #     s2 = str(s).strip()
    #     # collapse internal whitespace
    #     s2 = re.sub(r'\s+', ' ', s2)
    #     return s2
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        # preserve NaN-like values
        if isinstance(s, float):
            return s
        s2 = str(s).strip()
        # collapse internal whitespace
        s2 = re.sub(r'\s+', ' ', s2)
        return s2
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_LOCATION"] = table_1["SESSION_LOCATION"].apply(_std_apply)

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_START_TIME", func="""
    # import re
    # from datetime import datetime
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     if isinstance(s, float):
    #         return s
    #     s2 = str(s).strip().upper()
    #     if s2 in ("", "NAN", "NONE"):
    #         return None
    #     # Expect patterns like 1100AM, 0500PM, 1030AM
    #     m = re.fullmatch(r'(\d{1,4})(AM|PM)', s2)
    #     if not m:
    #         return s2  # keep raw if unexpected
    #     digits, ap = m.group(1), m.group(2)
    #     digits = digits.zfill(4)  # 900AM -> 0900AM
    #     dt = datetime.strptime(digits + ap, "%I%M%p")
    #     return dt.strftime("%H:%M")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        if isinstance(s, float):
            return s
        s2 = str(s).strip().upper()
        if s2 in ("", "NAN", "NONE"):
            return None
        # Expect patterns like 1100AM, 0500PM, 1030AM
        m = re.fullmatch(r'(\d{1,4})(AM|PM)', s2)
        if not m:
            return s2  # keep raw if unexpected
        digits, ap = m.group(1), m.group(2)
        digits = digits.zfill(4)  # 900AM -> 0900AM
        dt = datetime.strptime(digits + ap, "%I%M%p")
        return dt.strftime("%H:%M")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_START_TIME"] = table_1["SESSION_START_TIME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_END_TIME", func="""
    # import re
    # from datetime import datetime
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     if isinstance(s, float):
    #         return s
    #     s2 = str(s).strip().upper()
    #     if s2 in ("", "NAN", "NONE"):
    #         return None
    #     m = re.fullmatch(r'(\d{1,4})(AM|PM)', s2)
    #     if not m:
    #         return s2
    #     digits, ap = m.group(1), m.group(2)
    #     digits = digits.zfill(4)
    #     dt = datetime.strptime(digits + ap, "%I%M%p")
    #     return dt.strftime("%H:%M")
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        if isinstance(s, float):
            return s
        s2 = str(s).strip().upper()
        if s2 in ("", "NAN", "NONE"):
            return None
        m = re.fullmatch(r'(\d{1,4})(AM|PM)', s2)
        if not m:
            return s2
        digits, ap = m.group(1), m.group(2)
        digits = digits.zfill(4)
        dt = datetime.strptime(digits + ap, "%I%M%p")
        return dt.strftime("%H:%M")
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SESSION_END_TIME"] = table_1["SESSION_END_TIME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ACTIVITY_TITLE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ACTIVITY_TITLE'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
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

    # ---------------- Step 3 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="FEE", mode="mean")
    # MissingValueImputation
    table_1["FEE"] = table_1["FEE"].fillna(table_1["FEE"].mean())

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SESSION_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SESSION_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'FEE'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'FEE'] if c in table_1.columns]
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
prepared_sessions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subjects = prepared_table_2

# Merge sessions with subject/activity metadata on the session key
merged = prepared_sessions.merge(
    prepared_subjects,
    left_on='iap_subject_session_key',
    right_on='IAP_SUBJECT_SESSION_KEY',
    how='left'
)

# Normalize and filter to physical locations (exclude virtual/online markers)
loc = merged['SESSION_LOCATION'].astype(str).str.strip()
virtual_markers = ['virtual', 'zoom', 'online', 'remote']
mask_physical = ~loc.str.lower().fillna('').str.contains('|'.join(virtual_markers)) & (loc != '') & (loc.str.lower() != 'nan')
phys = merged.loc[mask_physical].copy()

# Parse times and compute duration (in minutes)

def parse_time(s):
    if pd.isna(s):
        return pd.NaT
    s = str(s).strip().upper()
    # Handle times like 1100AM, 1200PM, 1:30PM, etc.
    # Insert colon if missing
    if ':' not in s and len(s) in (5,6):
        # e.g., 1100AM -> 11:00AM, 0930AM -> 09:30AM
        ampm = s[-2:]
        core = s[:-2]
        if len(core) == 4:
            s = core[:2] + ':' + core[2:] + ampm
        elif len(core) == 3:
            s = core[:1] + ':' + core[1:] + ampm
    # Try multiple formats
    for fmt in ['%I:%M%p', '%I%p']:
        try:
            return pd.to_datetime(s, format=fmt, errors='raise')
        except Exception:
            continue
    return pd.NaT

phys['start_dt'] = phys['SESSION_START_TIME'].apply(parse_time)
phys['end_dt'] = phys['SESSION_END_TIME'].apply(parse_time)

# If end < start (spans noon/midnight parsing artifacts), add 12 hours where appropriate
cross_mask = (phys['start_dt'].notna() & phys['end_dt'].notna() & (phys['end_dt'] < phys['start_dt']))
phys.loc[cross_mask, 'end_dt'] = phys.loc[cross_mask, 'end_dt'] + pd.Timedelta(hours=12)

phys['duration_min'] = (phys['end_dt'] - phys['start_dt']).dt.total_seconds() / 60.0

# Coerce fee to numeric and treat NaN as 0 for total fee aggregation
phys['fee_num'] = pd.to_numeric(phys['FEE'], errors='coerce').fillna(0)

# Aggregate by physical location (building name/room string in SESSION_LOCATION)
agg = phys.groupby('SESSION_LOCATION', dropna=False).agg(
    total_subjects=('iap_subject_session_key', 'nunique'),
    total_fee=('fee_num', 'sum'),
    shortest_session_min=('duration_min', 'min'),
    longest_session_min=('duration_min', 'max')
).reset_index().rename(columns={'SESSION_LOCATION': 'building'})

# Final result per physical IAP session location
target = agg[['building', 'total_subjects', 'total_fee', 'shortest_session_min', 'longest_session_min']]

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
