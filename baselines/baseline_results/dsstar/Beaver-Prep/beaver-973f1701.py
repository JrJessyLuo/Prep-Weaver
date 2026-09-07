import pandas as pd

# Input tables are provided in `tables` dict
df = tables['table_2']  # CIS_COURSE_CATALOG.pkl

# Reproduce department search logic from the reference code
dept_cols = [c for c in df.columns if any(k in c.upper() for k in [
    "DEPT", "DEPARTMENT", "OFFER", "UNIT", "CENTER", "CENTRE", "INSTITUTE", "DIVISION"
])]

priority_cols = [
    "OFFER_DEPT_NAME", "DEPARTMENT_NAME", "OFFER_DEPARTMENT_NAME",
    "DEPT_NAME", "DEPARTMENT", "DEPARTMENT_DESC",
    "UNIT_NAME", "CENTER_NAME", "CENTRE_NAME", "DIVISION_NAME",
    "OFFER_DEPT_CODE", "DEPARTMENT_CODE"
]
priority_cols = [c for c in priority_cols if c in df.columns]
search_cols = priority_cols if priority_cols else dept_cols

if not search_cols:
    filtered_any = df.iloc[0:0]
else:
    needle = "international studies"
    contains_any = None
    for col in search_cols:
        series_contains = df[col].astype(str).str.casefold().str.contains(needle, na=False)
        contains_any = series_contains if contains_any is None else (contains_any | series_contains)
    filtered_any = df[contains_any] if contains_any is not None else df.iloc[0:0]

# If no direct department match found (as in reference run), fall back to join paths
# Goal: For each building key, building name and number of courses offered by Center for International Studies

# Start from all courses, tag those offered by "Center for International Studies"
# Try to infer offering unit by joining with SUBJECT_OFFERED tables if needed
df_courses = df.copy()

# Derive an "offering unit" candidate column similar to search_cols
offering_cols = search_cols if search_cols else []
# If none, attempt to enrich via SUBJECT_OFFERED-like tables
so_candidates = []
for key in ['table_5', 'table_6', 'table_8', 'table_9']:
    if key in tables:
        so_candidates.append(tables[key])

# Try to left-merge sequentially on common course identifiers to bring in department/unit fields
# Identify possible join keys
possible_keys = [
    ["MASTER_SUBJECT_ID"],
    ["PRINT_SUBJECT_ID"],
    ["SUBJECT_ID"],
    ["SUBJECT_CODE", "SUBJECT_NUMBER"],
]

enriched = df_courses.copy()
for so in so_candidates:
    # find overlap keys
    for keys in possible_keys:
        if all(k in enriched.columns for k in keys) and all(k in so.columns for k in keys):
            # perform merge bringing only dept-like columns
            so_dept_cols = [c for c in so.columns if any(k in c.upper() for k in [
                "DEPT", "DEPARTMENT", "OFFER", "UNIT", "CENTER", "CENTRE", "INSTITUTE", "DIVISION"
            ])]
            so_pick = list(dict.fromkeys(keys + so_dept_cols))
            so_small = so[so_pick].copy()
            # avoid column clashes by suffixes
            enriched = enriched.merge(so_small, on=keys, how="left", suffixes=("", f"_{'_'.join(keys)}"))
            # update offering_cols with any new dept-like columns
            new_cols = [c for c in enriched.columns if any(k in c.upper() for k in [
                "DEPT", "DEPARTMENT", "OFFER", "UNIT", "CENTER", "CENTRE", "INSTITUTE", "DIVISION"
            ])]
            offering_cols = list(dict.fromkeys(offering_cols + new_cols))

# Build mask for "Center for International Studies" across any offering columns
cis_needle = "center for international studies"
mask = None
for col in offering_cols:
    m = enriched[col].astype(str).str.casefold().str.contains(cis_needle, na=False)
    mask = m if mask is None else (mask | m)

cis_courses = enriched[mask] if mask is not None else enriched.iloc[0:0]

# Map courses to buildings via room/space/building relationships
# We will attempt multiple reasonable join paths depending on available columns:
# - From course to room/building via scheduled location-like columns if exist
# - Or via SPACE_DETAIL / FAC_ROOMS / FAC_BUILDING / BUILDINGS

# Start with space/room/building dataframes
fac_rooms = tables.get('table_3', pd.DataFrame()).copy()
fac_building = tables.get('table_4', pd.DataFrame()).copy()
buildings = tables.get('table_1', pd.DataFrame()).copy()
fclt_building = tables.get('table_7', pd.DataFrame()).copy()
space_detail = tables.get('table_10', pd.DataFrame()).copy()

# Normalize likely building key and name columns
# Try common names
bldg_key_cols = [c for c in buildings.columns if any(k in c.upper() for k in ["BLDG_KEY", "BUILDING_KEY", "FACILITY_KEY", "BLDG_ID", "BUILDING_ID"])]
bldg_name_cols = [c for c in buildings.columns if any(k in c.upper() for k in ["BLDG_NAME", "BUILDING_NAME", "FACILITY_NAME", "BLDG_TITLE", "NAME"])]
bldg_key_col = bldg_key_cols[0] if bldg_key_cols else None
bldg_name_col = bldg_name_cols[0] if bldg_name_cols else None

# Collect possible relationships to get building key for each course
course_with_bldg = cis_courses.copy()
course_with_bldg['_TMP_HAS_BLDG'] = False

# Helper to append building key via join
def attach_building(df_left, right_df, left_keys, right_keys, right_bldg_col):
    if df_left.empty or right_df.empty or right_bldg_col is None:
        return df_left
    common_left = [k for k in left_keys if k in df_left.columns]
    common_right = [k for k in right_keys if k in right_df.columns]
    if len(common_left) != len(left_keys) or len(common_right) != len(right_keys):
        return df_left
    rcols = list(dict.fromkeys(right_keys + [right_bldg_col]))
    merged = df_left.merge(right_df[rcols], left_on=left_keys, right_on=right_keys, how="left")
    # If building column name clashes, ensure we have it
    if right_bldg_col not in merged.columns:
        return df_left
    # Mark rows that gained a building key
    got = merged[right_bldg_col].notna()
    merged.loc[got, '_TMP_HAS_BLDG'] = True
    return merged

# Guess building key in FAC_BUILDING and FAC_ROOMS
fac_bldg_key_cols = [c for c in fac_building.columns if any(k in c.upper() for k in ["BLDG_KEY", "BUILDING_KEY", "FACILITY_KEY", "BLDG_ID", "BUILDING_ID"])]
fac_room_bldg_key_cols = [c for c in fac_rooms.columns if any(k in c.upper() for k in ["BLDG_KEY", "BUILDING_KEY", "FACILITY_KEY", "BLDG_ID", "BUILDING_ID"])]
fac_room_key_cols = [c for c in fac_rooms.columns if any(k in c.upper() for k in ["ROOM_KEY", "ROOM_ID", "SPACE_KEY", "SPACE_ID"])]

# Try to link courses to rooms via common schedule columns
possible_course_room_keys = [
    ["ROOM_KEY"],
    ["ROOM_ID"],
    ["SPACE_KEY"],
    ["SPACE_ID"],
    ["BLDG_KEY", "ROOM_NUMBER"],
    ["BUILDING_KEY", "ROOM_NUMBER"],
]

# Attach building from FAC_ROOMS directly if course has room keys
attached = course_with_bldg
for keys in possible_course_room_keys:
    # Determine right-side match keys
    right_keys = []
    for k in keys:
        if k in fac_rooms.columns:
            right_keys.append(k)
        else:
            # Map (BLDG_KEY, ROOM_NUMBER) pattern
            if k in ["BLDG_KEY", "BUILDING_KEY"] and fac_room_bldg_key_cols:
                right_keys.append(fac_room_bldg_key_cols[0])
            elif k == "ROOM_NUMBER" and "ROOM_NUMBER" in fac_rooms.columns:
                right_keys.append("ROOM_NUMBER")
            else:
                right_keys.append(None)
    if any(v is None for v in right_keys):
        continue
    right_bldg_col = fac_room_bldg_key_cols[0] if fac_room_bldg_key_cols else None
    attached = attach_building(attached, fac_rooms, keys, right_keys, right_bldg_col)

course_with_bldg = attached

# If still missing building, try SPACE_DETAIL -> FAC_BUILDING to get building
if not course_with_bldg.empty and not course_with_bldg['_TMP_HAS_BLDG'].all():
    space_key_cols = [c for c in space_detail.columns if any(k in c.upper() for k in ["SPACE_KEY", "ROOM_KEY", "ROOM_ID", "SPACE_ID"])]
    space_bldg_key_cols = [c for c in space_detail.columns if any(k in c.upper() for k in ["BLDG_KEY", "BUILDING_KEY", "FACILITY_KEY", "BLDG_ID", "BUILDING_ID"])]
    # Try attach from SPACE_DETAIL first
    attached2 = course_with_bldg
    for k in ["SPACE_KEY", "ROOM_KEY", "ROOM_ID", "SPACE_ID"]:
        if k in attached2.columns and any(s == k for s in space_key_cols):
            right_bldg = space_bldg_key_cols[0] if space_bldg_key_cols else None
            attached2 = attach_building(attached2, space_detail, [k], [k], right_bldg)
    course_with_bldg = attached2

# Standardize final building key column name
# Prefer to use the buildings' key column name
final_bldg_key_col = None
candidate_bldg_cols = [c for c in course_with_bldg.columns if any(k in c.upper() for k in ["BLDG_KEY", "BUILDING_KEY", "FACILITY_KEY", "BLDG_ID", "BUILDING_ID"])]
if bldg_key_col and bldg_key_col in candidate_bldg_cols:
    final_bldg_key_col = bldg_key_col
elif candidate_bldg_cols:
    final_bldg_key_col = candidate_bldg_cols[0]

# Aggregate count of courses by building key
if final_bldg_key_col is None or course_with_bldg.empty:
    agg = pd.DataFrame(columns=["BUILDING_KEY", "BUILDING_NAME", "COURSE_COUNT"])
else:
    counts = course_with_bldg.dropna(subset=[final_bldg_key_col]).groupby(final_bldg_key_col, dropna=False).size().reset_index(name="COURSE_COUNT")
    # Attach building name
    if not buildings.empty and bldg_key_col and bldg_name_col:
        bnames = buildings[[bldg_key_col, bldg_name_col]].drop_duplicates()
        merged_counts = counts.merge(bnames, left_on=final_bldg_key_col, right_on=bldg_key_col, how="left")
        agg = merged_counts[[final_bldg_key_col, bldg_name_col, "COURSE_COUNT"]].rename(columns={
            final_bldg_key_col: "BUILDING_KEY",
            bldg_name_col: "BUILDING_NAME"
        })
    else:
        agg = counts.rename(columns={final_bldg_key_col: "BUILDING_KEY"})
        agg["BUILDING_NAME"] = pd.NA
        agg = agg[["BUILDING_KEY", "BUILDING_NAME", "COURSE_COUNT"]]

# Ensure data types are friendly
result_df = agg.sort_values(["COURSE_COUNT", "BUILDING_KEY"], ascending=[False, True]).reset_index(drop=True)

# Assign final result mapping name to DataFrame
result = {
    "cis_courses_by_building": result_df
}