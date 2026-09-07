import pandas as pd

# The input tables are provided in a dict named `tables`
# Mapping per guidelines:
# tables['table_1'] -> BUILDINGS.pkl
# tables['table_2'] -> FAC_BUILDING.pkl
# tables['table_3'] -> FCLT_BUILDING_HIST.pkl
# tables['table_4'] -> FCLT_BUILDING.pkl
# tables['table_5'] -> FCLT_BUILDING_HIST_1.pkl
# tables['table_6'] -> FAC_ORGANIZATION.pkl
# tables['table_7'] -> FCLT_FLOOR.pkl
# tables['table_8'] -> FCLT_ORGANIZATION.pkl
# tables['table_9'] -> FCLT_ORGANIZATION_HIST.pkl
# tables['table_10'] -> FCLT_FLOOR_HIST.pkl

# Load tables from provided dict
bld = tables.get('table_1', pd.DataFrame()).copy()
fac_building = tables.get('table_2', pd.DataFrame()).copy()
fclt_building = tables.get('table_4', pd.DataFrame()).copy()
fclt_floor = tables.get('table_7', pd.DataFrame()).copy()
org = tables.get('table_8', pd.DataFrame()).copy()

# Choose facility building table (prefer FCLT_BUILDING, else FAC_BUILDING)
if not fclt_building.empty:
    fb = fclt_building.copy()
elif not fac_building.empty:
    fb = fac_building.copy()
else:
    raise RuntimeError("No facility building table found (FCLT_BUILDING/FAC_BUILDING).")

# Identify building key column
if "FCLT_BUILDING_KEY" in fb.columns:
    fb_building_key_col = "FCLT_BUILDING_KEY"
elif "FAC_BUILDING_KEY" in fb.columns:
    fb_building_key_col = "FAC_BUILDING_KEY"
else:
    cand = [c for c in fb.columns if "BUILDING_KEY" in c.upper()]
    if not cand:
        raise RuntimeError("No building key column found in facility building table.")
    fb_building_key_col = cand[0]

# Ensure BUILDING_NUMBER exists
if "BUILDING_NUMBER" not in fb.columns:
    raise RuntimeError("BUILDING_NUMBER not found in facility building table.")

# Determine HR join feasibility
can_direct_join = ("FCLT_ORGANIZATION_KEY" in fb.columns) and ("FCLT_ORGANIZATION_KEY" in org.columns)

# Select relevant facility building columns
fb_cols_wanted = [
    fb_building_key_col, "BUILDING_NUMBER",
    "BUILDING_NAME_LONG", "BUILDING_NAME",
    "PARENT_BUILDING_NAME", "PARENT_BUILDING_NAME_LONG",
    "EXT_GROSS_AREA", "ASSIGNABLE_AREA",
    "BUILDING_HEIGHT"
]
fb_use = fb[[c for c in fb_cols_wanted if c in fb.columns]].copy()

# BUILDINGS columns for address; also try to split city/state if present, else leave blank
bld_cols_wanted = [
    "BUILDING_NUMBER",
    "BUILDING_STREET_ADDRESS",
    "BUILDING_MAILING_ADDRESS",
    "CITY",
    "STATE"
]
bld_use = bld[[c for c in bld_cols_wanted if c in bld.columns]].copy() if not bld.empty else pd.DataFrame(columns=bld_cols_wanted)

# Merge address onto facility building
merged = fb_use.merge(bld_use, on="BUILDING_NUMBER", how="left", suffixes=("", "_B"))

# HR info (attempt direct join; otherwise none, consistent with reference logic outcome)
hr_cols = ["HR_DEPARTMENT_NAME", "HR_ORG_UNIT_ID"]
if can_direct_join:
    org_use = org[["FCLT_ORGANIZATION_KEY"] + [c for c in hr_cols if c in org.columns]].drop_duplicates()
    merged = merged.merge(org_use, on="FCLT_ORGANIZATION_KEY", how="left")

# Floors count for Average_SF
if not fclt_floor.empty and "FCLT_BUILDING_KEY" in fclt_floor.columns:
    floor_counts = (
        fclt_floor.groupby("FCLT_BUILDING_KEY")["FCLT_FLOOR_KEY"]
        .nunique()
        .rename("FLOORS_COUNT")
        .reset_index()
    )
    merged = merged.merge(
        floor_counts,
        left_on=fb_building_key_col,
        right_on="FCLT_BUILDING_KEY",
        how="left",
    )
    merged.drop(columns=["FCLT_BUILDING_KEY"], inplace=True, errors="ignore")
else:
    merged["FLOORS_COUNT"] = pd.NA

# Compute Average_SF
def _avg_sf(row):
    ext = row.get("EXT_GROSS_AREA")
    cnt = row.get("FLOORS_COUNT")
    if pd.notna(ext) and pd.notna(cnt) and cnt and float(cnt) > 0:
        return float(ext) / float(cnt)
    return pd.NA

merged["Average_SF"] = merged.apply(_avg_sf, axis=1)

# Prepare final columns per question:
# building name(s), building numbers, building height, street address, city, state,
# HR department name, assignable SF, total SF, average SF
final_df = merged.copy()

# Ensure CITY and STATE exist (fill blanks if not provided)
for col in ["CITY", "STATE"]:
    if col not in final_df.columns:
        final_df[col] = pd.NA

# Rename areas
final_df.rename(columns={
    "EXT_GROSS_AREA": "Total_SF",
    "ASSIGNABLE_AREA": "Assignable_SF",
}, inplace=True)

# Select and order columns
final_cols = []
# Building identifiers
for c in ["BUILDING_NAME_LONG", "BUILDING_NAME", "BUILDING_NUMBER", "BUILDING_HEIGHT"]:
    if c in final_df.columns:
        final_cols.append(c)
# Address components
if "BUILDING_STREET_ADDRESS" in final_df.columns:
    final_cols.append("BUILDING_STREET_ADDRESS")
if "CITY" in final_df.columns:
    final_cols.append("CITY")
if "STATE" in final_df.columns:
    final_cols.append("STATE")
# HR department
if "HR_DEPARTMENT_NAME" in final_df.columns:
    final_cols.append("HR_DEPARTMENT_NAME")
# Areas
for c in ["Assignable_SF", "Total_SF", "Average_SF"]:
    if c in final_df.columns:
        final_cols.append(c)

answer_df = final_df[final_cols].copy()

# Sort by Assignable_SF desc, then Total_SF desc, then Average_SF desc
sort_cols = [c for c in ["Assignable_SF", "Total_SF", "Average_SF"] if c in answer_df.columns]
answer_df = answer_df.sort_values(by=sort_cols, ascending=[False]*len(sort_cols), na_position="last")

# Assign final result as dict[str, DataFrame]
result = {"buildings_with_metrics": answer_df}