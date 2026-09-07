import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row.get('IAP_SUBJECT_SESSION_KEY') is not None and str(row.get('IAP_SUBJECT_SESSION_KEY')).strip() != ''
    # """)
    # Filter
    def filter_func(row):
        return row.get('IAP_SUBJECT_SESSION_KEY') is not None and str(row.get('IAP_SUBJECT_SESSION_KEY')).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['ACTIVITY_TITLE', 'TERM_CODE'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['ACTIVITY_TITLE', 'TERM_CODE'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'TERM_CODE', 'IS_CANCELLED', 'IS_MULTIPLE_SESSION'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'TERM_CODE', 'IS_CANCELLED', 'IS_MULTIPLE_SESSION'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SESSION_KEY', 'TERM_CODE'], keep='last').reset_index(drop=True)

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
    # MissingValueImputation(table_name="table_1", column_name="HAS_SESSION_INFO", mode="mode")
    # MissingValueImputation
    table_1["HAS_SESSION_INFO"] = table_1["HAS_SESSION_INFO"].fillna(table_1["HAS_SESSION_INFO"].mode().iloc[0])

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
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s == "" or s.lower() == "nan":
    #         return None
    #     # Normalize like 1100AM / 0500PM / 1030AM
    #     m = re.fullmatch(r"(\d{1,4})(AM|PM)", s.upper())
    #     if not m:
    #         return s  # leave as-is if unexpected
    #     digits, ampm = m.groups()
    #     digits = digits.zfill(4)  # ensure HHMM
    #     dt = datetime.strptime(digits + ampm, "%I%M%p")
    #     return dt.strftime("%H:%M:%S")
    # """)
    # StandardizeString

    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.lower() == "nan":
            return None
        # Normalize like 1100AM / 0500PM / 1030AM
        m = re.fullmatch(r"(\d{1,4})(AM|PM)", s.upper())
        if not m:
            return s  # leave as-is if unexpected
        digits, ampm = m.groups()
        digits = digits.zfill(4)  # ensure HHMM
        dt = datetime.strptime(digits + ampm, "%I%M%p")
        return dt.strftime("%H:%M:%S")
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
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     if s == "" or s.lower() == "nan":
    #         return None
    #     m = re.fullmatch(r"(\d{1,4})(AM|PM)", s.upper())
    #     if not m:
    #         return s
    #     digits, ampm = m.groups()
    #     digits = digits.zfill(4)
    #     dt = datetime.strptime(digits + ampm, "%I%M%p")
    #     return dt.strftime("%H:%M:%S")
    # """)
    # StandardizeString

    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        if s == "" or s.lower() == "nan":
            return None
        m = re.fullmatch(r"(\d{1,4})(AM|PM)", s.upper())
        if not m:
            return s
        digits, ampm = m.groups()
        digits = digits.zfill(4)
        dt = datetime.strptime(digits + ampm, "%I%M%p")
        return dt.strftime("%H:%M:%S")
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
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return str(row.get('HAS_SESSION_INFO', '')).strip().upper() == 'Y'
    # """)
    # Filter
    def filter_func(row):
        return str(row.get('HAS_SESSION_INFO', '')).strip().upper() == 'Y'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME'], how='any').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME', 'HAS_SESSION_INFO'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME', 'HAS_SESSION_INFO'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # ErrorDetection(table_name="table_1", column_name="TERM_END_DATE", func="""
    # import pandas as pd
    # def is_valid(val):
    #     if val is None or (isinstance(val, float) and pd.isna(val)):
    #         return False
    #     try:
    #         pd.to_datetime(str(val), format="%d-%b-%y")
    #         return True
    #     except Exception:
    #         return False
    # """)
    # ErrorDetection (keeps rows where func returns True)
    def is_valid(val):
        if val is None or (isinstance(val, float) and pd.isna(val)):
            return False
        try:
            pd.to_datetime(str(val), format="%d-%b-%y")
            return True
        except Exception:
            return False
    def _err_apply(val):
        if pd.isna(val):
            return False
        try:
            return bool(is_valid(val))
        except Exception:
            return False
    table_1 = table_1[table_1['TERM_END_DATE'].apply(_err_apply)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['term_code', 'IS_CURRENT_TERM', 'TERM_DESCRIPTION', 'TERM_START_DATE', 'TERM_END_DATE', 'TERM_STATUS'])
    # SelectCol
    _cols = [c for c in ['term_code', 'IS_CURRENT_TERM', 'TERM_DESCRIPTION', 'TERM_START_DATE', 'TERM_END_DATE', 'TERM_STATUS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="TERM_END_DATE", date_format="%Y-%m-%d")
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
    table_1['TERM_END_DATE'] = table_1['TERM_END_DATE'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['TERM_END_DATE'] = table_1['TERM_END_DATE'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 5 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['term_code'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['term_code'], how='any').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['term_code'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['term_code'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_iap_sessions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_10'])
prepared_academic_terms = prepared_table_3

# Assume prepared_iap_subjects, prepared_iap_sessions, prepared_academic_terms are dataframes

# 1) Integrate tables
sessions = prepared_iap_subjects.merge(
    prepared_academic_terms[["term_code","IS_CURRENT_TERM"]],
    left_on="TERM_CODE", right_on="term_code", how="left"
)

# Derive status label
sessions["CURRENT_STATUS"] = sessions["IS_CURRENT_TERM"].map(lambda x: "CURRENT" if str(x).strip().upper()=="Y" else "NOT CURRENT")

# Join to per-meeting sessions
meet = sessions.merge(
    prepared_iap_sessions,
    left_on="IAP_SUBJECT_SESSION_KEY", right_on="iap_subject_session_key", how="left"
)

# 2) Compute per-meeting duration in days
# Parse times; if missing or invalid, treat duration as 0

def parse_time(t):
    if pd.isna(t):
        return None
    s = str(t).strip().upper()
    # Expected forms like 1100AM, 1200PM, 1:30PM, etc.
    for fmt in ["%I%M%p","%I:%M%p","%I%p"]:
        try:
            return datetime.strptime(s, fmt)
        except Exception:
            pass
    return None

start = meet["SESSION_START_TIME"].apply(parse_time)
end = meet["SESSION_END_TIME"].apply(parse_time)

# Compute minutes difference; if either missing, 0
mins = []
for s,e in zip(start, end):
    if s is None or e is None:
        mins.append(0.0)
    else:
        # place both on same dummy date
        delta = (e - s).total_seconds() / 60.0
        if delta < 0:
            # handle potential crossing noon/midnight by adding 12 hours if needed
            delta += 12*60
        if delta < 0:
            delta = 0.0
        mins.append(delta)

meet["duration_days"] = pd.Series(mins) / (60.0*24.0)

# 3) Aggregate at (CURRENT_STATUS, ACTIVITY_TITLE)
per_session = meet.groupby(["CURRENT_STATUS","ACTIVITY_TITLE"], dropna=False).agg(
    IAP_sessions_count=("iap_subject_session_key", lambda x: x.notna().sum()),
    total_days=("duration_days","sum")
).reset_index()
per_session["avg_days"] = per_session.apply(
    lambda r: (r["total_days"] / r["IAP_sessions_count"]) if r["IAP_sessions_count"]>0 else 0.0,
    axis=1
)

# 4) Subtotals per CURRENT_STATUS
subtotals = per_session.groupby(["CURRENT_STATUS"], dropna=False).agg(
    IAP_sessions_count=("IAP_sessions_count","sum"),
    total_days=("total_days","sum")
).reset_index()
subtotals["avg_days"] = subtotals.apply(
    lambda r: (r["total_days"] / r["IAP_sessions_count"]) if r["IAP_sessions_count"]>0 else 0.0,
    axis=1
)
subtotals["ACTIVITY_TITLE"] = "Subtotal"

# 5) Grand total
grand = pd.DataFrame([{
    "CURRENT_STATUS": "Grand Total",
    "ACTIVITY_TITLE": "Grand Total",
    "IAP_sessions_count": per_session["IAP_sessions_count"].sum(),
    "total_days": per_session["total_days"].sum()
}])
grand["avg_days"] = grand.apply(
    lambda r: (r["total_days"] / r["IAP_sessions_count"]) if r["IAP_sessions_count"]>0 else 0.0,
    axis=1
)

# 6) Combine detail + subtotals + grand total
result_detail = per_session.copy()
# Order by CURRENT_STATUS then ACTIVITY_TITLE (cluster type interpreted as activity/session name)
result_detail = result_detail.sort_values(["CURRENT_STATUS","ACTIVITY_TITLE"], kind="mergesort")

# Insert subtotals beneath each status group
out = []
for status, grp in result_detail.groupby("CURRENT_STATUS", sort=False):
    out.append(grp)
    out.append(subtotals[subtotals["CURRENT_STATUS"]==status])
final_df = pd.concat(out + [grand], ignore_index=True)

# 7) Display current status only when it differs from previous entry
final_df = final_df.sort_values(["CURRENT_STATUS","ACTIVITY_TITLE"], kind="mergesort").reset_index(drop=True)
final_df["CURRENT_STATUS_DISPLAY"] = final_df["CURRENT_STATUS"]
prev = None
for i in range(len(final_df)):
    cur = final_df.at[i, "CURRENT_STATUS_DISPLAY"]
    if prev is not None and cur == prev and cur not in ("Grand Total"):
        final_df.at[i, "CURRENT_STATUS_DISPLAY"] = ""
    prev = cur

# Select and rename columns for presentation
answer = final_df[[
    "CURRENT_STATUS_DISPLAY",
    "ACTIVITY_TITLE",
    "IAP_sessions_count",
    "total_days",
    "avg_days"
]].rename(columns={
    "CURRENT_STATUS_DISPLAY":"Current Status",
    "ACTIVITY_TITLE":"Session Name",
    "IAP_sessions_count":"Number of IAP Sessions",
    "total_days":"Total IAP Session Time (days)",
    "avg_days":"Average IAP Session Time (days)"
})

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
