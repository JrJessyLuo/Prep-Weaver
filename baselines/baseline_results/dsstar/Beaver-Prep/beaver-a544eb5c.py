import pandas as pd

# Access input DataFrames from the provided `tables` dictionary
fac_building = tables['table_1']
fac_floor = tables['table_2']
fac_rooms = tables['table_9']

# Columns to use
area_cols = ["EXT_GROSS_AREA", "ASSIGNABLE_AREA", "NON_ASSIGNABLE_AREA"]

# 1) Aggregate floor-level totals by BUILDING_KEY
if not all(c in fac_floor.columns for c in area_cols):
    raise ValueError("FAC_FLOOR is missing required area columns.")
if "BUILDING_KEY" not in fac_floor.columns:
    raise ValueError("FAC_FLOOR is missing BUILDING_KEY.")

floor_agg = (
    fac_floor.groupby("BUILDING_KEY", dropna=False)[area_cols]
    .sum(min_count=1)
    .reset_index()
    .rename(columns={c: f"FLOOR_{c}_SUM" for c in area_cols})
)

# 2) Compute total room count by BUILDING_KEY
if "BUILDING_KEY" not in fac_rooms.columns:
    raise ValueError("FAC_ROOMS is missing BUILDING_KEY.")
rooms_agg = (
    fac_rooms.groupby("BUILDING_KEY", dropna=False)
    .size()
    .reset_index(name="total_room_count")
)

# 3) Determine join key between FAC_BUILDING and floor/rooms (BUILDING_KEY)
bld_key_building = "FAC_BUILDING_KEY" if "FAC_BUILDING_KEY" in fac_building.columns else (
    "BUILDING_KEY" if "BUILDING_KEY" in fac_building.columns else None
)
if bld_key_building is None:
    raise ValueError("No suitable building key found in FAC_BUILDING.")

# 4) Merge aggregated data back to buildings
bld_cols_to_keep = [c for c in ["BUILDING_NUMBER", "BUILDING_NAME_LONG", "PARENT_BUILDING_NAME_LONG"] if c in fac_building.columns]
building_base = fac_building[[bld_key_building] + bld_cols_to_keep].copy()

merged = building_base.merge(
    floor_agg, left_on=bld_key_building, right_on="BUILDING_KEY", how="left"
).merge(
    rooms_agg, on="BUILDING_KEY", how="left"
)

# 5) Compute per-building totals (renaming for clarity)
merged = merged.rename(columns={
    "FLOOR_ASSIGNABLE_AREA_SUM": "total_assignable",
    "FLOOR_NON_ASSIGNABLE_AREA_SUM": "total_non_assignable",
    "FLOOR_EXT_GROSS_AREA_SUM": "total_ext_gross_area"
})

# 6) Prepare final columns: building name, building number, total assignable, total non-assignable, total room count
final_cols = []
if "BUILDING_NAME_LONG" in merged.columns:
    final_cols.append("BUILDING_NAME_LONG")
elif "PARENT_BUILDING_NAME_LONG" in merged.columns:
    final_cols.append("PARENT_BUILDING_NAME_LONG")

if "BUILDING_NUMBER" in merged.columns:
    final_cols.append("BUILDING_NUMBER")

final_cols += ["total_assignable", "total_non_assignable", "total_room_count"]

final_df = merged[final_cols].copy()

# 7) Sort descending by total_assignable
final_df = final_df.sort_values(by="total_assignable", ascending=False)

# 8) Assign to result dict as required
result = {"building_areas_and_rooms": final_df}