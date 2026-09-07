import pandas as pd
import numpy as np

def norm_code(series):
    s = series.astype("string").str.strip()
    s = s.str.replace(r"\.0$", "", regex=True)
    return s.mask(s.str.lower().isin(["nan", "none", "<na>", ""]))

def clean_part(x):
    if pd.isna(x):
        return ""
    x = str(x).strip()
    if x.lower() in {"nan", "none", "<na>"}:
        return ""
    if x.endswith(".0"):
        x = x[:-2]
    return x

# Subjects that are Computer Science / EECS related and enrollable/offered
subjects = tables["table_8"].copy()
dept_name = subjects["DEPARTMENT_NAME"].astype("string")
cs_mask = dept_name.str.contains("Computer Sci", case=False, na=False)

cs_subjects = subjects[cs_mask].copy()
if "IS_OFFERED_THIS_YEAR" in cs_subjects.columns:
    offered = cs_subjects[cs_subjects["IS_OFFERED_THIS_YEAR"].astype("string").str.upper().eq("Y")]
    if not offered.empty:
        cs_subjects = offered

cs_dept_codes = set(norm_code(cs_subjects["DEPARTMENT_CODE"]).dropna().unique())
cs_subject_codes = set(norm_code(cs_subjects["SUBJECT_CODE"]).dropna().unique())
cs_codes = cs_dept_codes | cs_subject_codes

# Normalize current room tables
room_frames = []

if "table_1" in tables:
    r1 = tables["table_1"].copy()
    r1 = r1.rename(columns={
        "fac_room_key": "ROOM_KEY",
        "BUILDING_KEY": "BUILDING_KEY"
    })
    r1["BUILDING_ROOM"] = r1["ROOM_KEY"]
    room_frames.append(r1)

if "table_2" in tables:
    r2 = tables["table_2"].copy()
    r2 = r2.rename(columns={
        "FCLT_ROOM_KEY": "ROOM_KEY",
        "FCLT_BUILDING_KEY": "BUILDING_KEY"
    })
    room_frames.append(r2)

rooms = pd.concat(room_frames, ignore_index=True, sort=False)
rooms["BUILDING_KEY"] = norm_code(rooms["BUILDING_KEY"])
rooms["DEPT_CODE_NORM"] = norm_code(rooms["DEPT_CODE"])

org = rooms["ORGANIZATION_NAME"].astype("string")
room_mask = rooms["DEPT_CODE_NORM"].isin(cs_codes) | org.str.contains(
    r"\bEECS\b|Computer", case=False, na=False, regex=True
)
rooms = rooms[room_mask].copy()

rooms["room_full_name"] = rooms["ROOM_FULL_NAME"]
rooms["room_full_name"] = rooms["room_full_name"].where(
    rooms["room_full_name"].notna() & rooms["room_full_name"].astype(str).str.strip().ne(""),
    rooms["BUILDING_ROOM"].combine_first(rooms["ROOM_KEY"])
)

rooms = rooms[["room_full_name", "BUILDING_KEY"]].dropna(subset=["room_full_name", "BUILDING_KEY"])

# Normalize building tables
building_frames = []

if "table_3" in tables:
    b1 = tables["table_3"].copy()
    b1 = b1.rename(columns={"FAC_BUILDING_KEY": "BUILDING_KEY"})
    building_frames.append(b1)

if "table_6" in tables:
    b2 = tables["table_6"].copy()
    b2 = b2.rename(columns={"FCLT_BUILDING_KEY": "BUILDING_KEY"})
    building_frames.append(b2)

buildings = pd.concat(building_frames, ignore_index=True, sort=False)
buildings["BUILDING_KEY"] = norm_code(buildings["BUILDING_KEY"])
buildings["building_name"] = buildings["BUILDING_NAME"].combine_first(buildings["BUILDING_NAME_LONG"])
buildings = buildings[["BUILDING_KEY", "building_name", "BUILDING_HEIGHT"]].drop_duplicates("BUILDING_KEY")

# Choose one street address per building, preferring STREET, then E911, then MAIL
addresses = tables["table_5"].copy()
addresses["BUILDING_KEY"] = norm_code(addresses["BUILDING_KEY"])

purpose_priority = {
    "STREET": 0,
    "E911_1": 1,
    "E911_2": 2,
    "E911": 3,
    "MAIL": 4
}
addresses["address_priority"] = addresses["ADDRESS_PURPOSE"].map(purpose_priority).fillna(99)

address_parts = [
    "STREET_NUMBER",
    "STREET_NUMBER_SUFFIX",
    "PRE_DIRECTIONAL",
    "STREET_NAME",
    "STREET_SUFFIX",
    "POST_DIRECTIONAL"
]
for col in address_parts:
    if col not in addresses.columns:
        addresses[col] = np.nan

addresses["street_address"] = addresses[address_parts].apply(
    lambda row: " ".join([clean_part(v) for v in row if clean_part(v)]),
    axis=1
)

addresses["postal_code"] = addresses["POSTAL_CODE"].apply(
    lambda x: str(int(x)).zfill(5) if pd.notna(x) else pd.NA
)

addresses = (
    addresses.sort_values(["BUILDING_KEY", "address_priority"])
    .drop_duplicates("BUILDING_KEY")
    [["BUILDING_KEY", "street_address", "CITY", "STATE", "postal_code"]]
)

# Final result
out = (
    rooms
    .merge(buildings, on="BUILDING_KEY", how="left")
    .merge(addresses, on="BUILDING_KEY", how="left")
)

out = out.rename(columns={
    "BUILDING_HEIGHT": "building_height",
    "CITY": "city",
    "STATE": "state"
})

out = (
    out[[
        "room_full_name",
        "building_name",
        "street_address",
        "city",
        "state",
        "postal_code",
        "building_height"
    ]]
    .drop_duplicates()
    .sort_values(["room_full_name", "building_name"], na_position="last")
    .reset_index(drop=True)
)

result = {"cs_enrollable_subject_rooms": out}
