import pandas as pd
import re

# The input dataframes are provided in a dict named `tables`
# tables['table_1'] -> TIP_SUBJECT_OFFERED.pkl
# tables['table_2'] -> LIBRARY_SUBJECT_OFFERED.pkl
# tables['table_3'] -> SUBJECT_OFFERED_SUMMARY.pkl
# tables['table_4'] -> SUBJECT_OFFERED.pkl
# tables['table_5'] -> SUBJECT_ENROLLABLE.pkl
# tables['table_6'] -> IAP_SUBJECT_DETAIL.pkl
# tables['table_7'] -> COURSE_CATALOG_SUBJECT_OFFERED.pkl
# tables['table_8'] -> FAC_ROOMS.pkl
# tables['table_9'] -> SIS_SUBJECT_CODE.pkl

# Reproduce the SAME logic as the reference code, sourcing from `tables`

# Load SUBJECT_OFFERED
df = tables['table_4'].copy()

# Ensure NUM_ENROLLED_STUDENTS exists (fallback to SUMMARY if needed)
required_col = "NUM_ENROLLED_STUDENTS"
if required_col not in df.columns:
    if "SUBJECT_OFFERED_SUMMARY_KEY" in df.columns and 'table_3' in tables:
        df_sum = tables['table_3'][["SUBJECT_OFFERED_SUMMARY_KEY", "NUM_ENROLLED_STUDENTS"]].copy()
        df = df.merge(df_sum, on="SUBJECT_OFFERED_SUMMARY_KEY", how="left")
    else:
        raise KeyError("NUM_ENROLLED_STUDENTS column not found and SUBJECT_OFFERED_SUMMARY unavailable for enrichment.")

# Filter high-attendance sections
high_attendance = df.loc[df[required_col] > 300].copy()

# Select fields we need for enrichment
need_cols = [
    "TERM_CODE",
    "SUBJECT_TITLE",
    "MEET_PLACE",
    "NUM_ENROLLED_STUDENTS",
    "COURSE_NUMBER",
    "SUBJECT_ID",
    "SECTION_ID",
    "MEET_TIME",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
]
need_cols = [c for c in need_cols if c in high_attendance.columns]
enrich_df = high_attendance[need_cols].copy()

# Parse MEET_PLACE into BUILDING_KEY and ROOM
def extract_first_meet_place_token(value):
    if pd.isna(value):
        return None
    token = re.split(r"[;,/]", str(value).strip())[0].strip()
    return token or None

def parse_building_room(token):
    if not token:
        return (None, None)
    m = re.match(r"^\s*([A-Za-z0-9]+)\s*-\s*([A-Za-z0-9]+)\s*$", token)
    if m:
        return (m.group(1), m.group(2))
    m2 = re.match(r"^\s*([A-Za-z0-9]+)\s+([A-Za-z0-9]+)\s*$", token)
    if m2:
        return (m2.group(1), m2.group(2))
    return (None, None)

enrich_df["MEET_PLACE_TOKEN"] = enrich_df["MEET_PLACE"].apply(extract_first_meet_place_token)
enrich_df[["BUILDING_KEY", "ROOM"]] = enrich_df["MEET_PLACE_TOKEN"].apply(
    lambda x: pd.Series(parse_building_room(x))
)

# Load FAC_ROOMS for enrichment
fac_rooms = tables['table_8'].copy()
fac_cols = [
    "BUILDING_KEY",
    "ROOM",
    "FLOOR",
    "FLOOR_KEY",
    "ROOM_FULL_NAME",
    "MAJOR_USE_DESC",
    "USE_DESC",
    "ORGANIZATION_NAME",
    "AREA",
    "LATITUDE_WGS",
    "LONGITUDE_WGS",
    "NORTHING_SPCS",
    "EASTING_SPCS",
    # Address-related fields may or may not exist; include if present
    "BUILDING_STREET_ADDRESS",
    "CITY",
    "STATE",
    "POSTAL_CODE",
    # Sometimes address fields may have alternative names; we'll infer later if needed
]
fac_avail_cols = [c for c in fac_cols if c in fac_rooms.columns]
fac_rooms_view = fac_rooms[fac_avail_cols].drop_duplicates()

# Join on [BUILDING_KEY, ROOM]
merged = enrich_df.merge(
    fac_rooms_view,
    on=["BUILDING_KEY", "ROOM"],
    how="left",
    validate="m:1"
)

# Prepare address enrichment note (the reference mentions no address fields; we include if available)
# Create uniform address columns if they exist; otherwise set as NaN
addr_cols_map = {
    "BUILDING_STREET_ADDRESS": [c for c in ["BUILDING_STREET_ADDRESS", "STREET_ADDRESS", "ADDR_LINE1"] if c in merged.columns],
    "CITY": [c for c in ["CITY"] if c in merged.columns],
    "STATE": [c for c in ["STATE"] if c in merged.columns],
    "POSTAL_CODE": [c for c in ["POSTAL_CODE", "ZIP", "ZIP_CODE"] if c in merged.columns],
}
for out_col, src_candidates in addr_cols_map.items():
    if src_candidates:
        merged[out_col] = merged[src_candidates[0]]
    else:
        merged[out_col] = pd.NA

# Build final output with required fields
# Question asks: unique term code, subject title, room, floor, building key, building street address, city, state, and postal code, formats, and number of enrolled students
# "formats" is not explicitly present in reference code; interpret as MEET_TIME/MEET_PLACE_TOKEN context.
# We'll include MEET_TIME (if present) and MEET_PLACE_TOKEN to represent format/location token.
out_cols = [
    "TERM_CODE",
    "SUBJECT_TITLE",
    "ROOM",
    "FLOOR" if "FLOOR" in merged.columns else None,
    "BUILDING_KEY",
    "BUILDING_STREET_ADDRESS",
    "CITY",
    "STATE",
    "POSTAL_CODE",
    "MEET_TIME" if "MEET_TIME" in merged.columns else None,
    "MEET_PLACE_TOKEN",
    "NUM_ENROLLED_STUDENTS",
]
out_cols = [c for c in out_cols if c is not None and c in merged.columns]

final_df = merged[out_cols].drop_duplicates().sort_values(
    ["TERM_CODE", "NUM_ENROLLED_STUDENTS"], ascending=[True, False]
)

# Assign the final answer to `result` as required
result = {
    "high_attendance_sections_with_room_and_address": final_df
}