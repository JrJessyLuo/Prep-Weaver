import pandas as pd
import numpy as np

iap = tables["table_1"].copy()
sponsors = tables["table_2"].copy()
sessions = tables["table_3"].copy()

# Exclude cancelled IAP activities when identifying sessions held
if "IS_CANCELLED" in iap.columns:
    iap = iap[iap["IS_CANCELLED"].fillna("N").astype(str).str.upper().ne("Y")].copy()

sponsor_key = "IAP_SUBJECT_SPONSOR_KEY"
activity_key = "IAP_SUBJECT_SESSION_KEY"

def first_non_null(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else np.nan

# One activity per sponsor/activity key, avoiding duplicates from categories/people
iap_activity = (
    iap.groupby([sponsor_key, activity_key], as_index=False)
       .agg(
           MAX_ENROLLMENT=("MAX_ENROLLMENT", first_non_null),
           FEE=("FEE", first_non_null)
       )
)

activity_stats = (
    iap_activity.groupby(sponsor_key, as_index=False)
    .agg(
        total_number_of_enrollment=("MAX_ENROLLMENT", lambda s: s.sum(min_count=1)),
        minimum_fee=("FEE", "min"),
        maximum_fee=("FEE", "max")
    )
)

sessions = sessions.reset_index(drop=False).rename(columns={"index": "session_row_id"})
sessions["HAS_SESSION_INFO_NORM"] = sessions["HAS_SESSION_INFO"].fillna("").astype(str).str.upper().str.strip()
sessions["session_with_info"] = sessions["HAS_SESSION_INFO_NORM"].eq("Y").astype(int)
sessions["session_without_info"] = sessions["HAS_SESSION_INFO_NORM"].eq("N").astype(int)

joined_sessions = iap_activity[[sponsor_key, activity_key]].merge(
    sessions,
    left_on=activity_key,
    right_on="iap_subject_session_key",
    how="left"
)

session_stats = (
    joined_sessions.groupby(sponsor_key, as_index=False)
    .agg(
        number_of_sessions_held=("session_row_id", "count"),
        number_of_sessions_with_info=("session_with_info", "sum"),
        number_of_sessions_without_info=("session_without_info", "sum")
    )
)

sponsor_dim = sponsors[[sponsor_key, "SPONSOR_NAME"]].drop_duplicates(subset=[sponsor_key])

out = (
    iap_activity[[sponsor_key]].drop_duplicates()
    .merge(sponsor_dim, on=sponsor_key, how="left")
    .merge(session_stats, on=sponsor_key, how="left")
    .merge(activity_stats, on=sponsor_key, how="left")
)

count_cols = [
    "number_of_sessions_held",
    "number_of_sessions_with_info",
    "number_of_sessions_without_info",
]
out[count_cols] = out[count_cols].fillna(0).astype(int)

out["SPONSOR_NAME"] = out["SPONSOR_NAME"].fillna(out[sponsor_key])

out = out[
    [
        "SPONSOR_NAME",
        "number_of_sessions_held",
        "total_number_of_enrollment",
        "minimum_fee",
        "maximum_fee",
        "number_of_sessions_with_info",
        "number_of_sessions_without_info",
    ]
].rename(columns={"SPONSOR_NAME": "sponsor_name"})

out = out.sort_values("sponsor_name").reset_index(drop=True)

result = {"sponsor_iap_session_summary": out}
