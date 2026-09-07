import pandas as pd

# The input tables are provided in a dict named `tables`
# Mapping per guideline:
# tables['table_1'] -> BUILDINGS.pkl
# tables['table_3'] -> FAC_BUILDING.pkl
# tables['table_7'] -> SPACE_DETAIL.pkl
# tables['table_8'] -> FCLT_BUILDING_ADDRESS.pkl

# Load DataFrames from provided `tables` dict
bld = tables['table_1'].copy()
fac = tables['table_3'].copy()
space = tables['table_7'].copy()
addr = tables['table_8'].copy()

# Utility functions for key standardization (same logic as reference)
def std_str_series(s):
    return s.astype(str).str.strip().str.upper()

def coerce_to_str_numeric_key(s):
    def norm(x):
        if pd.isna(x):
            return None
        try:
            f = float(x)
            if f.is_integer():
                return str(int(f))
            else:
                xs = str(x).strip()
                if xs.endswith(".0"):
                    return xs[:-2]
                return xs
        except Exception:
            return str(x).strip()
    return s.apply(norm)

# Standardize join keys
if "BUILDING_NUMBER" in bld.columns:
    bld["BUILDING_NUMBER_STD"] = std_str_series(bld["BUILDING_NUMBER"])
if "BUILDING_NUMBER" in fac.columns:
    fac["BUILDING_NUMBER_STD"] = std_str_series(fac["BUILDING_NUMBER"])
if "BUILDING_NUMBER" in addr.columns:
    addr["BUILDING_NUMBER_STD"] = std_str_series(addr["BUILDING_NUMBER"])

if "BUILDING_KEY" in bld.columns:
    bld["BUILDING_KEY_STD"] = coerce_to_str_numeric_key(bld["BUILDING_KEY"])
if "BUILDING_KEY" in space.columns:
    space["BUILDING_KEY_STD"] = coerce_to_str_numeric_key(space["BUILDING_KEY"])

# a) Address count per BUILDING_NUMBER (distinct addresses)
if {"BUILDING_NUMBER_STD", "FCLT_BUILDING_ADDRESS_KEY"}.issubset(addr.columns):
    addr_counts = (
        addr.dropna(subset=["BUILDING_NUMBER_STD"])
            .groupby("BUILDING_NUMBER_STD")["FCLT_BUILDING_ADDRESS_KEY"]
            .nunique()
            .rename("ADDRESS_COUNT")
            .reset_index()
    )
else:
    addr_counts = pd.DataFrame(columns=["BUILDING_NUMBER_STD", "ADDRESS_COUNT"])

# b) Total rooms per BUILDING_KEY (count of ROOM_NUMBER non-null; fallback ROOM_COUNTER)
if "BUILDING_KEY_STD" in space.columns:
    if "ROOM_NUMBER" in space.columns:
        room_counts_num = (
            space.assign(_room_flag=space["ROOM_NUMBER"].notna())
                 .groupby("BUILDING_KEY_STD")["_room_flag"]
                 .sum()
                 .rename("ROOM_COUNT")
                 .astype(int)
                 .reset_index()
        )
    else:
        room_counts_num = (
            space.groupby("BUILDING_KEY_STD")["SPACE_UNIT_KEY"]
                 .size()
                 .rename("ROOM_COUNT")
                 .reset_index()
        )
else:
    room_counts_num = pd.DataFrame(columns=["BUILDING_KEY_STD", "ROOM_COUNT"])

# c) Average gross area across all buildings (from BUILDINGS; fallback to FAC_BUILDING EXT_GROSS_AREA)
gross_col = "BLDG_GROSS_SQUARE_FOOTAGE" if "BLDG_GROSS_SQUARE_FOOTAGE" in bld.columns else None
if gross_col:
    overall_avg_gross = bld[gross_col].dropna().mean()
else:
    if "EXT_GROSS_AREA" in fac.columns:
        overall_avg_gross = fac["EXT_GROSS_AREA"].dropna().mean()
        gross_col = None
    else:
        overall_avg_gross = None
        gross_col = None

# Prepare FAC subset with type and date built
fac_subset_cols = ["BUILDING_NUMBER_STD"]
if "BUILDING_TYPE" in fac.columns:
    fac_subset_cols.append("BUILDING_TYPE")
if "DATE_BUILT" in fac.columns:
    fac_subset_cols.append("DATE_BUILT")
fac_sub = fac[fac_subset_cols].drop_duplicates(subset=["BUILDING_NUMBER_STD"])

# Merge pipeline: start from BUILDINGS
out = bld.copy()

# Merge address counts (on BUILDING_NUMBER_STD)
if "BUILDING_NUMBER_STD" in out.columns and "BUILDING_NUMBER_STD" in addr_counts.columns:
    out = out.merge(addr_counts, on="BUILDING_NUMBER_STD", how="left")
else:
    out["ADDRESS_COUNT"] = pd.NA

# Merge room counts (on BUILDING_KEY_STD)
if "BUILDING_KEY_STD" in out.columns and "BUILDING_KEY_STD" in room_counts_num.columns:
    out = out.merge(room_counts_num, on="BUILDING_KEY_STD", how="left")
else:
    out["ROOM_COUNT"] = pd.NA

# Merge FAC building attributes
if "BUILDING_NUMBER_STD" in out.columns and "BUILDING_NUMBER_STD" in fac_sub.columns:
    out = out.merge(fac_sub, on="BUILDING_NUMBER_STD", how="left", suffixes=("", "_FAC"))
else:
    if "BUILDING_TYPE" not in out.columns:
        out["BUILDING_TYPE"] = pd.NA
    if "DATE_BUILT" not in out.columns:
        out["DATE_BUILT"] = pd.NaT

# Add overall average gross area as a scalar column
out["OVERALL_AVG_GROSS_SQFT"] = overall_avg_gross

# Select and rename columns per question:
# name (BUILDING_NAME), number (BUILDING_NUMBER), construction date (DATE_BUILT),
# type (BUILDING_TYPE), count of addresses (ADDRESS_COUNT), average gross area (OVERALL_AVG_GROSS_SQFT),
# total number of rooms (ROOM_COUNT). Sort by building name.
select_cols = [
    "BUILDING_NAME",
    "BUILDING_NUMBER",
    "DATE_BUILT" if "DATE_BUILT" in out.columns else None,
    "BUILDING_TYPE" if "BUILDING_TYPE" in out.columns else None,
    "ADDRESS_COUNT",
    "OVERALL_AVG_GROSS_SQFT",
    "ROOM_COUNT",
]
select_cols = [c for c in select_cols if c is not None and c in out.columns]

final_df = (
    out[select_cols]
    .rename(columns={
        "BUILDING_NAME": "BUILDING_NAME",
        "BUILDING_NUMBER": "BUILDING_NUMBER",
        "DATE_BUILT": "DATE_BUILT",
        "BUILDING_TYPE": "BUILDING_TYPE",
        "ADDRESS_COUNT": "ADDRESS_COUNT",
        "OVERALL_AVG_GROSS_SQFT": "AVERAGE_GROSS_AREA_SQFT",
        "ROOM_COUNT": "ROOM_COUNT",
    })
    .sort_values(by=["BUILDING_NAME"], kind="mergesort")
    .reset_index(drop=True)
)

# Package final answer as required
result = {"buildings_summary": final_df}