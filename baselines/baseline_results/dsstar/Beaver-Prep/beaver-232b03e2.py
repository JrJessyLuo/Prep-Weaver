import re
import pandas as pd

# Source tables from the provided `tables` dict
fclt_floor_df = tables['table_1'].copy()
buildings_df = tables['table_8'].copy()
fclt_building_df = tables['table_10'].copy()

# Helper to normalize FLOOR to numeric floor_number (same logic as reference)
def normalize_floor(val):
    if pd.isna(val):
        return None
    s = str(val).strip().upper()

    drop_exact = {"D", "G", "M", "PH", "MEZ", "P", "L", "LL", "ROOF", "RM", "R", "B", ""}
    if s in drop_exact:
        return None

    if re.fullmatch(r"D.*|G.*|.*M|0{2,}", s):
        return None

    m = re.fullmatch(r"B(\d+)", s)
    if m:
        return -int(m.group(1))

    if re.fullmatch(r"PH\d+", s):
        return None

    m = re.fullmatch(r"R(\d+)", s)
    if m:
        return int(m.group(1))

    if re.fullmatch(r"-?\d+", s):
        return int(s)

    f = float(s)
    if float(s).is_integer():
        return int(f)
    return None

# Apply normalization
fclt_floor_df["floor_number"] = fclt_floor_df["FLOOR"].apply(normalize_floor)

# Compute max floor_number per building (same as reference)
max_floor_per_building = (
    fclt_floor_df.dropna(subset=["floor_number"])
    .groupby("FCLT_BUILDING_KEY", as_index=False)["floor_number"]
    .max()
    .rename(columns={"floor_number": "max_floor_number"})
)

# Join to get building names
# Prefer FCLT_BUILDING to obtain a building name if present; otherwise fall back to BUILDINGS
# Standardize potential name columns
name_cols_fclt = [c for c in fclt_building_df.columns if c.upper() in ("BUILDING_NAME", "NAME", "FCLT_BUILDING_NAME", "DESCRIPTION", "DESC")]
name_cols_bldg = [c for c in buildings_df.columns if c.upper() in ("BUILDING_NAME", "NAME", "DESCRIPTION", "DESC")]

fclt_bldg_names = fclt_building_df.copy()
if name_cols_fclt:
    fclt_bldg_names = fclt_bldg_names[["FCLT_BUILDING_KEY", name_cols_fclt[0]]].rename(columns={name_cols_fclt[0]: "BUILDING_NAME"})
else:
    fclt_bldg_names = fclt_bldg_names[["FCLT_BUILDING_KEY"]]
    fclt_bldg_names["BUILDING_NAME"] = pd.NA

bldg_names = buildings_df.copy()
if "FCLT_BUILDING_KEY" not in bldg_names.columns and "BUILDING_KEY" in bldg_names.columns:
    bldg_names = bldg_names.rename(columns={"BUILDING_KEY": "FCLT_BUILDING_KEY"})
if name_cols_bldg:
    bldg_names = bldg_names[["FCLT_BUILDING_KEY", name_cols_bldg[0]]].rename(columns={name_cols_bldg[0]: "BUILDING_NAME"})
else:
    bldg_names = bldg_names[["FCLT_BUILDING_KEY"]]
    bldg_names["BUILDING_NAME"] = pd.NA

# Merge max floors with names; prefer FCLT_BUILDING names, then fallback to BUILDINGS
merged = max_floor_per_building.merge(fclt_bldg_names, on="FCLT_BUILDING_KEY", how="left", suffixes=("", "_FCLT"))
merged = merged.merge(bldg_names, on="FCLT_BUILDING_KEY", how="left", suffixes=("", "_BLDG"))

# Choose name from FCLT first, else from BUILDINGS
merged["BUILDING_NAME_FINAL"] = merged["BUILDING_NAME"].where(merged["BUILDING_NAME"].notna(), merged["BUILDING_NAME_BLDG"])

# Find the overall maximum floor number and filter
max_val = merged["max_floor_number"].max()
answer = merged.loc[merged["max_floor_number"] == max_val, ["BUILDING_NAME_FINAL", "max_floor_number"]].drop_duplicates()

# Final answer DataFrame with required columns
final_df = answer.rename(columns={"BUILDING_NAME_FINAL": "building_name", "max_floor_number": "max_floor_number"}).reset_index(drop=True)

# Assign to result as required
result = {"building_with_largest_floor_number": final_df}