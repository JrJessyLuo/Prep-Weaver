import pandas as pd
from typing import List, Any

# Access input tables from provided dict `tables`
fac_rooms = tables['table_1']          # FAC_ROOMS.pkl
buildings = tables['table_5']          # BUILDINGS.pkl

# Copy to avoid mutating originals
fac = fac_rooms.copy()
bldg = buildings.copy()

# Align key dtype to string for merge robustness
fac["BUILDING_KEY"] = fac["BUILDING_KEY"].astype(str)
bldg["BUILDING_KEY"] = bldg["BUILDING_KEY"].astype(str)

# Bring in building name
fac = fac.merge(
    bldg[["BUILDING_KEY", "BUILDING_NAME"]],
    on="BUILDING_KEY",
    how="left",
    validate="many_to_one"
)

# Helper: sorted unique list, dropping null-like values
def sorted_unique_list(series: pd.Series) -> List[Any]:
    vals = series.dropna().astype(str)
    vals = [v for v in vals if v not in ("", "nan", "None")]
    return sorted(set(vals))

# Floors: coerce to numeric for min/max
fac["_FLOOR_NUM"] = pd.to_numeric(fac["FLOOR"], errors="coerce")

# Choose room uniqueness basis:
# Prefer ROOM where available; if ROOM is very null, fallback to SPACE_ID
room_non_null_rate = 1.0 - float(fac["ROOM"].isna().mean())
use_room_col = "ROOM" if room_non_null_rate >= 0.5 else "SPACE_ID"

# Prepare DEPT_CODE as string for uniqueness while preserving numeric parse where needed
fac["_DEPT_STR"] = fac["DEPT_CODE"].astype(str)
fac["_DEPT_STR"] = fac["_DEPT_STR"].where(~fac["_DEPT_STR"].isin(["nan", "None"]), None)

# Groupby aggregations per building
agg_df = fac.groupby("BUILDING_KEY").agg(
    building_name=("BUILDING_NAME", lambda s: next((x for x in s if pd.notna(x)), None)),
    departments=("_DEPT_STR", sorted_unique_list),
    organizations=("ORGANIZATION_NAME", sorted_unique_list),
    min_floor=("_FLOOR_NUM", "min"),
    max_floor=("_FLOOR_NUM", "max"),
    room_count=(use_room_col, lambda s: int(s.dropna().astype(str).nunique()))
).reset_index()

# Optional: if building_name missing, try to backfill from BUILDINGS
mask_missing_name = agg_df["building_name"].isna()
if mask_missing_name.any():
    name_map = bldg.set_index("BUILDING_KEY")["BUILDING_NAME"].to_dict()
    agg_df.loc[mask_missing_name, "building_name"] = agg_df.loc[mask_missing_name, "BUILDING_KEY"].map(name_map)

# Reorder columns for readability
cols = ["BUILDING_KEY", "building_name", "min_floor", "max_floor", "room_count", "departments", "organizations"]
agg_df = agg_df[cols]

# Package final answer per guideline
result = {
    "building_summary": agg_df
}