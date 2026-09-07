import pandas as pd
import re

# Input tables already provided in `tables`
df = tables['table_2'].copy()

# Ensure required columns exist; infer reasonable identifiers if needed
# Columns we may rely on:
# - MEET_PLACE: meeting place string (from SUBJECT_OFFERED.pkl per reference)
# - SECTION_ID or SUBJECT_KEY: identifier for a section
# - SUBJECT_ID or SUBJECT_NUMBER/SUBJECT_KEY: identifier for a course
# - LEVEL or COURSE_LEVEL-like column for Graduate/Undergraduate (we'll derive if available)
# - INSTRUCTOR or instructor join via LIBRARY_COURSE_INSTRUCTOR if needed
cols = df.columns.astype(str).tolist()

# Choose section identifier
section_id_col = "SECTION_ID" if "SECTION_ID" in df.columns else ("SUBJECT_KEY" if "SUBJECT_KEY" in df.columns else None)

# Choose course identifier (unique course). Prefer SUBJECT_ID, then SUBJECT_NUMBER, then SUBJECT_KEY
if "SUBJECT_ID" in df.columns:
    course_id_col = "SUBJECT_ID"
elif "SUBJECT_NUMBER" in df.columns:
    course_id_col = "SUBJECT_NUMBER"
elif "SUBJECT_KEY" in df.columns:
    course_id_col = "SUBJECT_KEY"
else:
    # Fallback: use combination of possibly title + number if exists; else use section id which may overcount
    course_id_col = section_id_col

# Determine level column: try typical fields
level_col = None
for cand in ["LEVEL", "COURSE_LEVEL", "COURSE_LEVEL_DESC", "SUBJECT_LEVEL", "UG_GRAD_LEVEL"]:
    if cand in df.columns:
        level_col = cand
        break

# Normalize a Graduate/Undergraduate label
def normalize_level(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip().lower()
    if not s:
        return pd.NA
    # Match typical patterns
    if any(k in s for k in ["grad", "graduate", "g"]):
        return "Graduate"
    if any(k in s for k in ["undergrad", "undergraduate", "u", "ug"]):
        return "Undergraduate"
    # Sometimes numeric course levels imply UG/GR (e.g., MIT 0xx/1xx-4xx undergrad, 5xx+ grad)
    # Try to parse from subject number if available and no explicit label
    return pd.NA

if level_col is None:
    df["_course_level"] = pd.NA
else:
    df["_course_level"] = df[level_col].map(normalize_level)

# If still missing many levels, try to infer from SUBJECT_NUMBER if present and looks numeric prefix
if df["_course_level"].isna().all() and "SUBJECT_NUMBER" in df.columns:
    def infer_from_number(v):
        if pd.isna(v):
            return pd.NA
        s = str(v).strip()
        m = re.match(r"^(\d+)", s)
        if not m:
            return pd.NA
        num = int(m.group(1))
        # Heuristic: MIT numbering isn't strictly numeric for UG/GR, but a coarse rule:
        # Treat numbers < 500 as Undergraduate, >= 500 as Graduate (common in many catalogs)
        return "Undergraduate" if num < 500 else "Graduate"
    df["_course_level"] = df["_course_level"].fillna(df["SUBJECT_NUMBER"].map(infer_from_number))

# Reference code logic to parse on-campus building codes from MEET_PLACE
room_token_pattern = re.compile(r"^[A-Za-z]?\d+[A-Za-z]?(?:-\w+)$")
non_building_keywords = {
    "remote", "online", "zoom", "web", "webinar", "internet", "virtual",
    "tba", "to be announced", "arr", "arranged", "by arrangement",
    "off campus", "off-campus", "na", "n/a", "none", "unspecified", "unknown"
}

def classify_meet_place(value: str):
    if pd.isna(value):
        return "non_building_or_online", []
    s = str(value).strip()
    if not s:
        return "non_building_or_online", []
    tokens = re.split(r"[,\;/]+", s)
    tokens = [t.strip() for t in tokens if t.strip()]
    if not tokens:
        return "non_building_or_online", []
    def is_non_building(tok: str) -> bool:
        low = tok.lower()
        if low in non_building_keywords:
            return True
        for kw in non_building_keywords:
            if kw in low:
                return True
        if re.fullmatch(r"(tbd|tbc)", low):
            return True
        return False
    def is_building_room(tok: str) -> bool:
        return bool(room_token_pattern.match(tok))
    flags = []
    for tok in tokens:
        if is_building_room(tok):
            flags.append("building")
        elif is_non_building(tok):
            flags.append("non_building")
        else:
            inner = re.search(r"[A-Za-z]?\d+[A-Za-z]?(?:-\w+)", tok)
            if inner:
                flags.append("building")
            else:
                flags.append("unknown")
    if all(f == "building" for f in flags):
        category = "on_campus_building"
    elif all(f in ("non_building",) for f in flags):
        category = "non_building_or_online"
    elif any(f == "building" for f in flags) and any(f != "building" for f in flags):
        category = "mixed"
    else:
        category = "unknown_format"
    return category, tokens

cat_tokens = df["MEET_PLACE"].astype("string").map(lambda v: classify_meet_place(v))
df["_meet_place_category"] = cat_tokens.map(lambda x: x[0])
df["_meet_place_tokens"] = cat_tokens.map(lambda x: x[1])

building_code_regex = re.compile(r"^([A-Za-z]?\d+[A-Za-z]?)-")
def extract_building_code_from_tokens(tokens):
    if not tokens:
        return pd.NA
    for tok in tokens:
        m = building_code_regex.match(tok)
        if m:
            return m.group(1)
        inner = re.search(r"([A-Za-z]?\d+[A-Za-z]?)-\w+", tok)
        if inner:
            return inner.group(1)
    return pd.NA

df["MEET_BUILDING_CODE"] = pd.NA
mask_oncampus = df["_meet_place_category"] == "on_campus_building"
df.loc[mask_oncampus, "MEET_BUILDING_CODE"] = df.loc[mask_oncampus, "_meet_place_tokens"].map(extract_building_code_from_tokens)

# Keep only on-campus rows with parsed building code and known course level
df_oncampus = df.loc[mask_oncampus & df["MEET_BUILDING_CODE"].notna()].copy()
df_oncampus["_course_level"] = df_oncampus["_course_level"].fillna("Unknown")

# Instructors: try to use LIBRARY_COURSE_INSTRUCTOR to count instructors per course if present
instructor_df = tables['table_3'].copy()
instructor_cols = instructor_df.columns.astype(str).tolist()

# Find join key to map to course; prefer SUBJECT_ID/NUMBER/KEY present in both
join_key = None
for k in [course_id_col, "SUBJECT_ID", "SUBJECT_NUMBER", "SUBJECT_KEY"]:
    if (k is not None) and (k in instructor_df.columns) and (k in df_oncampus.columns):
        join_key = k
        break

# Derive instructor identifier column
instr_id_col = None
for k in ["INSTRUCTOR_ID", "INSTRUCTOR_KEY", "PERSON_ID", "KERBEROS_ID", "INSTRUCTOR_NAME", "NAME"]:
    if k in instructor_df.columns:
        instr_id_col = k
        break

if join_key is not None and instr_id_col is not None:
    # Map course -> set of instructors
    inst_map = (
        instructor_df[[join_key, instr_id_col]]
        .dropna()
        .drop_duplicates()
    )
    # Prepare on-campus subset of course-building-level unique relationships
    base = df_oncampus[[ "MEET_BUILDING_CODE", "_course_level", course_id_col ]].dropna().drop_duplicates()
    # Join to instructor list
    base_inst = base.merge(inst_map, left_on=course_id_col, right_on=join_key, how="left")
    # Count unique instructors per group
    agg_inst = (
        base_inst.groupby(["MEET_BUILDING_CODE", "_course_level"], dropna=False)[instr_id_col]
        .nunique()
        .reset_index(name="Total Instructors")
    )
else:
    # Fallback: if no instructor table or keys, try to count unique instructor names in SUBJECT_OFFERED if exists
    subj_instr_col = None
    for k in ["INSTRUCTOR", "INSTRUCTORS", "INSTRUCTOR_NAME", "PRIMARY_INSTRUCTOR", "PRIMARY_INSTRUCTOR_NAME"]:
        if k in df_oncampus.columns:
            subj_instr_col = k
            break
    if subj_instr_col:
        base = df_oncampus[["MEET_BUILDING_CODE", "_course_level", course_id_col, subj_instr_col]].dropna(subset=[course_id_col])
        agg_inst = (
            base.groupby(["MEET_BUILDING_CODE", "_course_level"], dropna=False)[subj_instr_col]
            .nunique()
            .reset_index(name="Total Instructors")
        )
    else:
        # If no instructor info at all, set instructors to 0
        agg_inst = (
            df_oncampus.assign(_dummy=0)
            .groupby(["MEET_BUILDING_CODE", "_course_level"], dropna=False)["_dummy"]
            .sum()
            .reset_index(name="Total Instructors")
        )

# Count unique courses per building and level
unique_courses = (
    df_oncampus.dropna(subset=[course_id_col])
    .groupby(["MEET_BUILDING_CODE", "_course_level"], dropna=False)[course_id_col]
    .nunique()
    .reset_index(name="Total Unique Courses")
)

# Merge counts
summary = unique_courses.merge(
    agg_inst, on=["MEET_BUILDING_CODE", "_course_level"], how="left"
).fillna({"Total Instructors": 0})

# Prepare subtotals per building (summing across levels)
building_subtotals = (
    summary.groupby("MEET_BUILDING_CODE", as_index=False)[["Total Unique Courses", "Total Instructors"]]
    .sum()
)
building_subtotals["_course_level"] = "Subtotal"
building_subtotals = building_subtotals[["MEET_BUILDING_CODE", "_course_level", "Total Unique Courses", "Total Instructors"]]

# Grand total
grand_total = pd.DataFrame({
    "MEET_BUILDING_CODE": ["Grand Total"],
    "_course_level": ["All"],
    "Total Unique Courses": [summary["Total Unique Courses"].sum()],
    "Total Instructors": [summary["Total Instructors"].sum()]
})

# Concatenate final table with subtotals and grand total
final_table = pd.concat([summary, building_subtotals, grand_total], ignore_index=True)

# Rename columns to match requested naming
final_table = final_table.rename(columns={
    "MEET_BUILDING_CODE": "Building",
    "_course_level": "Course Level"
})

# Sort: by Building (with Grand Total last), and Course Level with Subtotal at bottom per building
def sort_key_building(x):
    return (x != "Grand Total", x)

def sort_key_level(x):
    order = {"Undergraduate": 0, "Graduate": 1, "Unknown": 2, "Subtotal": 3, "All": 4}
    return order.get(x, 5)

final_table = final_table.sort_values(
    by=["Building", "Course Level"],
    key=lambda col: col.map(sort_key_building) if col.name == "Building" else col.map(sort_key_level)
).reset_index(drop=True)

# Assign to result dict
result = {
    "On-campus courses by building and level with instructors and totals": final_table
}