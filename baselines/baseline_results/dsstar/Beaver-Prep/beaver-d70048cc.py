import pandas as pd

# Access input tables from the provided `tables` dict
fac_rooms = tables['table_1'].copy()         # FAC_ROOMS.pkl
space_detail = tables['table_5'].copy()      # SPACE_DETAIL.pkl
fac_building = tables['table_6'].copy()      # FAC_BUILDING.pkl
space_supervisor_usage = tables['table_10'].copy()  # SPACE_SUPERVISOR_USAGE.pkl

# 1) Prepare and inspect-like setup (no prints per guideline)
fac_rooms_cols = ["fac_room_key","BUILDING_KEY","FLOOR","FLOOR_KEY","ROOM","SPACE_ID","AREA","ROOM_FULL_NAME","ACCESS_LEVEL"]
space_detail_cols = ["BUILDING_KEY","FLOOR_KEY","SPACE_UNIT_KEY","SPACE_USAGE_KEY","BUILDING_ROOM","ROOM_NUMBER","ROOM_SQUARE_FOOTAGE","BUILDING_COMPONENT"]
fac_building_cols = ["FAC_BUILDING_KEY","BUILDING_NUMBER","BUILDING_NAME_LONG","ACCESS_LEVEL_NAME","LATITUDE_WGS","LONGITUDE_WGS"]

# Keep only relevant columns if present
fac_rooms = fac_rooms[[c for c in fac_rooms_cols if c in fac_rooms.columns]].copy()
space_detail = space_detail[[c for c in space_detail_cols if c in space_detail.columns]].copy()
fac_building = fac_building[[c for c in fac_building_cols if c in fac_building.columns]].copy()

# 2) Normalize key types and create normalized room identifiers
for col in ["BUILDING_KEY","FLOOR_KEY"]:
    if col in fac_rooms.columns:
        fac_rooms[col] = fac_rooms[col].astype(str)
    if col in space_detail.columns:
        space_detail[col] = space_detail[col].astype(str)

if "ROOM" in fac_rooms.columns:
    fac_rooms["ROOM_norm"] = fac_rooms["ROOM"].astype(str).str.strip()
if "ROOM_NUMBER" in space_detail.columns:
    space_detail["ROOM_NUMBER_norm"] = space_detail["ROOM_NUMBER"].astype(str).str.strip()

# 3) Attempt three-key join: BUILDING_KEY, FLOOR_KEY, ROOM vs ROOM_NUMBER
space_detail_merge = space_detail.rename(columns={"ROOM_NUMBER_norm":"ROOM_norm"})
three_key_cols = ["BUILDING_KEY","FLOOR_KEY","ROOM_norm"]
sd_pick_cols = [c for c in ["BUILDING_KEY","FLOOR_KEY","ROOM_norm","BUILDING_ROOM","ROOM_SQUARE_FOOTAGE","BUILDING_COMPONENT"] if c in space_detail_merge.columns]
test_merge = fac_rooms.merge(
    space_detail_merge[sd_pick_cols],
    on=[c for c in three_key_cols if c in fac_rooms.columns and c in space_detail_merge.columns],
    how="left",
    validate="m:1" if all(c in space_detail_merge.columns for c in three_key_cols) else "m:m"
)

# 4) Alternative join using derived BUILDING_ROOM = BUILDING_NUMBER-ROOM
fac_building_map = fac_building[["FAC_BUILDING_KEY","BUILDING_NUMBER"]].copy()
if "FAC_BUILDING_KEY" in fac_building_map.columns:
    fac_building_map["FAC_BUILDING_KEY"] = fac_building_map["FAC_BUILDING_KEY"].astype(str)
fac_rooms_w_bnum = fac_rooms.merge(
    fac_building_map,
    left_on="BUILDING_KEY",
    right_on="FAC_BUILDING_KEY",
    how="left"
)

fac_rooms_w_bnum["BUILDING_ROOM_DERIVED"] = (
    fac_rooms_w_bnum.get("BUILDING_NUMBER", "").astype(str).str.strip() + "-" + fac_rooms_w_bnum["ROOM_norm"].astype(str).str.strip()
)

space_detail["BUILDING_ROOM_norm"] = space_detail.get("BUILDING_ROOM", "").astype(str).str.strip()

sd_alt_cols = [c for c in ["BUILDING_ROOM_norm","ROOM_SQUARE_FOOTAGE","BUILDING_COMPONENT","FLOOR_KEY","BUILDING_KEY"] if c in space_detail.columns]
test_merge_alt = fac_rooms_w_bnum.merge(
    space_detail[sd_alt_cols].rename(columns={"BUILDING_ROOM_norm":"BUILDING_ROOM"}),
    left_on="BUILDING_ROOM_DERIVED",
    right_on="BUILDING_ROOM",
    how="left",
    validate="m:1" if "BUILDING_ROOM" in space_detail.columns else "m:m"
)

# 5) Choose better match based on availability of ROOM_SQUARE_FOOTAGE
match_rate = test_merge["BUILDING_ROOM"].notna().mean() if "BUILDING_ROOM" in test_merge.columns else 0.0
match_rate_alt = test_merge_alt["ROOM_SQUARE_FOOTAGE"].notna().mean() if "ROOM_SQUARE_FOOTAGE" in test_merge_alt.columns else 0.0
merged_best = test_merge.copy() if match_rate >= match_rate_alt else test_merge_alt.rename(columns={"BUILDING_ROOM":"BUILDING_ROOM_from_SD"}).copy()

# 6) Compute floor- and building-level totals using FAC_ROOMS AREA
rooms_for_totals = fac_rooms.copy()
for col in ["BUILDING_KEY","FLOOR_KEY"]:
    if col in rooms_for_totals.columns:
        rooms_for_totals[col] = rooms_for_totals[col].astype(str)

floor_totals = (
    rooms_for_totals
    .groupby(["BUILDING_KEY","FLOOR_KEY"], dropna=False, as_index=False)["AREA"]
    .sum()
    .rename(columns={"AREA":"floor_total_area"})
)

bldg_totals = (
    rooms_for_totals
    .groupby(["BUILDING_KEY"], dropna=False, as_index=False)["AREA"]
    .sum()
    .rename(columns={"AREA":"building_total_area"})
)

# Ensure keys as strings in merged_best
if "BUILDING_KEY" in merged_best.columns:
    merged_best["BUILDING_KEY"] = merged_best["BUILDING_KEY"].astype(str)
if "FLOOR_KEY" in merged_best.columns:
    merged_best["FLOOR_KEY"] = merged_best["FLOOR_KEY"].astype(str)

merged_best = merged_best.merge(floor_totals, on=["BUILDING_KEY","FLOOR_KEY"], how="left")
merged_best = merged_best.merge(bldg_totals, on=["BUILDING_KEY"], how="left")

merged_best["pct_room_over_floor"] = merged_best["AREA"] / merged_best["floor_total_area"]
merged_best["pct_room_over_building"] = merged_best["AREA"] / merged_best["building_total_area"]

# 7) Bring in building names
fac_building_names = fac_building[["FAC_BUILDING_KEY","BUILDING_NAME_LONG"]].copy()
fac_building_names["FAC_BUILDING_KEY"] = fac_building_names["FAC_BUILDING_KEY"].astype(str)
merged_best = merged_best.merge(
    fac_building_names,
    left_on="BUILDING_KEY",
    right_on="FAC_BUILDING_KEY",
    how="left"
)

# 8) Bring in organizations and departments occupying rooms from SPACE_SUPERVISOR_USAGE
# Attempt to join via SPACE_UNIT_KEY or SPACE_USAGE_KEY from SPACE_DETAIL mapped to FAC_ROOMS via the selected merge
# First, capture the best linkage keys from SPACE_DETAIL in merged_best
space_keys = []
if "SPACE_UNIT_KEY" in space_detail.columns:
    space_keys.append("SPACE_UNIT_KEY")
if "SPACE_USAGE_KEY" in space_detail.columns:
    space_keys.append("SPACE_USAGE_KEY")

# Reconstruct a mapping from the chosen merge to space_detail keys to facilitate org/department join
if match_rate >= match_rate_alt:
    # three-key path: merge back the keys from space_detail on the same linkage
    sd_for_link = space_detail.rename(columns={"ROOM_NUMBER_norm":"ROOM_norm"})
    link_cols = [c for c in ["BUILDING_KEY","FLOOR_KEY","ROOM_norm"] if c in sd_for_link.columns and c in merged_best.columns]
    add_cols = [c for c in space_keys if c in sd_for_link.columns]
    if add_cols:
        merged_best = merged_best.merge(
            sd_for_link[link_cols + add_cols].drop_duplicates(link_cols),
            on=link_cols,
            how="left"
        )
else:
    # derived BUILDING_ROOM path: merge back via BUILDING_ROOM
    sd_for_link = space_detail.copy()
    sd_for_link["BUILDING_ROOM_norm"] = sd_for_link.get("BUILDING_ROOM", "").astype(str).str.strip()
    add_cols = [c for c in space_keys if c in sd_for_link.columns]
    if add_cols:
        merged_best = merged_best.merge(
            sd_for_link[["BUILDING_ROOM_norm"] + add_cols].rename(columns={"BUILDING_ROOM_norm":"BUILDING_ROOM"}),
            on="BUILDING_ROOM",
            how="left"
        )

# Now attach org and department from SPACE_SUPERVISOR_USAGE
# Guess common keys: SPACE_UNIT_KEY or SPACE_USAGE_KEY
org_cols_candidates = ["ORG_NAME","ORGANIZATION_NAME","ORG","ORGANIZATION"]
dept_cols_candidates = ["DEPARTMENT_NAME","DEPT_NAME","DEPARTMENT","DEPT"]

ssu = space_supervisor_usage.copy()
# Normalize potential join key types
for k in ["SPACE_UNIT_KEY","SPACE_USAGE_KEY"]:
    if k in ssu.columns:
        ssu[k] = ssu[k].astype(str)
    if k in merged_best.columns:
        merged_best[k] = merged_best[k].astype(str)

# Determine available org/department columns
org_col = next((c for c in org_cols_candidates if c in ssu.columns), None)
dept_col = next((c for c in dept_cols_candidates if c in ssu.columns), None)

# Perform the join prioritizing SPACE_UNIT_KEY, then SPACE_USAGE_KEY
if "SPACE_UNIT_KEY" in ssu.columns and "SPACE_UNIT_KEY" in merged_best.columns:
    orgdept = ssu[["SPACE_UNIT_KEY"] + [c for c in [org_col, dept_col] if c]].copy().drop_duplicates("SPACE_UNIT_KEY")
    merged_best = merged_best.merge(orgdept, on="SPACE_UNIT_KEY", how="left")
elif "SPACE_USAGE_KEY" in ssu.columns and "SPACE_USAGE_KEY" in merged_best.columns:
    orgdept = ssu[["SPACE_USAGE_KEY"] + [c for c in [org_col, dept_col] if c]].copy().drop_duplicates("SPACE_USAGE_KEY")
    merged_best = merged_best.merge(orgdept, on="SPACE_USAGE_KEY", how="left")
else:
    # If no keys match, just create empty placeholders
    if org_col is None:
        org_col = "ORGANIZATION_NAME"
    if dept_col is None:
        dept_col = "DEPARTMENT_NAME"
    merged_best[org_col] = pd.NA
    merged_best[dept_col] = pd.NA

# 9) Final selection: room full name, building name, floor number, organization, department, percentages
# Map column names to requested output
out_cols = []

# Room full name
if "ROOM_FULL_NAME" in merged_best.columns:
    out_cols.append("ROOM_FULL_NAME")
else:
    # Fallback to ROOM if full name missing
    if "ROOM" in merged_best.columns:
        merged_best["ROOM_FULL_NAME"] = merged_best["ROOM"]
        out_cols.append("ROOM_FULL_NAME")

# Building name
if "BUILDING_NAME_LONG" in merged_best.columns:
    out_cols.append("BUILDING_NAME_LONG")

# Floor number (prefer numeric FLOOR, else FLOOR_KEY)
if "FLOOR" in merged_best.columns:
    out_cols.append("FLOOR")
elif "FLOOR_KEY" in merged_best.columns:
    out_cols.append("FLOOR_KEY")

# Organization and Department columns
if org_col and org_col in merged_best.columns:
    merged_best.rename(columns={org_col: "ORGANIZATION_NAME_OUT"}, inplace=True)
    out_cols.append("ORGANIZATION_NAME_OUT")
else:
    merged_best["ORGANIZATION_NAME_OUT"] = pd.NA
    out_cols.append("ORGANIZATION_NAME_OUT")

if dept_col and dept_col in merged_best.columns:
    merged_best.rename(columns={dept_col: "DEPARTMENT_NAME_OUT"}, inplace=True)
    out_cols.append("DEPARTMENT_NAME_OUT")
else:
    merged_best["DEPARTMENT_NAME_OUT"] = pd.NA
    out_cols.append("DEPARTMENT_NAME_OUT")

# Percentages and areas
pct_cols = ["AREA","floor_total_area","building_total_area","pct_room_over_floor","pct_room_over_building"]
pct_cols = [c for c in pct_cols if c in merged_best.columns]
out_cols.extend(pct_cols)

final_df = merged_best[out_cols].copy()

# Optional: order/sort for readability (not printed)
sort_cols = [c for c in ["BUILDING_NAME_LONG","FLOOR","ROOM_FULL_NAME"] if c in final_df.columns]
if sort_cols:
    final_df = final_df.sort_values(sort_cols)

# Assign final answer to result dict
result = {"room_details_with_org_dept_and_percentages": final_df}