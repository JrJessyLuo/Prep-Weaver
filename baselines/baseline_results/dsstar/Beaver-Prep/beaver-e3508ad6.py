import pandas as pd
import numpy as np

# Source input from provided tables dict
df = tables['table_1'].copy()

# Helper to safely coerce to uppercase string
def to_u_str(s):
    return s.astype(str).str.upper()

# Identify likely date fields for built/occupied in FAC_BUILDING by name heuristics
date_cols = [c for c in df.columns if any(k in c.upper() for k in ["DATE", "BUILT", "BUILD", "OCCUP", "CONSTRUCT"])]
# Prefer more specific names if present
candidates_built = [c for c in date_cols if any(k in c.upper() for k in ["DATE_BUILT", "BUILT", "BUILD", "CONSTRUCT"]) and "OCCUP" not in c.upper()]
candidates_occupied = [c for c in date_cols if "OCCUP" in c.upper() or "DATE_OCCUP" in c.upper()]

# Choose primary fields to parse, fallback to None if none
date_built_col = candidates_built[0] if candidates_built else None
date_occupied_col = candidates_occupied[0] if candidates_occupied else None

# Parse to datetime then extract year
def parse_year_from_col(df_local, col):
    if col is None or col not in df_local.columns:
        return pd.Series([pd.NA] * len(df_local), index=df_local.index, dtype="Int64")
    ser = df_local[col]
    dt = pd.to_datetime(ser, errors="coerce", infer_datetime_format=True)
    if dt.isna().mean() > 0.8:
        ser_str = ser.astype(str).str.extract(r"(\d{4})")[0]
        yr = pd.to_numeric(ser_str, errors="coerce").astype("Int64")
        return yr
    return dt.dt.year.astype("Int64")

year_built = parse_year_from_col(df, date_built_col)
year_occupied = parse_year_from_col(df, date_occupied_col)

# Create standardized fields
df_out = df.copy()
df_out["CONSTRUCTION_START_YEAR"] = year_built
df_out["INITIAL_OCCUPANCY_YEAR"] = year_occupied

# Define ownership heuristic: OWNERSHIP_TYPE contains "OWN"
if "OWNERSHIP_TYPE" in df_out.columns:
    owned_mask = to_u_str(df_out["OWNERSHIP_TYPE"]).str.contains("OWN", na=False)
else:
    owned_mask = pd.Series([True] * len(df_out), index=df_out.index)

# Define subdivision heuristic using PARENT_BUILDING_NUMBER vs BUILDING_NUMBER
if "PARENT_BUILDING_NUMBER" in df_out.columns and "BUILDING_NUMBER" in df_out.columns:
    p = df_out["PARENT_BUILDING_NUMBER"].astype(str).str.strip()
    b = df_out["BUILDING_NUMBER"].astype(str).str.strip()
    not_subdivision_mask = (df_out["PARENT_BUILDING_NUMBER"].isna()) | (p.eq("")) | (to_u_str(p).eq("NONE")) | (p.eq(b))
else:
    not_subdivision_mask = pd.Series([True] * len(df_out), index=df_out.index)

filtered = df_out.loc[owned_mask & not_subdivision_mask].copy()

# Prepare display columns (preserve any available identifiers)
display_cols = []
for c in ["FAC_BUILDING_KEY", "BUILDING_NUMBER", "BUILDING_NAME_LONG", "OWNERSHIP_TYPE", "PARENT_BUILDING_NUMBER"]:
    if c in filtered.columns:
        display_cols.append(c)
for c in ["CONSTRUCTION_START_YEAR", "INITIAL_OCCUPANCY_YEAR"]:
    if c in filtered.columns:
        display_cols.append(c)

# Build the final answer per guideline:
# - For each owned building not a subdivision, list:
#   [Construction Start Year (only if differs from previous row, otherwise null)],
#   [Building Number],
#   [Initial Occupancy Year]
# - Unknown years shown as 'UNKNOWN'
# - Append a final row: (null, "#building Buildings", null)

# Choose an ordering for display; default to BUILDING_NUMBER ascending if present, else index order
if "BUILDING_NUMBER" in filtered.columns:
    ordered = filtered.sort_values(by=["BUILDING_NUMBER"]).reset_index(drop=True)
else:
    ordered = filtered.reset_index(drop=True)

# Prepare working series
cs = ordered["CONSTRUCTION_START_YEAR"] if "CONSTRUCTION_START_YEAR" in ordered.columns else pd.Series([pd.NA]*len(ordered), dtype="Int64")
io = ordered["INITIAL_OCCUPANCY_YEAR"] if "INITIAL_OCCUPANCY_YEAR" in ordered.columns else pd.Series([pd.NA]*len(ordered), dtype="Int64")
bn = ordered["BUILDING_NUMBER"] if "BUILDING_NUMBER" in ordered.columns else pd.Series([""]*len(ordered))

# Replace unknowns with 'UNKNOWN' for year display, but keep a copy for "diff from previous" logic
cs_year = cs.copy()
io_year = io.copy()

# Display strings
cs_disp = cs_year.astype("Int64").astype(str)
cs_disp = cs_disp.where(~cs_year.isna(), "UNKNOWN")
io_disp = io_year.astype("Int64").astype(str)
io_disp = io_disp.where(~io_year.isna(), "UNKNOWN")

# Show construction year only if differs from previous row (string compare including UNKNOWN)
cs_disp_final = cs_disp.copy()
if len(cs_disp_final) > 0:
    prev = None
    for i in range(len(cs_disp_final)):
        cur = cs_disp.iloc[i]
        if i == 0:
            prev = cur
            # keep first row's value as-is
        else:
            if cur == prev:
                cs_disp_final.iloc[i] = None
            else:
                prev = cur

# Build the main output DataFrame
out = pd.DataFrame({
    "CONSTRUCTION_START_YEAR": cs_disp_final,
    "BUILDING_NUMBER": bn.astype(str),
    "INITIAL_OCCUPANCY_YEAR": io_disp
})

# Append the summary row
total_n = len(out)
summary_row = pd.DataFrame({
    "CONSTRUCTION_START_YEAR": [None],
    "BUILDING_NUMBER": [f"{total_n} Buildings"],
    "INITIAL_OCCUPANCY_YEAR": [None]
})
final_df = pd.concat([out, summary_row], ignore_index=True)

# Package result
result = {
    "Owned_Not_Subdivision_Construction_and_Occupancy": final_df
}