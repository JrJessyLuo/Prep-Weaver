import pandas as pd

def _norm_key(s):
    return s.astype("string").str.strip().str.lower()

def _join_unique(s):
    vals = []
    seen = set()
    for x in s:
        if pd.isna(x):
            continue
        v = str(x).strip()
        if not v or v.lower() == "nan":
            continue
        if v not in seen:
            vals.append(v)
            seen.add(v)
    return ", ".join(vals) if vals else pd.NA

def _first_non_null(s):
    for x in s:
        if pd.notna(x) and str(x).strip():
            return x
    return pd.NA

subjects = tables["table_1"].copy()
sessions = tables["table_3"].copy()
categories = tables["table_4"].copy()
sponsors = tables["table_5"].copy()

subjects["_subject_key"] = _norm_key(subjects["IAP_SUBJECT_SESSION_KEY"])
subjects["_category_key"] = _norm_key(subjects["IAP_SUBJECT_CATEGORY_KEY"])
subjects["_sponsor_key"] = _norm_key(subjects["IAP_SUBJECT_SPONSOR_KEY"])

categories["_category_key"] = _norm_key(categories["IAP_SUBJECT_CATEGORY_KEY"])
sponsors["_sponsor_key"] = _norm_key(sponsors["IAP_SUBJECT_SPONSOR_KEY"])
sessions["_subject_key"] = _norm_key(sessions["iap_subject_session_key"])

base_subjects = (
    subjects.dropna(subset=["_subject_key"])
    .groupby("_subject_key", as_index=False)
    .agg(iap_subject_title=("ACTIVITY_TITLE", _first_non_null))
)

category_agg = (
    subjects[["_subject_key", "_category_key"]]
    .drop_duplicates()
    .merge(
        categories[["_category_key", "IAP_CATEGORY_NAME"]].drop_duplicates(),
        on="_category_key",
        how="left",
    )
    .groupby("_subject_key", as_index=False)
    .agg(categories=("IAP_CATEGORY_NAME", _join_unique))
)

sponsor_agg = (
    subjects[["_subject_key", "_sponsor_key"]]
    .drop_duplicates()
    .merge(
        sponsors[["_sponsor_key", "SPONSOR_NAME"]].drop_duplicates(),
        on="_sponsor_key",
        how="left",
    )
    .groupby("_subject_key", as_index=False)
    .agg(sponsor_names=("SPONSOR_NAME", _join_unique))
)

valid_sessions = sessions[
    sessions["HAS_SESSION_INFO"].astype("string").str.strip().str.upper().eq("Y")
].copy()

session_counts = (
    valid_sessions.groupby("_subject_key")
    .size()
    .reset_index(name="total_number_of_sessions")
)

session_details = valid_sessions[
    [
        "_subject_key",
        "SESSION_SEQUENCE",
        "SESSION_DATE",
        "SESSION_TITLE",
        "SESSION_START_TIME",
        "SESSION_END_TIME",
    ]
].drop_duplicates()

session_details["_session_date_sort"] = pd.to_datetime(
    session_details["SESSION_DATE"], format="%d-%b-%y", errors="coerce"
)

out = (
    base_subjects
    .merge(category_agg, on="_subject_key", how="left")
    .merge(sponsor_agg, on="_subject_key", how="left")
    .merge(session_details, on="_subject_key", how="left")
    .merge(session_counts, on="_subject_key", how="left")
)

out["total_number_of_sessions"] = (
    out["total_number_of_sessions"].fillna(0).astype(int)
)

out = out.sort_values(
    ["iap_subject_title", "_session_date_sort", "SESSION_SEQUENCE"],
    na_position="last",
).rename(
    columns={
        "SESSION_TITLE": "session_title",
        "SESSION_START_TIME": "session_start_time",
        "SESSION_END_TIME": "session_end_time",
    }
)

final = out[
    [
        "iap_subject_title",
        "categories",
        "session_title",
        "session_start_time",
        "session_end_time",
        "sponsor_names",
        "total_number_of_sessions",
    ]
].reset_index(drop=True)

result = {"iap_subject_information": final}
