import pandas as pd
import numpy as np

subjects = tables["table_8"].copy()

# Keep rows with a recorded meeting place
subjects = subjects[subjects["MEET_PLACE"].notna()].copy()

# Use section enrollment when available; otherwise fall back to subject-level enrolled students
section_enrollment = pd.to_numeric(subjects.get("SECTION_ENROLLMENT_NUMBER"), errors="coerce")
subject_enrollment = pd.to_numeric(subjects.get("NUM_ENROLLED_STUDENTS"), errors="coerce")
subjects["_students"] = section_enrollment.fillna(subject_enrollment).fillna(0)

# Normalize and split meeting places in case multiple places are listed
subjects["_place"] = (
    subjects["MEET_PLACE"]
    .astype(str)
    .str.upper()
    .str.strip()
    .str.replace(r"\s*-\s*", "-", regex=True)
)

subjects = subjects.assign(_place=subjects["_place"].str.split(r"\s*(?:,|;|\band\b|/)\s*", regex=True))
subjects = subjects.explode("_place")
subjects["_place"] = subjects["_place"].astype(str).str.strip()
subjects = subjects[subjects["_place"].ne("")].copy()

# Remove duplicated subject-section/place records if present
dedup_cols = [c for c in ["SUBJECT_KEY", "TERM_CODE", "SECTION_ID", "_place"] if c in subjects.columns]
if dedup_cols:
    subjects = subjects.drop_duplicates(dedup_cols)

# Map exact room keys to building keys when possible
rooms = tables["table_9"][["fac_room_key", "BUILDING_KEY"]].dropna(subset=["fac_room_key"]).copy()
rooms["_place"] = (
    rooms["fac_room_key"]
    .astype(str)
    .str.upper()
    .str.strip()
    .str.replace(r"\s*-\s*", "-", regex=True)
)
rooms["BUILDING_KEY"] = rooms["BUILDING_KEY"].astype(str).str.upper().str.strip()
rooms = rooms.drop_duplicates("_place")

subjects = subjects.merge(
    rooms[["_place", "BUILDING_KEY"]],
    on="_place",
    how="left"
)

# Fallback: extract building number from the meeting-place string
subjects["_building_from_place"] = subjects["_place"].str.extract(r"(?:^|\b)([A-Z]*\d+[A-Z]*)\s*-", expand=False)
subjects["BUILDING_NUMBER"] = subjects["BUILDING_KEY"].fillna(subjects["_building_from_place"])
subjects = subjects[subjects["BUILDING_NUMBER"].notna()].copy()
subjects["BUILDING_NUMBER"] = subjects["BUILDING_NUMBER"].astype(str).str.upper().str.strip()

# Total students accommodated by each building
building_totals = (
    subjects.groupby("BUILDING_NUMBER", as_index=False)["_students"]
    .sum()
    .rename(columns={"_students": "students_accommodated"})
)

# Build a building-name lookup, preferring the current facilities building table
name_frames = []

if "table_5" in tables:
    b = tables["table_5"].copy()
    b["BUILDING_NUMBER"] = b["BUILDING_NUMBER"].astype(str).str.upper().str.strip()
    b["building_name"] = b["BUILDING_NAME_LONG"].fillna(b["BUILDING_NAME"])
    name_frames.append(b[["BUILDING_NUMBER", "building_name"]])

if "table_7" in tables:
    b = tables["table_7"].copy()
    b["BUILDING_NUMBER"] = b["BUILDING_NUMBER"].astype(str).str.upper().str.strip()
    b["building_name"] = b["BUILDING_NAME"]
    name_frames.append(b[["BUILDING_NUMBER", "building_name"]])

building_names = (
    pd.concat(name_frames, ignore_index=True)
    .dropna(subset=["BUILDING_NUMBER", "building_name"])
    .drop_duplicates("BUILDING_NUMBER", keep="first")
)

answer = (
    building_totals.merge(building_names, on="BUILDING_NUMBER", how="left")
    .assign(building_name=lambda d: d["building_name"].fillna(d["BUILDING_NUMBER"]))
    .sort_values("students_accommodated", ascending=False)
    .head(1)
    [["building_name", "students_accommodated"]]
    .reset_index(drop=True)
)

answer["students_accommodated"] = answer["students_accommodated"].round().astype("Int64")

result = {
    "building_accommodating_most_students": answer
}
