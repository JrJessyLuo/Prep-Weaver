import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="TERM_CODE", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['TERM_CODE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['TERM_CODE']
    if _dtype == "datetime64":
        table_1['TERM_CODE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['TERM_CODE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['TERM_CODE'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'IS_CANCELLED'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'IS_CANCELLED'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'IS_CANCELLED'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'IAP_SUBJECT_SESSION_KEY', 'TERM_CODE', 'IS_CANCELLED'], keep='first').reset_index(drop=True)

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
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_CATEGORY_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_CATEGORY_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_SUBJECT_CATEGORY_KEY", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     # remove surrounding double-quotes if present
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        # remove surrounding double-quotes if present
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IAP_SUBJECT_CATEGORY_KEY"] = table_1["IAP_SUBJECT_CATEGORY_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="IAP_CATEGORY_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    #         s = s[1:-1]
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["IAP_CATEGORY_NAME"] = table_1["IAP_CATEGORY_NAME"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME'] if c in table_1.columns]
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'])
    # SelectCol
    _cols = [c for c in ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME'] if c in table_1.columns]
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
def _prep_4(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     return row.get('HAS_SESSION_INFO') == 'Y'
    # """)
    # Filter
    def filter_func(row):
        return row.get('HAS_SESSION_INFO') == 'Y'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SESSION_START_TIME", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip().upper()
    #     if s in ("", "NAN", "NONE", "NULL"):
    #         return None
    #     # Normalize patterns like '1100AM', '11:00 AM', '1100 AM' -> '1100AM'
    #     s = s.replace(" ", "")
    #     s = s.replace(":", "")
    #     # Keep only valid time tokens like 3-4 digits + AM/PM
    #     m = re.match(r'^(\d{3,4})(AM|PM)$', s)
    #     if m:
    #         digits, ap = m.groups()
    #         # left-pad to 4 digits (e.g., 900AM -> 0900AM)
    #         digits = digits.zfill(4)
    #         return f"{digits}{ap}"
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip().upper()
        if s in ("", "NAN", "NONE", "NULL"):
            return None
        # Normalize patterns like '1100AM', '11:00 AM', '1100 AM' -> '1100AM'
        s = s.replace(" ", "")
        s = s.replace(":", "")
        # Keep only valid time tokens like 3-4 digits + AM/PM
        m = re.match(r'^(\d{3,4})(AM|PM)$', s)
        if m:
            digits, ap = m.groups()
            # left-pad to 4 digits (e.g., 900AM -> 0900AM)
            digits = digits.zfill(4)
            return f"{digits}{ap}"
        return s
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
    # DropNulls(table_name="table_1", subset=['iap_subject_session_key', 'SESSION_START_TIME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['iap_subject_session_key', 'SESSION_START_TIME'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['iap_subject_session_key'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['iap_subject_session_key'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['iap_subject_session_key', 'SESSION_START_TIME'])
    # SelectCol
    _cols = [c for c in ['iap_subject_session_key', 'SESSION_START_TIME'] if c in table_1.columns]
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
iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
iap_categories = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
iap_sponsors = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
iap_sessions = prepared_table_4

# Assume prepared tables already loaded as dataframes: iap_subjects, iap_categories, iap_sponsors, iap_sessions

# Clean potential whitespace in keys
for df, cols in [
    (iap_subjects, ["IAP_SUBJECT_CATEGORY_KEY", "IAP_SUBJECT_SPONSOR_KEY", "IAP_SUBJECT_SESSION_KEY"]),
    (iap_categories, ["IAP_SUBJECT_CATEGORY_KEY"]),
    (iap_sponsors, ["IAP_SUBJECT_SPONSOR_KEY"]),
    (iap_sessions, ["iap_subject_session_key"]),
]:
    for c in cols:
        df[c] = df[c].astype(str).str.strip()

# Join dimensions
subjects_cat = iap_subjects.merge(iap_categories, on="IAP_SUBJECT_CATEGORY_KEY", how="left")
subjects_cat_spon = subjects_cat.merge(iap_sponsors, on="IAP_SUBJECT_SPONSOR_KEY", how="left")
full = subjects_cat_spon.merge(iap_sessions, left_on="IAP_SUBJECT_SESSION_KEY", right_on="iap_subject_session_key", how="left")

# Exclude cancelled sessions for counting
full_active = full[full["IS_CANCELLED"].astype(str).str.upper().ne("Y")]

# Define helpers
def mode_or_null(s):
    s = s.dropna()
    if s.empty:
        return None
    vc = s.value_counts(dropna=True)
    # Tie-breaker: first by highest count, then alphabetical
    top_count = vc.iloc[0]
    candidates = vc[vc == top_count].index
    return sorted([str(x) for x in candidates])[0]

# Aggregate per category
grp = full_active.groupby(["IAP_SUBJECT_CATEGORY_KEY", "IAP_CATEGORY_NAME"], dropna=False)

agg_df = grp.agg(
    unique_sessions=("IAP_SUBJECT_SESSION_KEY", lambda x: x.dropna().nunique()),
    total_attendees=("IAP_SUBJECT_PERSON_KEY", "count"),
    begin_term_code=("TERM_CODE", lambda x: x.dropna().min() if len(x.dropna()) else None),
    end_term_code=("TERM_CODE", lambda x: x.dropna().max() if len(x.dropna()) else None),
    most_common_sponsor=("SPONSOR_NAME", mode_or_null),
    most_common_start_time=("SESSION_START_TIME", mode_or_null)
).reset_index()

# Compose active period string
def fmt_period(beg, end):
    if pd.isna(beg) and pd.isna(end):
        return None
    b = None if pd.isna(beg) else str(beg)
    e = None if pd.isna(end) else str(end)
    if b is None and e is not None:
        return f"-{e}"
    if b is not None and e is None:
        return f"{b}-"
    return f"{b}-{e}"

agg_df["active_period"] = [fmt_period(b, e) for b, e in zip(agg_df["begin_term_code"], agg_df["end_term_code"])]

result_cols = [
    "IAP_CATEGORY_NAME",
    "unique_sessions",
    "total_attendees",
    "active_period",
    "most_common_sponsor",
    "most_common_start_time",
]
result = agg_df[result_cols].rename(columns={"IAP_CATEGORY_NAME": "category_name"})

# Grand total row across all categories
grand_sessions = full_active["IAP_SUBJECT_SESSION_KEY"].dropna().nunique()
grand_attendees = full_active["IAP_SUBJECT_PERSON_KEY"].shape[0]

grand_row = pd.DataFrame([
    {
        "category_name": "TOTAL",
        "unique_sessions": int(grand_sessions),
        "total_attendees": int(grand_attendees),
        "active_period": None,
        "most_common_sponsor": None,
        "most_common_start_time": None,
    }
])

final_output = pd.concat([result, grand_row], ignore_index=True)

# final_output is the answer dataframe

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
