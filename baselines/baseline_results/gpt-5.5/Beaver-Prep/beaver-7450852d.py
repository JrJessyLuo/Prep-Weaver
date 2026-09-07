import pandas as pd
import numpy as np

subjects = tables["table_1"].copy()
sessions = tables["table_2"].copy()

# Standardize join keys
subjects["session_key"] = subjects["IAP_SUBJECT_SESSION_KEY"].astype(str).str.strip().str.lower()
sessions["session_key"] = sessions["iap_subject_session_key"].astype(str).str.strip().str.lower()

# Identify virtual sessions from session-location style fields
virtual_pattern = r"\b(virtual|zoom|online|remote|webex|teams)\b"
search_text = (
    sessions["SESSION_LOCATION"].fillna("").astype(str) + " " +
    sessions["SESSION_TITLE"].fillna("").astype(str) + " " +
    sessions["SESSION_DESCRIPTION"].fillna("").astype(str)
)
virtual_sessions = sessions[
    search_text.str.contains(virtual_pattern, case=False, regex=True, na=False)
].copy()

# Deduplicate subjects/activities before aggregating subject count and fees
virtual_subject_keys = virtual_sessions["session_key"].dropna().unique()
virtual_subjects = subjects[
    subjects["session_key"].isin(virtual_subject_keys)
].drop_duplicates(subset=["session_key"])

total_number_of_subjects = virtual_subjects["session_key"].nunique()
total_fee = virtual_subjects["FEE"].fillna(0).sum()

# Compute session durations
def parse_datetime(date_series, time_series):
    dt_str = date_series.fillna("").astype(str).str.strip() + " " + time_series.fillna("").astype(str).str.strip()
    return pd.to_datetime(dt_str, format="%d-%b-%y %I%M%p", errors="coerce")

virtual_sessions["start_dt"] = parse_datetime(
    virtual_sessions["SESSION_DATE"], virtual_sessions["SESSION_START_TIME"]
)
virtual_sessions["end_dt"] = parse_datetime(
    virtual_sessions["SESSION_DATE"], virtual_sessions["SESSION_END_TIME"]
)

# If an end time is earlier than/equal to the start time, assume it ends after midnight
overnight = virtual_sessions["end_dt"].notna() & virtual_sessions["start_dt"].notna() & (
    virtual_sessions["end_dt"] <= virtual_sessions["start_dt"]
)
virtual_sessions.loc[overnight, "end_dt"] += pd.Timedelta(days=1)

virtual_sessions["session_duration"] = virtual_sessions["end_dt"] - virtual_sessions["start_dt"]
valid_durations = virtual_sessions["session_duration"].dropna()

result_df = pd.DataFrame([{
    "total_number_of_subjects": total_number_of_subjects,
    "total_fee": total_fee,
    "shortest_session": valid_durations.min() if not valid_durations.empty else pd.NaT,
    "longest_session": valid_durations.max() if not valid_durations.empty else pd.NaT
}])

result = {"virtual_iap_session_summary": result_df}
