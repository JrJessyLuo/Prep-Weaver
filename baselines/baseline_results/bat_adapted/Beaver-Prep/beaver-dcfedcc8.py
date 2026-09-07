import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['IAP_SUBJECT_CATEGORY_KEY','IAP_SUBJECT_SPONSOR_KEY','IAP_SUBJECT_SESSION_KEY','TERM_CODE','IS_CANCELLED']
    df = table_1[cols].copy()
    df['TERM_CODE'] = df['TERM_CODE'].astype('string')
    df['IS_CANCELLED'] = df['IS_CANCELLED'].astype('string')
    target = df.groupby(['IAP_SUBJECT_CATEGORY_KEY','IAP_SUBJECT_SPONSOR_KEY','IAP_SUBJECT_SESSION_KEY'], as_index=False).agg({'TERM_CODE':'first','IS_CANCELLED':'first'})[cols]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['IAP_SUBJECT_SPONSOR_KEY','SPONSOR_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    source = table_1[['iap_subject_session_key','SESSION_START_TIME']].copy()
    source['SESSION_START_TIME'] = source['SESSION_START_TIME'].replace('nan', pd.NA)
    source = source.sort_values(['iap_subject_session_key','SESSION_START_TIME'], na_position='last')
    target = source.drop_duplicates(subset=['iap_subject_session_key'], keep='first')[['iap_subject_session_key','SESSION_START_TIME']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
