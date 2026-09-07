import pandas as pd
import numpy as np

# Source tables
iap = tables["table_1"].copy()
cat = tables["table_3"].copy()
sess = tables["table_4"].copy()
spon = tables["table_5"].copy()

# Normalize join keys
iap["category_key"] = iap["IAP_SUBJECT_CATEGORY_KEY"].astype(str).str.strip()
iap["sponsor_key"] = iap["IAP_SUBJECT_SPONSOR_KEY"].astype(str).str.strip()
iap["session_key"] = iap["IAP_SUBJECT_SESSION_KEY"].astype(str).str.strip()

cat["category_key"] = cat["IAP_SUBJECT_CATEGORY_KEY"].astype(str).str.strip()
spon["sponsor_key"] = spon["IAP_SUBJECT_SPONSOR_KEY"].astype(str).str.strip()
sess["session_key"] = sess["iap_subject_session_key"].astype(str).str.strip()

# One row per category-session for session counts, attendees, and active period
cat_sessions = (
    iap[["category_key", "session_key", "TERM_CODE", "MAX_ENROLLMENT"]]
    .drop_duplicates(subset=["category_key", "session_key"])
    .copy()
)

cat_sessions["MAX_ENROLLMENT"] = pd.to_numeric(cat_sessions["MAX_ENROLLMENT"], errors="coerce").fillna(0)

base_agg = (
    cat_sessions
    .groupby("category_key", as_index=False)
    .agg(
        number_of_unique_sessions=("session_key", "nunique"),
        total_number_of_attendees=("MAX_ENROLLMENT", "sum"),
        beginning_term_code=("TERM_CODE", "min"),
        end_term_code=("TERM_CODE", "max"),
    )
)

base_agg["active_period"] = (
    base_agg["beginning_term_code"].astype(str) + "-" + base_agg["end_term_code"].astype(str)
)

# Category names
base_agg = base_agg.merge(
    cat[["category_key", "IAP_CATEGORY_NAME"]].drop_duplicates("category_key"),
    on="category_key",
    how="left"
)

# Most common sponsor name per category, counting unique category-session-sponsor combinations
cat_sponsors = (
    iap[["category_key", "session_key", "sponsor_key"]]
    .drop_duplicates()
    .merge(
        spon[["sponsor_key", "SPONSOR_NAME"]].drop_duplicates("sponsor_key"),
        on="sponsor_key",
        how="left"
    )
)

sponsor_counts = (
    cat_sponsors
    .dropna(subset=["SPONSOR_NAME"])
    .groupby(["category_key", "SPONSOR_NAME"], as_index=False)
    .agg(cnt=("session_key", "nunique"))
    .sort_values(["category_key", "cnt", "SPONSOR_NAME"], ascending=[True, False, True])
)

top_sponsor = (
    sponsor_counts
    .drop_duplicates("category_key")
    [["category_key", "SPONSOR_NAME"]]
    .rename(columns={"SPONSOR_NAME": "most_common_sponsor_name"})
)

# Most common session start time per category
cat_session_keys = cat_sessions[["category_key", "session_key"]].drop_duplicates()

session_times = (
    sess[["session_key", "SESSION_START_TIME"]]
    .dropna(subset=["SESSION_START_TIME"])
    .drop_duplicates()
)

cat_times = cat_session_keys.merge(session_times, on="session_key", how="left")

time_counts = (
    cat_times
    .dropna(subset=["SESSION_START_TIME"])
    .groupby(["category_key", "SESSION_START_TIME"], as_index=False)
    .size()
    .rename(columns={"size": "cnt"})
    .sort_values(["category_key", "cnt", "SESSION_START_TIME"], ascending=[True, False, True])
)

top_time = (
    time_counts
    .drop_duplicates("category_key")
    [["category_key", "SESSION_START_TIME"]]
    .rename(columns={"SESSION_START_TIME": "most_common_session_start_time"})
)

# Final category-level result
out = (
    base_agg
    .merge(top_sponsor, on="category_key", how="left")
    .merge(top_time, on="category_key", how="left")
)

out["IAP_CATEGORY_NAME"] = out["IAP_CATEGORY_NAME"].fillna(out["category_key"])

out = out[
    [
        "IAP_CATEGORY_NAME",
        "number_of_unique_sessions",
        "total_number_of_attendees",
        "active_period",
        "most_common_sponsor_name",
        "most_common_session_start_time",
    ]
].rename(columns={"IAP_CATEGORY_NAME": "iap_category_name"})

out["number_of_unique_sessions"] = out["number_of_unique_sessions"].astype(int)
out["total_number_of_attendees"] = out["total_number_of_attendees"].astype(int)

out = out.sort_values("iap_category_name").reset_index(drop=True)

# Grand total row
unique_sessions_all = (
    iap[["session_key", "MAX_ENROLLMENT"]]
    .drop_duplicates(subset=["session_key"])
    .copy()
)
unique_sessions_all["MAX_ENROLLMENT"] = pd.to_numeric(
    unique_sessions_all["MAX_ENROLLMENT"], errors="coerce"
).fillna(0)

grand_total = pd.DataFrame([{
    "iap_category_name": "TOTAL",
    "number_of_unique_sessions": int(unique_sessions_all["session_key"].nunique()),
    "total_number_of_attendees": int(unique_sessions_all["MAX_ENROLLMENT"].sum()),
    "active_period": pd.NA,
    "most_common_sponsor_name": pd.NA,
    "most_common_session_start_time": pd.NA,
}])

final_df = pd.concat([out, grand_total], ignore_index=True)

result = {"iap_category_summary": final_df}
