import pandas as pd

subjects = tables["table_1"].copy()
sponsors = tables["table_2"].copy()
sessions = tables["table_4"].copy()

# Normalize join keys
subjects["sponsor_key"] = subjects["IAP_SUBJECT_SPONSOR_KEY"].astype("string").str.strip()
subjects["subject_key"] = subjects["IAP_SUBJECT_SESSION_KEY"].astype("string").str.strip()

sponsors["sponsor_key"] = sponsors["IAP_SUBJECT_SPONSOR_KEY"].astype("string").str.strip()

sessions["subject_key"] = sessions["iap_subject_session_key"].astype("string").str.strip()
sessions["HAS_SESSION_INFO"] = sessions["HAS_SESSION_INFO"].astype("string").str.strip().str.upper()

# One row per sponsor-subject relationship
sponsor_subjects = (
    subjects[["sponsor_key", "subject_key"]]
    .dropna()
    .drop_duplicates()
)

# Count actual listed IAP session rows for each subject
session_cols = [
    "subject_key",
    "SESSION_SEQUENCE",
    "SESSION_TITLE",
    "SESSION_DESCRIPTION",
    "SESSION_LOCATION",
    "SESSION_DATE",
    "SESSION_START_TIME",
    "SESSION_END_TIME",
    "HAS_SESSION_INFO",
]

session_counts = (
    sessions.loc[sessions["HAS_SESSION_INFO"].eq("Y"), session_cols]
    .drop_duplicates()
    .groupby("subject_key", as_index=False)
    .size()
    .rename(columns={"size": "sessions_for_subject"})
)

# Aggregate to sponsor level
agg = (
    sponsor_subjects
    .merge(session_counts, on="subject_key", how="left")
    .assign(sessions_for_subject=lambda d: d["sessions_for_subject"].fillna(0))
    .groupby("sponsor_key", as_index=False)
    .agg(
        number_of_iap_sessions_hosted=("sessions_for_subject", "sum"),
        number_of_unique_subjects_organized=("subject_key", "nunique"),
    )
)

# Attach sponsor names and format final answer
sponsor_names = sponsors[["sponsor_key", "SPONSOR_NAME"]].drop_duplicates()

out = (
    sponsor_names
    .merge(agg, on="sponsor_key", how="left")
    .fillna({
        "number_of_iap_sessions_hosted": 0,
        "number_of_unique_subjects_organized": 0,
    })
)

out["number_of_iap_sessions_hosted"] = out["number_of_iap_sessions_hosted"].astype(int)
out["number_of_unique_subjects_organized"] = out["number_of_unique_subjects_organized"].astype(int)

out = (
    out.rename(columns={"SPONSOR_NAME": "sponsor_name"})
    [["sponsor_name", "number_of_iap_sessions_hosted", "number_of_unique_subjects_organized"]]
    .sort_values("sponsor_name", na_position="last")
    .reset_index(drop=True)
)

result = {"sponsor_iap_summary": out}
