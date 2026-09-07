import pandas as pd
import numpy as np
import re

sections = tables["table_4"].copy()
rooms = tables["table_8"].copy()

# Courses/sections with more than 300 attendees
sections = sections[sections["NUM_ENROLLED_STUDENTS"] > 300].copy()

# Parse MEET_PLACE into building key and room.
# Handles values like "26-247D", "E51-350", and multiple/extra text by taking the first building-room token.
meet = sections["MEET_PLACE"].astype("string").str.extract(r"(?P<parsed_building_key>[A-Za-z]?\d+[A-Za-z]?)\s*-\s*(?P<parsed_room>[A-Za-z0-9]+)")
sections["parsed_building_key"] = meet["parsed_building_key"]
sections["parsed_room"] = meet["parsed_room"]
sections["fac_room_key"] = sections["parsed_building_key"].astype("string") + "-" + sections["parsed_room"].astype("string")

# Normalize join keys
sections["fac_room_key_norm"] = sections["fac_room_key"].astype("string").str.strip().str.upper()
rooms["fac_room_key_norm"] = rooms["fac_room_key"].astype("string").str.strip().str.upper()

merged = sections.merge(
    rooms[["fac_room_key_norm", "ROOM", "FLOOR", "BUILDING_KEY"]],
    on="fac_room_key_norm",
    how="left",
    suffixes=("", "_room")
)

# Prefer room/building/floor from facilities table when available; otherwise use parsed values
merged["ROOM"] = merged["ROOM"].fillna(merged["parsed_room"])
merged["BUILDING_KEY"] = merged["BUILDING_KEY"].fillna(merged["parsed_building_key"])

# Building address fields are not present in the provided schemas; include them as requested with missing values.
for col in ["BUILDING_STREET_ADDRESS", "CITY", "STATE", "POSTAL_CODE"]:
    if col not in merged.columns:
        merged[col] = pd.NA

out = merged.rename(columns={
    "TERM_CODE": "term_code",
    "SUBJECT_TITLE": "subject_title",
    "ROOM": "room",
    "FLOOR": "floor",
    "BUILDING_KEY": "building_key",
    "BUILDING_STREET_ADDRESS": "building_street_address",
    "CITY": "city",
    "STATE": "state",
    "POSTAL_CODE": "postal_code",
    "FORM_TYPE_DESC": "formats",
    "NUM_ENROLLED_STUDENTS": "number_enrolled_students"
})[
    [
        "term_code",
        "subject_title",
        "room",
        "floor",
        "building_key",
        "building_street_address",
        "city",
        "state",
        "postal_code",
        "formats",
        "number_enrolled_students",
    ]
].drop_duplicates().sort_values(
    ["term_code", "subject_title", "building_key", "room", "formats"],
    na_position="last"
).reset_index(drop=True)

result = {"courses_with_more_than_300_attendees": out}
