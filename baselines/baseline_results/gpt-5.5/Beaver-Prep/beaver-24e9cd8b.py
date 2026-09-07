import pandas as pd
import numpy as np

# Select the current building table
building_candidates = []
for name, df in tables.items():
    cols = set(df.columns)
    if {"CAMPUS_SECTOR", "ASSIGNABLE_AREA", "OWNERSHIP_TYPE"}.issubset(cols) and "FISCAL_PERIOD" not in cols:
        building_candidates.append((name, df))

if "table_1" in tables and {"CAMPUS_SECTOR", "ASSIGNABLE_AREA"}.issubset(tables["table_1"].columns):
    bldg = tables["table_1"].copy()
elif building_candidates:
    bldg = sorted(building_candidates, key=lambda x: len(x[1]))[0][1].copy()
else:
    # Fallback to latest historical building table
    hist_candidates = []
    for name, df in tables.items():
        cols = set(df.columns)
        if {"CAMPUS_SECTOR", "ASSIGNABLE_AREA", "FISCAL_PERIOD"}.issubset(cols):
            hist_candidates.append((name, df))
    bldg = sorted(hist_candidates, key=lambda x: len(x[1]))[0][1].copy()
    latest_period = bldg["FISCAL_PERIOD"].max()
    bldg = bldg[bldg["FISCAL_PERIOD"].eq(latest_period)].copy()

# Identify building key
building_key_col = next(
    c for c in ["FCLT_BUILDING_KEY", "FAC_BUILDING_KEY", "BUILDING_KEY", "BUILDING_NUMBER"]
    if c in bldg.columns
)

# Building name column
building_name_col = "BUILDING_NAME_LONG" if "BUILDING_NAME_LONG" in bldg.columns else "BUILDING_NAME"

# Compute total floors from the current floor table
floor_counts = pd.DataFrame(columns=[building_key_col, "total_number_of_floors"])

floor_candidates = []
for name, df in tables.items():
    cols = set(df.columns)
    has_floor = "FLOOR" in cols
    has_current = "FISCAL_PERIOD" not in cols
    possible_bkey = [c for c in ["FCLT_BUILDING_KEY", "FAC_BUILDING_KEY", "BUILDING_KEY"] if c in cols]
    if has_floor and has_current and possible_bkey:
        floor_candidates.append((name, df, possible_bkey[0]))

if floor_candidates:
    floor_name, floors, floor_bkey_col = sorted(floor_candidates, key=lambda x: len(x[1]))[0]
    floor_id_col = next(
        (c for c in ["FCLT_FLOOR_KEY", "FLOOR_KEY", "FLOOR"] if c in floors.columns),
        "FLOOR"
    )
    floor_counts = (
        floors.groupby(floor_bkey_col, dropna=False)[floor_id_col]
        .nunique()
        .reset_index(name="total_number_of_floors")
        .rename(columns={floor_bkey_col: building_key_col})
    )

# Try to compute distinct organization counts if any building-organization bridge exists
org_counts = None
org_id_priority = ["organization_key", "ORGANIZATION_ID", "ORGANIZATION_KEY", "ORGANIZATION", "ORG_KEY", "ORG_ID"]

for name, df in tables.items():
    cols = list(df.columns)
    upper_cols = {c.upper(): c for c in cols}

    possible_bkey = None
    for c in ["FCLT_BUILDING_KEY", "FAC_BUILDING_KEY", "BUILDING_KEY"]:
        if c in cols:
            possible_bkey = c
            break

    possible_org = None
    for c in org_id_priority:
        if c in cols:
            possible_org = c
            break

    if possible_bkey is not None and possible_org is not None:
        tmp = (
            df.dropna(subset=[possible_org])
            .groupby(possible_bkey, dropna=False)[possible_org]
            .nunique()
            .reset_index(name="total_number_of_organizations")
            .rename(columns={possible_bkey: building_key_col})
        )
        org_counts = tmp
        break

if org_counts is None:
    org_counts = pd.DataFrame({
        building_key_col: bldg[building_key_col],
        "total_number_of_organizations": pd.NA
    })

# Infer city/state
def infer_city_state_from_site(site):
    if pd.isna(site):
        return pd.Series([pd.NA, pd.NA], index=["city", "state"])

    s = str(site).upper()

    if "LINCOLN" in s:
        return pd.Series(["Lexington", "MA"], index=["city", "state"])
    if "BATES" in s:
        return pd.Series(["Middleton", "MA"], index=["city", "state"])
    if "HAYSTACK" in s:
        return pd.Series(["Westford", "MA"], index=["city", "state"])
    if "WOODS" in s or "WHOI" in s:
        return pd.Series(["Woods Hole", "MA"], index=["city", "state"])
    if "ENDICOTT" in s:
        return pd.Series(["Dedham", "MA"], index=["city", "state"])
    if "BOSTON" in s:
        return pd.Series(["Boston", "MA"], index=["city", "state"])
    if "CAMBRIDGE" in s or "MIT" in s:
        return pd.Series(["Cambridge", "MA"], index=["city", "state"])

    return pd.Series([pd.NA, pd.NA], index=["city", "state"])

city_candidates = [c for c in bldg.columns if c.upper() in {"CITY", "BUILDING_CITY", "BLDG_CITY", "TOWN", "MUNICIPALITY"}]
state_candidates = [c for c in bldg.columns if c.upper() in {"STATE", "BUILDING_STATE", "BLDG_STATE", "STATE_CODE"}]

if city_candidates:
    bldg["city"] = bldg[city_candidates[0]]
else:
    bldg["city"] = pd.NA

if state_candidates:
    bldg["state"] = bldg[state_candidates[0]]
else:
    bldg["state"] = pd.NA

if "SITE" in bldg.columns:
    inferred_city_state = bldg["SITE"].apply(infer_city_state_from_site)
    bldg["city"] = bldg["city"].combine_first(inferred_city_state["city"])
    bldg["state"] = bldg["state"].combine_first(inferred_city_state["state"])

# Build detail rows
detail = (
    bldg.merge(floor_counts, on=building_key_col, how="left")
        .merge(org_counts, on=building_key_col, how="left")
)

detail["campus_sector"] = detail["CAMPUS_SECTOR"].fillna("(Unknown)")
detail["building_name"] = detail[building_name_col]
detail["total_number_of_floors"] = detail["total_number_of_floors"].fillna(0).astype("Int64")
detail["total_assignable_area"] = detail["ASSIGNABLE_AREA"]
detail["total_number_of_rooms"] = detail["NUM_OF_ROOMS"] if "NUM_OF_ROOMS" in detail.columns else pd.NA
detail["ownership_type"] = detail["OWNERSHIP_TYPE"] if "OWNERSHIP_TYPE" in detail.columns else pd.NA

detail = detail[
    [
        "campus_sector",
        "building_name",
        "city",
        "state",
        "total_number_of_floors",
        "total_assignable_area",
        "total_number_of_rooms",
        "total_number_of_organizations",
        "ownership_type",
    ]
].copy()

# Rank buildings within each sector by descending assignable area
detail = detail.sort_values(
    ["campus_sector", "total_assignable_area", "building_name"],
    ascending=[True, False, True],
    na_position="last"
).reset_index(drop=True)

detail["rank"] = detail.groupby("campus_sector").cumcount() + 1
detail["_row_type"] = 0
detail["_sector_sort"] = detail["campus_sector"]

# Sector subtotal rows
subtotals = (
    detail.groupby("campus_sector", as_index=False, dropna=False)
    .agg(
        total_number_of_floors=("total_number_of_floors", "sum"),
        total_assignable_area=("total_assignable_area", "sum"),
    )
)

subtotals["building_name"] = "Subtotal"
subtotals["city"] = pd.NA
subtotals["state"] = pd.NA
subtotals["total_number_of_rooms"] = pd.NA
subtotals["total_number_of_organizations"] = pd.NA
subtotals["ownership_type"] = pd.NA
subtotals["rank"] = pd.NA
subtotals["_row_type"] = 1
subtotals["_sector_sort"] = subtotals["campus_sector"]

subtotals = subtotals[
    [
        "campus_sector",
        "building_name",
        "city",
        "state",
        "total_number_of_floors",
        "total_assignable_area",
        "total_number_of_rooms",
        "total_number_of_organizations",
        "ownership_type",
        "rank",
        "_row_type",
        "_sector_sort",
    ]
]

# Grand total row
grand_total = pd.DataFrame([{
    "campus_sector": "Grand Total",
    "building_name": "Grand Total",
    "city": pd.NA,
    "state": pd.NA,
    "total_number_of_floors": detail["total_number_of_floors"].sum(),
    "total_assignable_area": detail["total_assignable_area"].sum(),
    "total_number_of_rooms": pd.NA,
    "total_number_of_organizations": pd.NA,
    "ownership_type": pd.NA,
    "rank": pd.NA,
    "_row_type": 2,
    "_sector_sort": "\uffff",
}])

# Combine detail rows, subtotals, and grand total
final = pd.concat([detail, subtotals, grand_total], ignore_index=True, sort=False)

final = final.sort_values(
    ["_sector_sort", "_row_type", "rank"],
    ascending=[True, True, True],
    na_position="last"
).drop(columns=["_row_type", "_sector_sort"]).reset_index(drop=True)

result = {
    "buildings_by_campus_sector": final
}
