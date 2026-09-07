import pandas as pd
import numpy as np

# Source tables from the provided `tables` dict
BUILDINGS = tables['table_1'].copy()
FAC_BUILDING = tables['table_2'].copy()
FAC_FLOOR = tables['table_5'].copy()
SPACE_DETAIL = tables['table_9'].copy()

# Safety: standardize join keys as strings (strip whitespace)
for df, col in [(BUILDINGS, "BUILDING_NUMBER"), (FAC_BUILDING, "BUILDING_NUMBER")]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

for df, col in [(BUILDINGS, "BUILDING_KEY"), (FAC_FLOOR, "BUILDING_KEY"), (SPACE_DETAIL, "BUILDING_KEY")]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

# 1) Join BUILDINGS to FAC_BUILDING on BUILDING_NUMBER (left join)
# Select core columns from FAC_BUILDING
fac_bldg_cols = [
    "BUILDING_NUMBER", "BUILDING_NAME_LONG", "EXT_GROSS_AREA", "ASSIGNABLE_AREA",
    "BUILDING_HEIGHT", "BUILDING_CITY", "BUILDING_STATE", "POSTAL_CODE"
]
fac_bldg_cols = [c for c in fac_bldg_cols if c in FAC_BUILDING.columns]

buildings_core_cols = [
    "BUILDING_KEY", "BUILDING_NUMBER", "BUILDING_NAME", "BUILDING_STREET_ADDRESS",
    "BLDG_GROSS_SQUARE_FOOTAGE", "BLDG_ASSIGNABLE_SQUARE_FOOTAGE"
]
# Try common city/state/zip fields from BUILDINGS if present (sometimes address parts live here)
for extra_col in ["BUILDING_CITY", "BUILDING_STATE", "POSTAL_CODE"]:
    if extra_col in BUILDINGS.columns and extra_col not in buildings_core_cols:
        buildings_core_cols.append(extra_col)

buildings_core_cols = [c for c in buildings_core_cols if c in BUILDINGS.columns]

bld_join = BUILDINGS[buildings_core_cols].merge(
    FAC_BUILDING[fac_bldg_cols],
    on="BUILDING_NUMBER",
    how="left",
    suffixes=("", "_FAC")
)

# Prefer address city/state/zip from FAC_BUILDING when available, else fallback to BUILDINGS
for fld in ["BUILDING_CITY", "BUILDING_STATE", "POSTAL_CODE"]:
    if fld in bld_join.columns and f"{fld}_FAC" in bld_join.columns:
        # If FAC field exists, use that; otherwise keep existing
        bld_join[fld] = bld_join[f"{fld}_FAC"].combine_first(bld_join[fld])
    # Clean up FAC suffix columns if present
    fac_col = f"{fld}_FAC"
    if fac_col in bld_join.columns:
        bld_join.drop(columns=[fac_col], inplace=True)

# 2) Compute smallest and largest floor per BUILDING_KEY from FAC_FLOOR.FLOOR
if "FLOOR" in FAC_FLOOR.columns and "BUILDING_KEY" in FAC_FLOOR.columns:
    flr = FAC_FLOOR[["BUILDING_KEY", "FLOOR"]].copy()
    flr["BUILDING_KEY"] = flr["BUILDING_KEY"].astype(str).str.strip()
    flr["FLOOR_NUMERIC"] = pd.to_numeric(flr["FLOOR"], errors="coerce")
    floor_agg = flr.groupby("BUILDING_KEY").agg(
        smallest_floor=("FLOOR_NUMERIC", "min"),
        largest_floor=("FLOOR_NUMERIC", "max")
    ).reset_index()
else:
    floor_agg = pd.DataFrame(columns=["BUILDING_KEY", "smallest_floor", "largest_floor"])

# 3) Total room area per BUILDING_KEY from SPACE_DETAIL.ROOM_SQUARE_FOOTAGE
if "ROOM_SQUARE_FOOTAGE" in SPACE_DETAIL.columns and "BUILDING_KEY" in SPACE_DETAIL.columns:
    room_agg = SPACE_DETAIL.groupby("BUILDING_KEY", as_index=False)["ROOM_SQUARE_FOOTAGE"].sum()
    room_agg = room_agg.rename(columns={"ROOM_SQUARE_FOOTAGE": "total_room_area"})
else:
    room_agg = pd.DataFrame(columns=["BUILDING_KEY", "total_room_area"])

# 4) Assemble final aggregated frame per BUILDING_KEY
agg = bld_join.merge(floor_agg, on="BUILDING_KEY", how="left").merge(room_agg, on="BUILDING_KEY", how="left")

# 5) Select and order requested columns
final_cols_order = [
    "BUILDING_KEY",
    "BUILDING_NAME",
    "BUILDING_HEIGHT",
    "BUILDING_STREET_ADDRESS",
    "BUILDING_CITY",
    "BUILDING_STATE",
    "POSTAL_CODE",
    "BLDG_GROSS_SQUARE_FOOTAGE",
    "BLDG_ASSIGNABLE_SQUARE_FOOTAGE",
    "smallest_floor",
    "largest_floor",
    "total_room_area",
]
# If BUILDING_NAME is not available, fallback to BUILDING_NAME_LONG
if "BUILDING_NAME" not in agg.columns and "BUILDING_NAME_LONG" in agg.columns:
    agg["BUILDING_NAME"] = agg["BUILDING_NAME_LONG"]

final_cols = [c for c in final_cols_order if c in agg.columns]
final_df = agg[final_cols].copy()

# Optional: sort by BUILDING_KEY for readability if present
if "BUILDING_KEY" in final_df.columns:
    # Attempt numeric sort if possible
    bk_num = pd.to_numeric(final_df["BUILDING_KEY"], errors="coerce")
    if bk_num.notna().any():
        final_df = final_df.iloc[bk_num.sort_values(kind="stable").index]
    else:
        final_df = final_df.sort_values("BUILDING_KEY", kind="stable")

# Assign to result as required
result = {"building_summary": final_df}