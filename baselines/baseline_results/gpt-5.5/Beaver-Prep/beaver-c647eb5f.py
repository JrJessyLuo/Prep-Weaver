import pandas as pd
import numpy as np
import re

sessions = tables["table_1"].copy()
subjects = tables["table_3"].copy()

def first_nonnull(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else np.nan

def normalize_time_value(x):
    if pd.isna(x):
        return pd.NA
    s = re.sub(r"[\s\.:]", "", str(x).strip().upper())
    if s in {"NOON"}:
        return "1200PM"
    if s in {"MIDNIGHT"}:
        return "1200AM"
    m = re.match(r"^(\d{1,4})([AP]M)$", s)
    if not m:
        return pd.NA
    num, ampm = m.groups()
    if len(num) <= 2:
        num = num.zfill(2) + "00"
    elif len(num) == 3:
        num = "0" + num
    return num + ampm

sessions["subject_key"] = sessions["iap_subject_session_key"].astype("string").str.strip().str.lower()

subjects["subject_key"] = subjects["IAP_SUBJECT_SESSION_KEY"].astype("string").str.strip().str.lower()
if "IS_CANCELLED" in subjects.columns:
    subjects = subjects[subjects["IS_CANCELLED"].astype("string").str.strip().str.upper().ne("Y")]

subject_meta = (
    subjects
    .groupby("subject_key", as_index=False)
    .agg(
        activity_title=("ACTIVITY_TITLE", first_nonnull),
        fee=("FEE", first_nonnull)
    )
)

df = sessions.merge(subject_meta, on="subject_key", how="left")

df["session_location_clean"] = (
    df["SESSION_LOCATION"]
    .astype("string")
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

virtual_or_nonphysical = (
    r"zoom|virtual|online|remote|webex|youtube|livestream|"
    r"google\s*meet|teams|skype|link|url|to be arranged|tba|tbd"
)

physical = df[
    df["session_location_clean"].notna()
    & ~df["session_location_clean"].str.contains(virtual_or_nonphysical, case=False, na=False, regex=True)
].copy()

physical["building_code"] = physical["session_location_clean"].str.extract(
    r"\b((?:NW|NE|SW|SE|N|E|W)?\d+[A-Z]?)\s*[-–]",
    flags=re.IGNORECASE
)[0]

physical["building_from_word"] = physical["session_location_clean"].str.extract(
    r"\b(?:building|bldg\.?)\s*((?:NW|NE|SW|SE|N|E|W)?\d+[A-Z]?)\b",
    flags=re.IGNORECASE
)[0]

physical["building_from_lobby"] = physical["session_location_clean"].str.extract(
    r"\blobby\s+(\d+[A-Z]?)\b",
    flags=re.IGNORECASE
)[0]

physical["building_name"] = (
    physical["building_code"]
    .fillna(physical["building_from_word"])
    .fillna(physical["building_from_lobby"])
    .fillna(physical["session_location_clean"])
    .astype("string")
    .str.strip()
)

code_like = physical["building_name"].str.match(r"^(?:NW|NE|SW|SE|N|E|W)?\d+[A-Z]?$", case=False, na=False)
physical.loc[code_like, "building_name"] = physical.loc[code_like, "building_name"].str.upper()

physical["start_time_norm"] = physical["SESSION_START_TIME"].map(normalize_time_value)
physical["end_time_norm"] = physical["SESSION_END_TIME"].map(normalize_time_value)

physical["session_start_dt"] = pd.to_datetime(
    physical["SESSION_DATE"].astype("string").str.strip() + " " + physical["start_time_norm"].astype("string"),
    errors="coerce"
)
physical["session_end_dt"] = pd.to_datetime(
    physical["SESSION_DATE"].astype("string").str.strip() + " " + physical["end_time_norm"].astype("string"),
    errors="coerce"
)

overnight = physical["session_end_dt"] < physical["session_start_dt"]
physical.loc[overnight, "session_end_dt"] = physical.loc[overnight, "session_end_dt"] + pd.Timedelta(days=1)

physical["session_duration_minutes"] = (
    physical["session_end_dt"] - physical["session_start_dt"]
).dt.total_seconds() / 60

physical["fee_num"] = pd.to_numeric(physical["fee"], errors="coerce").fillna(0)

subject_location = physical.drop_duplicates(["building_name", "subject_key"])

subject_agg = (
    subject_location
    .groupby("building_name", as_index=False)
    .agg(
        total_number_of_subjects=("subject_key", "nunique"),
        total_fee=("fee_num", "sum")
    )
)

duration_agg = (
    physical
    .groupby("building_name", as_index=False)
    .agg(
        shortest_session_minutes=("session_duration_minutes", "min"),
        longest_session_minutes=("session_duration_minutes", "max")
    )
)

answer = (
    subject_agg
    .merge(duration_agg, on="building_name", how="outer")
    .sort_values("building_name", kind="stable")
    .reset_index(drop=True)
)

answer = answer[
    [
        "building_name",
        "total_number_of_subjects",
        "total_fee",
        "shortest_session_minutes",
        "longest_session_minutes",
    ]
]

result = {"physical_iap_session_locations": answer}
