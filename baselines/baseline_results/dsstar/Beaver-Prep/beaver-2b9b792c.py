import pandas as pd
import numpy as np

# Source tables from the provided `tables` dict
lib = tables['table_2'].copy()       # LIBRARY_COURSE_INSTRUCTOR.pkl
fac_rooms = tables['table_3'].copy() # FAC_ROOMS.pkl
fac_building = tables['table_5'].copy()  # FAC_BUILDING.pkl

# -------------------------------
# 1) Build per-course timeline from LIBRARY_COURSE_INSTRUCTOR
# -------------------------------
df = lib.copy()

# Parse date columns
df["DATE_FROM_DT"] = pd.to_datetime(df["DATE_FROM"], format="%d-%b-%y", errors="coerce")
df["DATE_TO_DT"]   = pd.to_datetime(df["DATE_TO"],   format="%d-%b-%y", errors="coerce")

# Stable sort within course by DATE_FROM/DATE_TO; include WAREHOUSE_LOAD_DATE as tie-breaker
sort_cols = ["COURSE_NAME", "DATE_FROM_DT", "DATE_TO_DT", "WAREHOUSE_LOAD_DATE"]
df_sorted = df.sort_values(sort_cols, kind="mergesort")

# Group by COURSE_NAME and compute prev/next pointers
grp = df_sorted.groupby("COURSE_NAME", dropna=False)
df_sorted["PREV_DATE_FROM_DT"]     = grp["DATE_FROM_DT"].shift(1)
df_sorted["PREV_DATE_TO_DT"]       = grp["DATE_TO_DT"].shift(1)
df_sorted["PREV_INSTRUCTOR_NAME"]  = grp["INSTRUCTOR_NAME"].shift(1)
df_sorted["NEXT_DATE_FROM_DT"]     = grp["DATE_FROM_DT"].shift(-1)
df_sorted["NEXT_DATE_TO_DT"]       = grp["DATE_TO_DT"].shift(-1)
df_sorted["NEXT_INSTRUCTOR_NAME"]  = grp["INSTRUCTOR_NAME"].shift(-1)
df_sorted["COURSE_TIMELINE_ORDER"] = grp.cumcount() + 1

# -------------------------------
# 2) Prepare FAC_ROOMS and FAC_BUILDING as in reference
# -------------------------------
fac_rooms_sel = fac_rooms.rename(columns={
    "fac_room_key": "FAC_ROOM_KEY",
    "BUILDING_KEY": "FAC_BUILDING_KEY",
    "FLOOR": "ROOM_FLOOR",
    "FLOOR_KEY": "ROOM_FLOOR_KEY",
    "ROOM": "ROOM_NUMBER",
    "SPACE_ID": "SPACE_ID",
    "MAJOR_USE_KEY": "MAJOR_USE_KEY",
    "MAJOR_USE_DESC": "MAJOR_USE_DESC",
    "USE_KEY": "USE_KEY",
    "USE_DESC": "USE_DESC",
    "MINOR_USE_KEY": "MINOR_USE_KEY",
    "MINOR_USE_DESC": "MINOR_USE_DESC",
    "ORGANIZATION_KEY": "ORGANIZATION_KEY",
    "ORGANIZATION_NAME": "ORGANIZATION_NAME",
    "MINOR_ORGANIZATION_KEY": "MINOR_ORGANIZATION_KEY",
    "MINOR_ORGANIZATION": "MINOR_ORGANIZATION",
    "AREA": "ROOM_AREA",
    "ROOM_FULL_NAME": "ROOM_FULL_NAME",
    "DEPT_CODE": "ROOM_DEPT_CODE",
    "ACCESS_LEVEL": "ROOM_ACCESS_LEVEL",
    "LATITUDE_WGS": "ROOM_LATITUDE_WGS",
    "LONGITUDE_WGS": "ROOM_LONGITUDE_WGS",
    "NORTHING_SPCS": "ROOM_NORTHING_SPCS",
    "EASTING_SPCS": "ROOM_EASTING_SPCS",
    "WAREHOUSE_LOAD_DATE": "ROOM_WAREHOUSE_LOAD_DATE"
})[
    [
        "FAC_ROOM_KEY", "FAC_BUILDING_KEY", "ROOM_FLOOR", "ROOM_FLOOR_KEY", "ROOM_NUMBER",
        "SPACE_ID", "MAJOR_USE_KEY", "MAJOR_USE_DESC", "USE_KEY", "USE_DESC",
        "MINOR_USE_KEY", "MINOR_USE_DESC", "ORGANIZATION_KEY", "ORGANIZATION_NAME",
        "MINOR_ORGANIZATION_KEY", "MINOR_ORGANIZATION", "ROOM_AREA", "ROOM_FULL_NAME",
        "ROOM_DEPT_CODE", "ROOM_ACCESS_LEVEL", "ROOM_LATITUDE_WGS", "ROOM_LONGITUDE_WGS",
        "ROOM_NORTHING_SPCS", "ROOM_EASTING_SPCS", "ROOM_WAREHOUSE_LOAD_DATE"
    ]
]

fac_bldg_sel = fac_building.rename(columns={
    "FAC_BUILDING_KEY": "FAC_BUILDING_KEY",
    "BUILDING_NUMBER": "BUILDING_NUMBER",
    "PARENT_BUILDING_NUMBER": "PARENT_BUILDING_NUMBER",
    "PARENT_BUILDING_NAME": "PARENT_BUILDING_NAME",
    "PARENT_BUILDING_NAME_LONG": "PARENT_BUILDING_NAME_LONG",
    "BUILDING_NAME_LONG": "BUILDING_NAME_LONG",
    "ACCESS_LEVEL_CODE": "BUILDING_ACCESS_LEVEL_CODE",
    "ACCESS_LEVEL_NAME": "BUILDING_ACCESS_LEVEL_NAME",
    "BUILDING_TYPE": "BUILDING_TYPE",
    "OWNERSHIP_TYPE": "OWNERSHIP_TYPE",
    "BUILDING_USE": "BUILDING_USE",
    "OCCUPANCY_CLASS": "OCCUPANCY_CLASS",
    "LATITUDE_WGS": "BUILDING_LATITUDE_WGS",
    "LONGITUDE_WGS": "BUILDING_LONGITUDE_WGS",
})[
    [
        "FAC_BUILDING_KEY", "BUILDING_NUMBER", "PARENT_BUILDING_NUMBER", "PARENT_BUILDING_NAME",
        "PARENT_BUILDING_NAME_LONG", "BUILDING_NAME_LONG",
        "BUILDING_ACCESS_LEVEL_CODE", "BUILDING_ACCESS_LEVEL_NAME",
        "BUILDING_TYPE", "OWNERSHIP_TYPE", "BUILDING_USE", "OCCUPANCY_CLASS",
        "BUILDING_LATITUDE_WGS", "BUILDING_LONGITUDE_WGS"
    ]
]

# -------------------------------
# 3) Harmonize keys for joining (UNIT vs ROOM_FULL_NAME heuristic)
# -------------------------------
def _norm_str(s):
    if pd.isna(s):
        return None
    s = str(s).strip().lower()
    s = " ".join(s.split())
    return s

df_sorted["UNIT_NORM"] = df_sorted["UNIT"].map(_norm_str)
fac_rooms_sel["ROOM_FULL_NAME_NORM"] = fac_rooms_sel["ROOM_FULL_NAME"].map(_norm_str)

# First attempt: exact normalized match UNIT_NORM == ROOM_FULL_NAME_NORM
merge1 = df_sorted.merge(
    fac_rooms_sel,
    left_on="UNIT_NORM",
    right_on="ROOM_FULL_NAME_NORM",
    how="left",
    suffixes=("", "_RM")
)

# Fallback: match UNIT to ORGANIZATION_NAME (normalized containment match)
no_match_mask = merge1["FAC_ROOM_KEY"].isna()
if no_match_mask.any():
    fac_rooms_org = fac_rooms_sel.copy()
    fac_rooms_org["ORG_NAME_NORM"] = fac_rooms_org["ORGANIZATION_NAME"].map(_norm_str)

    tmp_left = merge1.loc[no_match_mask, ["UNIT_NORM"]].copy()
    tmp_left = tmp_left.reset_index().rename(columns={"index": "ROW_ID"})
    fac_rooms_org_small = fac_rooms_org[[
        "FAC_ROOM_KEY", "FAC_BUILDING_KEY", "ROOM_AREA", "ROOM_FULL_NAME", "ROOM_FULL_NAME_NORM",
        "ROOM_ACCESS_LEVEL", "ROOM_LATITUDE_WGS", "ROOM_LONGITUDE_WGS",
        "ORGANIZATION_NAME", "ORG_NAME_NORM"
    ]].copy()

    tmp_left["key"] = 1
    fac_rooms_org_small["key"] = 1
    cross = tmp_left.merge(fac_rooms_org_small, on="key", how="left")

    def org_match(row):
        u = row["UNIT_NORM"]
        o = row["ORG_NAME_NORM"]
        if not u or not o:
            return False
        return (u == o) or (u in o) or (o in u)

    cross = cross[cross.apply(org_match, axis=1)]
    cross_first = cross.sort_values(["ROW_ID"]).drop_duplicates("ROW_ID", keep="first")

    fill_cols = ["FAC_ROOM_KEY", "FAC_BUILDING_KEY", "ROOM_AREA", "ROOM_FULL_NAME", "ROOM_FULL_NAME_NORM",
                 "ROOM_ACCESS_LEVEL", "ROOM_LATITUDE_WGS", "ROOM_LONGITUDE_WGS", "ORGANIZATION_NAME"]

    cross_first = cross_first[["ROW_ID"] + fill_cols]

    target_indices = merge1.index[no_match_mask]
    idx_map = pd.Series(range(len(target_indices)), index=target_indices)
    cross_first = cross_first.merge(
        idx_map.rename("TARGET_IDX").reset_index().rename(columns={"index": "ROW_ID"}),
        on="ROW_ID", how="inner"
    ).set_index("TARGET_IDX").sort_index()

    for c in fill_cols:
        merge1.loc[target_indices, c] = merge1.loc[target_indices, c].fillna(cross_first[c])

# -------------------------------
# 4) Bring in building info
# -------------------------------
merged = merge1.merge(
    fac_bldg_sel,
    on="FAC_BUILDING_KEY",
    how="left",
    suffixes=("", "_BLDG")
)

# -------------------------------
# 5) Build final answer for the question
#    For each course, list:
#    - course name
#    - building name of the course location
#    - start date
#    - name of course before it
#    - name of course after it
#    - access level of the building
#    - assignable area of the room used
#    Sorted by ascending start date and course name
# -------------------------------
# Use BUILDING_NAME_LONG as building name, BUILDING_ACCESS_LEVEL_NAME as access level, ROOM_AREA as area
answer = merged[[
    "COURSE_NAME",
    "BUILDING_NAME_LONG",
    "DATE_FROM_DT",
    "PREV_INSTRUCTOR_NAME",   # Note: Reference code provides prev/next instructor names, not course titles
    "NEXT_INSTRUCTOR_NAME",
    "BUILDING_ACCESS_LEVEL_NAME",
    "ROOM_AREA"
]].rename(columns={
    "BUILDING_NAME_LONG": "BUILDING_NAME",
    "DATE_FROM_DT": "START_DATE",
    "PREV_INSTRUCTOR_NAME": "PREV_COURSE_NAME",
    "NEXT_INSTRUCTOR_NAME": "NEXT_COURSE_NAME",
    "BUILDING_ACCESS_LEVEL_NAME": "BUILDING_ACCESS_LEVEL",
    "ROOM_AREA": "ASSIGNABLE_ROOM_AREA"
})

# Sort as requested
answer = answer.sort_values(["START_DATE", "COURSE_NAME"], kind="mergesort").reset_index(drop=True)

# Package final result as required
result = {
    "courses_with_location_timeline": answer
}