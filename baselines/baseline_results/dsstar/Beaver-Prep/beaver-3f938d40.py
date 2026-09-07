import pandas as pd
import re

# ---------------------------
# 0) Setup and load data from provided `tables` dict
# ---------------------------
drupal = tables['table_1']
co = tables['table_2']
rooms = tables['table_3']
rooms_hist = tables['table_4']
fac_rooms = tables['table_5']
cis = tables['table_6']
zpm = tables['table_7']
summ = tables['table_8']
iap = tables['table_9']

# ---------------------------
# 1) Helpers
# ---------------------------
def extract_first_building_room(s):
    if pd.isna(s):
        return None
    txt = str(s).strip()
    if not txt:
        return None
    first = re.split(r"[;,\n]| {2,}", txt)[0].strip()
    first = re.sub(r"[^0-9A-Za-z\-]", "", first)
    return first or None

def parse_building_from_building_room(br):
    if pd.isna(br):
        return None
    s = str(br)
    parts = s.split("-", 1)
    return parts[0].strip() if len(parts) > 1 else None

def mode_or_first(series):
    if series.empty:
        return None
    vc = series.dropna().value_counts()
    if vc.empty:
        return None
    return vc.index[0]

def derive_course_level(row):
    if "HGN_CODE" in row and pd.notna(row["HGN_CODE"]):
        return str(row["HGN_CODE"])
    num = row.get("SUBJECT_NUMBER", None)
    if pd.isna(num):
        return None
    s = str(num).strip()
    m = re.match(r"^(\d+)", s)
    if not m:
        return None
    first_digit = m.group(1)[0]
    try:
        d = int(first_digit)
    except:
        return None
    if d <= 1:
        return "UG-lower"
    if 2 <= d <= 4:
        return "UG-upper"
    if 5 <= d <= 8:
        return "Graduate"
    return "Special"

# ---------------------------
# 2) Prepare base course_offered with normalized keys
# ---------------------------
co = co.copy()

meet_col = "MEET_PLACE" if "MEET_PLACE" in co.columns else None
if not meet_col:
    cand = [c for c in co.columns if c.lower() == "meet_place"]
    if cand:
        meet_col = cand[0]
if meet_col is None:
    co["MEET_PLACE"] = None
    meet_col = "MEET_PLACE"

co["MEET_PLACE_NORM"] = co[meet_col].apply(extract_first_building_room)

if "TERM_CODE" in co.columns:
    co["TERM_CODE"] = co["TERM_CODE"].astype(str)
else:
    term_cands = [c for c in co.columns if c.lower() in ("term_code", "term")]
    if term_cands:
        co["TERM_CODE"] = co[term_cands[0]].astype(str)
    else:
        co["TERM_CODE"] = None

co_subj_id_col = None
for c in ["SUBJECT_ID", "subject_id", "Subject_ID"]:
    if c in co.columns:
        co_subj_id_col = c
        break
if co_subj_id_col is None:
    if "SUBJECT_CODE" in co.columns and "SUBJECT_NUMBER" in co.columns:
        co["SUBJECT_ID_FALLBACK"] = co["SUBJECT_CODE"].astype(str) + "-" + co["SUBJECT_NUMBER"].astype(str)
        co_subj_id_col = "SUBJECT_ID_FALLBACK"
    else:
        co["SUBJECT_ID_FALLBACK"] = co.index.astype(str)
        co_subj_id_col = "SUBJECT_ID_FALLBACK"

co[co_subj_id_col] = co[co_subj_id_col].astype(str)

if "HGN_CODE" not in co.columns:
    co["HGN_CODE"] = None
co["COURSE_LEVEL"] = co.apply(derive_course_level, axis=1)

# ---------------------------
# 3) Prepare room dimensions (augment with building meta if available)
# ---------------------------
room_dim_small = None
if rooms is not None and "BUILDING_ROOM" in rooms.columns:
    room_keep = [
        "FCLT_ROOM_KEY", "BUILDING_ROOM", "FCLT_BUILDING_KEY", "ROOM", "ROOM_FULL_NAME",
        "MAJOR_USE_DESC", "USE_DESC", "ORGANIZATION_NAME", "AREA", "ACCESS_LEVEL",
        "LATITUDE_WGS", "LONGITUDE_WGS",
        # Try to include possible building meta if present
        "BUILDING_NAME", "BUILDING_NUMBER", "BUILDING_CITY", "BUILDING_STATE"
    ]
    room_keep = [c for c in room_keep if c in rooms.columns]
    room_dim_small = rooms[room_keep].drop_duplicates().copy()
    room_dim_small["BUILDING_CODE"] = room_dim_small["BUILDING_ROOM"].apply(parse_building_from_building_room)

# If FAC_ROOMS contains better building attributes keyed by BUILDING_ROOM, merge them
if fac_rooms is not None and "BUILDING_ROOM" in fac_rooms.columns and room_dim_small is not None:
    fac_keep = ["BUILDING_ROOM", "BUILDING_NAME", "BUILDING_NUMBER", "BUILDING_CITY", "BUILDING_STATE"]
    fac_keep = [c for c in fac_keep if c in fac_rooms.columns]
    if fac_keep:
        fac_small = fac_rooms[fac_keep].drop_duplicates()
        # prefer FAC values when available
        room_dim_small = room_dim_small.merge(fac_small, on="BUILDING_ROOM", how="left", suffixes=("", "_FAC"))
        for col in ["BUILDING_NAME", "BUILDING_NUMBER", "BUILDING_CITY", "BUILDING_STATE"]:
            fac_col = f"{col}_FAC"
            if fac_col in room_dim_small.columns:
                room_dim_small[col] = room_dim_small[col].where(room_dim_small[col].notna(), room_dim_small[fac_col])
                room_dim_small.drop(columns=[fac_col], inplace=True)

zpm_dim_small = None
if zpm is not None and "BUILDING_ROOM" in zpm.columns:
    zpm_keep = ["BUILDING_ROOM", "ACCESS_LEVEL", "SPACE_USAGE", "HR_ORG_UNIT_ID", "SPACE_UNIT_CODE"]
    zpm_keep = [c for c in zpm_keep if c in zpm.columns]
    zpm_dim_small = zpm[zpm_keep].drop_duplicates().copy()
    zpm_dim_small = zpm_dim_small.add_prefix("ZPM_")

# ---------------------------
# 4) Prepare subject summary (units, enrollment, etc.)
# ---------------------------
summ_small = None
summ_subj_id_col = None
if summ is not None:
    for c in ["SUBJECT_ID", "subject_id"]:
        if c in summ.columns:
            summ_subj_id_col = c
            break
    summ_keep = [
        "TERM_CODE",
        summ_subj_id_col if summ_subj_id_col else None,
        "TOTAL_UNITS", "LECTURE_UNITS", "LAB_UNITS", "PREPARATION_UNITS",
        "SUBJECT_ENROLLMENT_NUMBER", "NUM_ENROLLED_STUDENTS",
        "SUBJECT_TITLE", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME",
        "HGN_CODE"
    ]
    summ_keep = [c for c in summ_keep if c in summ.columns]
    summ_small = summ[summ_keep].drop_duplicates().copy() if summ_keep else None
    if summ_small is not None:
        if "TERM_CODE" in summ_small.columns:
            summ_small["TERM_CODE"] = summ_small["TERM_CODE"].astype(str)
        if summ_subj_id_col:
            summ_small[summ_subj_id_col] = summ_small[summ_subj_id_col].astype(str)

# ---------------------------
# 5) Link courses -> rooms -> summary
# ---------------------------
linked = co.copy()

if room_dim_small is not None and "MEET_PLACE_NORM" in linked.columns:
    linked = linked.merge(
        room_dim_small,
        how="left",
        left_on="MEET_PLACE_NORM",
        right_on="BUILDING_ROOM",
        suffixes=("", "_ROOM")
    )

if zpm_dim_small is not None and "MEET_PLACE_NORM" in linked.columns and "ZPM_BUILDING_ROOM" in zpm_dim_small.columns:
    linked = linked.merge(
        zpm_dim_small,
        how="left",
        left_on="MEET_PLACE_NORM",
        right_on="ZPM_BUILDING_ROOM"
    )

if summ_small is not None:
    if summ_subj_id_col:
        linked = linked.merge(
            summ_small,
            how="left",
            left_on=["TERM_CODE", co_subj_id_col],
            right_on=["TERM_CODE", summ_subj_id_col],
            suffixes=("", "_SUMM")
        )
    else:
        linked = linked.merge(
            summ_small,
            how="left",
            on="TERM_CODE",
            suffixes=("", "_SUMM")
        )

if "HGN_CODE" in linked.columns:
    def refine_level(row):
        if pd.notna(row.get("HGN_CODE")):
            return str(row["HGN_CODE"])
        return row.get("COURSE_LEVEL")
    linked["COURSE_LEVEL"] = linked.apply(refine_level, axis=1)

# ---------------------------
# 6) Aggregate per course (TERM_CODE + SUBJECT_ID) with filter: no NULL meet_place and meet_time
# ---------------------------
meet_time_col = "MEET_TIME" if "MEET_TIME" in linked.columns else None
if not meet_time_col:
    mt_cands = [c for c in linked.columns if c.lower() == "meet_time"]
    if mt_cands:
        meet_time_col = mt_cands[0]
if meet_time_col is None:
    meet_time_col = "MEET_TIME"
    linked[meet_time_col] = None

# Filter: must have meet place and meet time not null
filtered = linked[
    linked["MEET_PLACE_NORM"].notna() & linked[meet_time_col].notna()
].copy()

course_keys = ["TERM_CODE", co_subj_id_col]

grp_full = filtered.groupby(course_keys, dropna=False)

agg = grp_full.agg({
    "ROOM": mode_or_first if "ROOM" in filtered.columns else (lambda x: None),
    "BUILDING_ROOM": mode_or_first if "BUILDING_ROOM" in filtered.columns else (lambda x: None),
    "AREA": "max" if "AREA" in filtered.columns else (lambda x: None),
    "ORGANIZATION_NAME": mode_or_first if "ORGANIZATION_NAME" in filtered.columns else (lambda x: None),
    "MAJOR_USE_DESC": mode_or_first if "MAJOR_USE_DESC" in filtered.columns else (lambda x: None),
    "COURSE_LEVEL": mode_or_first if "COURSE_LEVEL" in filtered.columns else (lambda x: None),
    "TOTAL_UNITS": "max" if "TOTAL_UNITS" in filtered.columns else (lambda x: None),
    "SUBJECT_TITLE": mode_or_first if "SUBJECT_TITLE" in filtered.columns else (lambda x: None),
    "OFFER_DEPT_CODE": mode_or_first if "OFFER_DEPT_CODE" in filtered.columns else (lambda x: None),
    "OFFER_DEPT_NAME": mode_or_first if "OFFER_DEPT_NAME" in filtered.columns else (lambda x: None),
    "OFFER_SCHOOL_NAME": mode_or_first if "OFFER_SCHOOL_NAME" in filtered.columns else (lambda x: None),
}).reset_index()

# Building code and building meta
if "BUILDING_ROOM" in agg.columns:
    agg["BUILDING_CODE"] = agg["BUILDING_ROOM"].apply(parse_building_from_building_room)
else:
    agg["BUILDING_CODE"] = None

# Add room full name and building meta via most frequent among filtered
add_cols = []
if "ROOM_FULL_NAME" in filtered.columns:
    add_cols.append("ROOM_FULL_NAME")
for bc in ["BUILDING_NAME", "BUILDING_NUMBER", "BUILDING_CITY", "BUILDING_STATE"]:
    if bc in filtered.columns:
        add_cols.append(bc)
if add_cols:
    extras = grp_full[add_cols].agg(mode_or_first).reset_index()
    agg = agg.merge(extras, on=course_keys, how="left")

# Counts
num_distinct_subjects = grp_full[co_subj_id_col].nunique().reset_index(name="NUM_DISTINCT_SUBJECTS")
num_unique_meet_times = grp_full[meet_time_col].nunique().reset_index(name="NUM_UNIQUE_MEET_TIMES")

course_agg = agg.merge(num_distinct_subjects, on=course_keys, how="left")
course_agg = course_agg.merge(num_unique_meet_times, on=course_keys, how="left")

if "NUM_UNIQUE_MEET_TIMES" in course_agg.columns:
    course_agg["NUM_UNIQUE_MEET_TIMES"] = course_agg["NUM_UNIQUE_MEET_TIMES"].fillna(0).astype(int)
if "NUM_DISTINCT_SUBJECTS" in course_agg.columns:
    course_agg["NUM_DISTINCT_SUBJECTS"] = course_agg["NUM_DISTINCT_SUBJECTS"].fillna(0).astype(int)

# ---------------------------
# 7) Select/rename columns to match the question
# ---------------------------
# Question wants: room number (ROOM), building name, building number, building city, building state,
# area, organization name, room usage, term code, course level, total number of subjects,
# unique meeting times, total units. Also building number (we also provide BUILDING_CODE parsed).
sel_cols = []
rename_map = {}

if "ROOM" in course_agg.columns:
    sel_cols.append("ROOM")  # room number
if "BUILDING_NAME" in course_agg.columns:
    sel_cols.append("BUILDING_NAME")
if "BUILDING_NUMBER" in course_agg.columns:
    sel_cols.append("BUILDING_NUMBER")
if "BUILDING_CITY" in course_agg.columns:
    sel_cols.append("BUILDING_CITY")
if "BUILDING_STATE" in course_agg.columns:
    sel_cols.append("BUILDING_STATE")
if "AREA" in course_agg.columns:
    sel_cols.append("AREA")
if "ORGANIZATION_NAME" in course_agg.columns:
    sel_cols.append("ORGANIZATION_NAME")
# room usage: prefer MAJOR_USE_DESC else USE_DESC if present
usage_col = "MAJOR_USE_DESC" if "MAJOR_USE_DESC" in course_agg.columns else ("USE_DESC" if "USE_DESC" in course_agg.columns else None)
if usage_col:
    sel_cols.append(usage_col)
    rename_map[usage_col] = "ROOM_USAGE"

sel_cols_prefix = ["TERM_CODE", co_subj_id_col]
tail_cols = []
if "COURSE_LEVEL" in course_agg.columns:
    tail_cols.append("COURSE_LEVEL")
if "NUM_DISTINCT_SUBJECTS" in course_agg.columns:
    tail_cols.append("NUM_DISTINCT_SUBJECTS")
if "NUM_UNIQUE_MEET_TIMES" in course_agg.columns:
    tail_cols.append("NUM_UNIQUE_MEET_TIMES")
if "TOTAL_UNITS" in course_agg.columns:
    tail_cols.append("TOTAL_UNITS")
# Optional helpful columns:
if "BUILDING_CODE" in course_agg.columns:
    tail_cols.insert(0, "BUILDING_CODE")
if "SUBJECT_TITLE" in course_agg.columns:
    tail_cols.append("SUBJECT_TITLE")
if "OFFER_DEPT_CODE" in course_agg.columns:
    tail_cols.append("OFFER_DEPT_CODE")
if "OFFER_DEPT_NAME" in course_agg.columns:
    tail_cols.append("OFFER_DEPT_NAME")
if "OFFER_SCHOOL_NAME" in course_agg.columns:
    tail_cols.append("OFFER_SCHOOL_NAME")

final_cols = [c for c in sel_cols_prefix + sel_cols + tail_cols if c in course_agg.columns]
final = course_agg[final_cols].rename(columns=rename_map).copy()

# Assign to required output variable
result = {"course_room_summary": final}