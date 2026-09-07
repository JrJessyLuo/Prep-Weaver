import pandas as pd
import numpy as np

# Tables are provided in 'tables' dict:
# tables['table_1'] -> FAC_ROOMS.pkl
# tables['table_5'] -> FAC_BUILDING.pkl
# tables['table_10'] -> FCLT_FLOOR.pkl
# tables['table_9'] -> SPACE_DETAIL.pkl

# 1) Load DataFrames from provided tables dict
fac_rooms = tables['table_1'].copy()
fac_building = tables['table_5'].copy()
fclt_floor = tables['table_10'].copy()
space_detail = tables['table_9'].copy() if 'table_9' in tables else pd.DataFrame()

# 2) Coerce keys to string/object for consistent join
fac_rooms["BUILDING_KEY_str"] = fac_rooms["BUILDING_KEY"].astype(str)
fac_rooms["FLOOR_KEY_str"] = fac_rooms["FLOOR_KEY"].astype(str)
fac_building["FAC_BUILDING_KEY_str"] = fac_building["FAC_BUILDING_KEY"].astype(str)
fclt_floor["FCLT_FLOOR_KEY_str"] = fclt_floor["FCLT_FLOOR_KEY"].astype(str)

# 3) Prepare dimension columns and rename to avoid collisions
# Keep building number/name and assignable area at building level
cols_building = [
    "FAC_BUILDING_KEY_str",
    "BUILDING_NUMBER",
    "BUILDING_NAME_LONG",
    "ASSIGNABLE_AREA"
]
# For floors, keep assignable area and a floor identifier/number if present
cols_floor = ["FCLT_FLOOR_KEY_str", "ASSIGNABLE_AREA"]
# Add common floor number columns if they exist
for cand in ["FLOOR_NUMBER", "FLOOR_NUM", "FLOOR_CODE", "FLOOR_NAME"]:
    if cand in fclt_floor.columns and cand not in cols_floor:
        cols_floor.append(cand)

fac_building_ren = fac_building[cols_building].rename(columns={
    "FAC_BUILDING_KEY_str": "BUILDING_KEY_str",
    "ASSIGNABLE_AREA": "BUILDING_ASSIGNABLE_AREA"
})

rename_floor = {
    "FCLT_FLOOR_KEY_str": "FLOOR_KEY_str",
    "ASSIGNABLE_AREA": "FLOOR_ASSIGNABLE_AREA"
}
# Standardize floor number column to FLOOR_NUMBER if possible
if "FLOOR_NUMBER" in cols_floor:
    pass
elif "FLOOR_NUM" in cols_floor:
    rename_floor["FLOOR_NUM"] = "FLOOR_NUMBER"
elif "FLOOR_CODE" in cols_floor:
    rename_floor["FLOOR_CODE"] = "FLOOR_NUMBER"
elif "FLOOR_NAME" in cols_floor:
    rename_floor["FLOOR_NAME"] = "FLOOR_NUMBER"

fclt_floor_ren = fclt_floor[cols_floor].rename(columns=rename_floor)

# 4) Left joins from FAC_ROOMS to enrich with building and floor assignable areas
fac_rooms_enriched = (
    fac_rooms
    .merge(fac_building_ren, on="BUILDING_KEY_str", how="left")
    .merge(fclt_floor_ren, on="FLOOR_KEY_str", how="left")
)

# 5) Compute per-room percentage fields
den_floor = fac_rooms_enriched["FLOOR_ASSIGNABLE_AREA"]
den_bldg = fac_rooms_enriched["BUILDING_ASSIGNABLE_AREA"]

fac_rooms_enriched["room_pct_of_floor"] = np.where(
    (den_floor.notna()) & (den_floor > 0),
    fac_rooms_enriched["AREA"] / den_floor,
    np.nan
)

fac_rooms_enriched["room_pct_of_building"] = np.where(
    (den_bldg.notna()) & (den_bldg > 0),
    fac_rooms_enriched["AREA"] / den_bldg,
    np.nan
)

# 6) Attach organization and department info from SPACE_DETAIL if available
# Attempt to link via a reasonable key. Common candidates in FAC_ROOMS include:
# 'fac_room_key', 'ROOM_KEY', 'ROOM_FULL_NAME'
org_cols = []
if not space_detail.empty:
    # Identify likely keys and org/department columns
    left_key = None
    right_key = None
    if "fac_room_key" in fac_rooms_enriched.columns and "fac_room_key" in space_detail.columns:
        left_key = right_key = "fac_room_key"
    elif "ROOM_KEY" in fac_rooms_enriched.columns and "ROOM_KEY" in space_detail.columns:
        left_key = right_key = "ROOM_KEY"
    elif "ROOM_FULL_NAME" in fac_rooms_enriched.columns and "ROOM_FULL_NAME" in space_detail.columns:
        left_key = right_key = "ROOM_FULL_NAME"

    # Heuristic detection of organization/department columns
    possible_org_cols = [c for c in space_detail.columns if c.lower() in {
        "org", "organization", "org_name", "org_desc", "org_long_name", "org_short_name"
    }]
    possible_dept_cols = [c for c in space_detail.columns if c.lower() in {
        "dept", "department", "dept_name", "department_name", "dept_desc"
    }]

    # Pick first matches, if any
    org_col = possible_org_cols[0] if possible_org_cols else None
    dept_col = possible_dept_cols[0] if possible_dept_cols else None

    if left_key is not None:
        keep_cols = [right_key]
        if org_col:
            keep_cols.append(org_col)
        if dept_col:
            keep_cols.append(dept_col)
        sd_small = space_detail[keep_cols].drop_duplicates(right_key)
        fac_rooms_enriched = fac_rooms_enriched.merge(
            sd_small,
            left_on=left_key,
            right_on=right_key,
            how="left",
            suffixes=("", "_sd")
        )
        # Standardize output names
        if org_col:
            fac_rooms_enriched = fac_rooms_enriched.rename(columns={org_col: "ORGANIZATION_NAME"})
        if dept_col:
            fac_rooms_enriched = fac_rooms_enriched.rename(columns={dept_col: "DEPARTMENT_NAME"})

# 7) Select final output columns
final_cols = []

# Room full name
if "ROOM_FULL_NAME" in fac_rooms_enriched.columns:
    final_cols.append("ROOM_FULL_NAME")
elif "ROOM_NAME" in fac_rooms_enriched.columns:
    fac_rooms_enriched = fac_rooms_enriched.rename(columns={"ROOM_NAME": "ROOM_FULL_NAME"})
    final_cols.append("ROOM_FULL_NAME")

# Building name
if "BUILDING_NAME_LONG" in fac_rooms_enriched.columns:
    final_cols.append("BUILDING_NAME_LONG")
# Building number if available
if "BUILDING_NUMBER" in fac_rooms_enriched.columns:
    final_cols.append("BUILDING_NUMBER")

# Floor number (standardized earlier where possible)
if "FLOOR_NUMBER" in fac_rooms_enriched.columns:
    final_cols.append("FLOOR_NUMBER")

# Organization and Department
for cname in ["ORGANIZATION_NAME", "DEPARTMENT_NAME"]:
    if cname in fac_rooms_enriched.columns:
        final_cols.append(cname)

# Percentages
final_cols += ["room_pct_of_floor", "room_pct_of_building"]

# Ensure columns exist; if not, create empty placeholders
for c in final_cols:
    if c not in fac_rooms_enriched.columns:
        fac_rooms_enriched[c] = pd.NA

answer_df = fac_rooms_enriched[final_cols].copy()

# Optional: format percentages as numeric (keep as floats per guideline)
# Round to 6 decimals for readability while remaining numeric
answer_df["room_pct_of_floor"] = answer_df["room_pct_of_floor"].astype(float).round(6)
answer_df["room_pct_of_building"] = answer_df["room_pct_of_building"].astype(float).round(6)

# 8) Assign final result
result = {"room_details_with_org_dept_and_pct": answer_df}