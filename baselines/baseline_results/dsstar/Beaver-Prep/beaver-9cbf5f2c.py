import pandas as pd
import numpy as np

# Input tables (already provided in the environment)
# Mapping per instructions:
# tables['table_1'] -> BUILDINGS.pkl
# tables['table_2'] -> FAC_BUILDING.pkl
# tables['table_9'] -> HR_ORG_UNIT_NEW.pkl
# tables['table_10'] -> ZPM_ROOMS_LOAD.pkl

# 1) Load dataframes from provided `tables` dict
bld = tables['table_1'].copy()
fac_bld = tables['table_2'].copy()
hr = tables['table_9'].copy()
rooms = tables['table_10'].copy()

# Helpers
def strip_upper(series):
    return series.astype(str).str.strip().str.upper()

# 2) Prepare join keys
# Clean BUILDING_NUMBER in BUILDINGS and FAC_BUILDING
bld["BUILDING_NUMBER_CLEAN"] = strip_upper(bld["BUILDING_NUMBER"])
fac_bld["BUILDING_NUMBER_CLEAN"] = strip_upper(fac_bld["BUILDING_NUMBER"])

# Derive building number from rooms
def derive_bnum(row):
    br = str(row.get("BUILDING_ROOM", "")).strip()
    bc = str(row.get("BUILDING_COMPONENT", "")).strip()
    if br and br.lower() != "nan":
        if "-" in br:
            return br.split("-", 1)[0].strip().upper()
        else:
            return br.strip().upper()
    if bc and bc.lower() != "nan":
        return bc.strip().upper()
    return pd.NA

rooms["BUILDING_NUMBER_DERIVED"] = rooms.apply(derive_bnum, axis=1).astype("string")
rooms["BUILDING_NUMBER_CLEAN"] = rooms["BUILDING_NUMBER_DERIVED"].str.strip().str.upper()

# Normalize HR_ORG_UNIT_ID types
rooms["HR_ORG_UNIT_ID"] = pd.to_numeric(rooms["HR_ORG_UNIT_ID"], errors="coerce").astype("Int64")
hr["HR_ORG_UNIT_ID"] = pd.to_numeric(hr["HR_ORG_UNIT_ID"], errors="coerce").astype("Int64")

# 3) Join buildings to rooms using BUILDING_NUMBER
rooms_fac = rooms.merge(
    fac_bld.add_prefix("FAC_"),
    left_on="BUILDING_NUMBER_CLEAN",
    right_on="FAC_BUILDING_NUMBER_CLEAN",
    how="left",
    validate="m:1"
)

# Fallback join with BUILDINGS where FAC not found
missing_mask = rooms_fac["FAC_BUILDING_NUMBER_CLEAN"].isna()
if missing_mask.any():
    base_cols = [c for c in rooms_fac.columns if not c.startswith("FAC_")]
    rooms_missing = rooms_fac.loc[missing_mask, base_cols].merge(
        bld.add_prefix("BLD_"),
        left_on="BUILDING_NUMBER_CLEAN",
        right_on="BLD_BUILDING_NUMBER_CLEAN",
        how="left",
        validate="m:1"
    )
    for col in rooms_missing.columns:
        if col not in rooms_fac.columns:
            rooms_fac[col] = pd.NA
    rooms_fac.loc[missing_mask, rooms_missing.columns] = rooms_missing.values

# 4) Join HR org details
rooms_full = rooms_fac.merge(
    hr.add_prefix("HR_"),
    left_on="HR_ORG_UNIT_ID",
    right_on="HR_HR_ORG_UNIT_ID",
    how="left",
    validate="m:1"
)

# 5) Filter to HR-related rows
def is_hr_like(s):
    if s is None:
        return False
    ss = str(s).upper()
    return ("HUMAN RESOURCE" in ss) or (ss.strip().startswith("HR")) or (" HR " in f" {ss} ") or (ss == "HR")

hr_name_col = "HR_HR_DEPARTMENT_NAME" if "HR_HR_DEPARTMENT_NAME" in rooms_full.columns else None
hr_abbr_col = "HR_HR_DEPARTMENT_ABBR" if "HR_HR_DEPARTMENT_ABBR" in rooms_full.columns else None

hr_mask = pd.Series(False, index=rooms_full.index)
if hr_name_col:
    hr_mask |= rooms_full[hr_name_col].apply(is_hr_like)
if hr_abbr_col:
    hr_mask |= rooms_full[hr_abbr_col].apply(is_hr_like)

rooms_hr = rooms_full.loc[hr_mask].copy()

# 6) Determine grouping keys: prefer FAC building key/name; fallback to BUILDINGS
fac_key_col = "FAC_FCLT_BUILDING_KEY" if "FAC_FCLT_BUILDING_KEY" in rooms_hr.columns else None
fac_name_col = "FAC_BUILDING_NAME_LONG" if "FAC_BUILDING_NAME_LONG" in rooms_hr.columns else None
fac_bnum_col = "FAC_BUILDING_NUMBER" if "FAC_BUILDING_NUMBER" in rooms_hr.columns else None
fac_parent_name_col = "FAC_PARENT_BUILDING_NAME" if "FAC_PARENT_BUILDING_NAME" in rooms_hr.columns else None

# Built year column detection in FAC
fac_built_year_col = None
for cand in ["BUILT_YEAR", "YEAR_BUILT", "BUILDING_YEAR", "CONST_YEAR", "CONSTRUCTION_YEAR"]:
    c_full = f"FAC_{cand}"
    if c_full in rooms_hr.columns:
        fac_built_year_col = c_full
        break

bld_key_col = "BLD_BUILDING_KEY" if "BLD_BUILDING_KEY" in rooms_hr.columns else None
bld_name_col = "BLD_BUILDING_NAME" if "BLD_BUILDING_NAME" in rooms_hr.columns else None
bld_bnum_col = "BLD_BUILDING_NUMBER" if "BLD_BUILDING_NUMBER" in rooms_hr.columns else None

rooms_hr["GROUP_BUILDING_KEY"] = np.where(
    fac_key_col and rooms_hr[fac_key_col].notna(),
    rooms_hr[fac_key_col],
    rooms_hr[bld_key_col] if bld_key_col else pd.NA
)

# If no building key available at all, fallback to building number
if rooms_hr["GROUP_BUILDING_KEY"].isna().all():
    fallback_bnum = None
    if fac_bnum_col and rooms_hr[fac_bnum_col].notna().any():
        fallback_bnum = fac_bnum_col
    elif bld_bnum_col and rooms_hr[bld_bnum_col].notna().any():
        fallback_bnum = bld_bnum_col
    else:
        fallback_bnum = "BUILDING_NUMBER_CLEAN"
    rooms_hr["GROUP_BUILDING_KEY"] = rooms_hr[fallback_bnum]

# Unified building name
def pick_name(row):
    if fac_name_col and pd.notna(row.get(fac_name_col, pd.NA)):
        return row[fac_name_col]
    if fac_parent_name_col and pd.notna(row.get(fac_parent_name_col, pd.NA)):
        return row[fac_parent_name_col]
    if bld_name_col and pd.notna(row.get(bld_name_col, pd.NA)):
        return row[bld_name_col]
    if fac_bnum_col and pd.notna(row.get(fac_bnum_col, pd.NA)):
        return row[fac_bnum_col]
    if bld_bnum_col and pd.notna(row.get(bld_bnum_col, pd.NA)):
        return row[bld_bnum_col]
    return row.get("BUILDING_NUMBER_CLEAN", pd.NA)

rooms_hr["GROUP_BUILDING_NAME"] = rooms_hr.apply(pick_name, axis=1)

# 7) Compute aggregation inputs
gross_fac_col = "FAC_EXT_GROSS_AREA" if "FAC_EXT_GROSS_AREA" in rooms_hr.columns else None
gross_bld_col = "BLD_BLDG_GROSS_SQUARE_FOOTAGE" if "BLD_BLDG_GROSS_SQUARE_FOOTAGE" in rooms_hr.columns else None

rooms_hr["GROSS_SQFT_USED"] = pd.NA
if gross_fac_col:
    rooms_hr["GROSS_SQFT_USED"] = rooms_hr[gross_fac_col]
if gross_bld_col:
    rooms_hr["GROSS_SQFT_USED"] = rooms_hr["GROSS_SQFT_USED"].where(
        rooms_hr["GROSS_SQFT_USED"].notna(), rooms_hr[gross_bld_col]
    )
rooms_hr["GROSS_SQFT_USED"] = pd.to_numeric(rooms_hr["GROSS_SQFT_USED"], errors="coerce")

assign_col = "FAC_ASSIGNABLE_AREA" if "FAC_ASSIGNABLE_AREA" in rooms_hr.columns else None
if assign_col:
    rooms_hr["ASSIGNABLE_SQFT_USED"] = pd.to_numeric(rooms_hr[assign_col], errors="coerce")
else:
    rooms_hr["ASSIGNABLE_SQFT_USED"] = np.nan

# Built year
if fac_built_year_col:
    rooms_hr["BUILT_YEAR_USED"] = rooms_hr[fac_built_year_col]
else:
    rooms_hr["BUILT_YEAR_USED"] = pd.NA

# HR department name for list aggregation
hr_dept_name = hr_name_col if hr_name_col else hr_abbr_col
if hr_dept_name is None:
    hr_dept_name = "HR_DEPT_FALLBACK"
    rooms_hr[hr_dept_name] = pd.NA

# 8) Group and aggregate
group_cols = ["GROUP_BUILDING_KEY", "GROUP_BUILDING_NAME"]
agg_df = rooms_hr.groupby(group_cols).agg(
    total_gross_sqft=("GROSS_SQFT_USED", "sum"),
    total_assignable_sqft=("ASSIGNABLE_SQFT_USED", "sum"),
    avg_assignable_sqft=("ASSIGNABLE_SQFT_USED", "mean"),
    hr_departments=(hr_dept_name, lambda x: sorted(set([str(v) for v in x.dropna().astype(str) if v.strip()]))),
    built_year=("BUILT_YEAR_USED", lambda x: next((v for v in x if pd.notna(v)), np.nan)),
).reset_index()

# Final result packaging as required
result = {
    "hr_by_building": agg_df
}