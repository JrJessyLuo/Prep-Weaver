import pandas as pd
import numpy as np

# Current buildings and rooms
buildings = tables["table_3"].copy()
rooms = tables["table_10"].copy()

building_key = "FCLT_BUILDING_KEY"
room_building_key = "BUILDING_KEY"
org_col = "ORGANIZATION_KEY"

# Keep MIT buildings and normalize ownership into owned/leased groups
buildings = buildings[
    buildings["SITE"].astype(str).str.strip().str.upper().eq("MIT")
].copy()

ownership_raw = buildings["OWNERSHIP_TYPE"].astype(str).str.strip().str.upper()
buildings["OWNERSHIP_GROUP"] = np.where(
    ownership_raw.str.contains("LEASE", na=False),
    "LEASED",
    np.where(ownership_raw.str.contains("OWN", na=False), "OWNED", ownership_raw)
)

buildings = buildings[buildings["OWNERSHIP_GROUP"].isin(["OWNED", "LEASED"])].copy()
buildings["USAGE_TYPE"] = buildings["BUILDING_USE"].fillna("(Unknown)").astype(str)

# Attach room organizations to building ownership/use
room_orgs = rooms[[room_building_key, org_col]].copy()
room_orgs = room_orgs.dropna(subset=[room_building_key])

room_orgs = room_orgs.merge(
    buildings[[building_key, "OWNERSHIP_GROUP", "USAGE_TYPE"]],
    left_on=room_building_key,
    right_on=building_key,
    how="inner"
)

# Detail rows by ownership and usage
detail = (
    buildings
    .groupby(["OWNERSHIP_GROUP", "USAGE_TYPE"], as_index=False, dropna=False)
    .agg(
        number_of_buildings=(building_key, "nunique"),
        gross_square_footage=("EXT_GROSS_AREA", "sum"),
        number_of_rooms=("NUM_OF_ROOMS", "sum")
    )
)

detail_orgs = (
    room_orgs
    .groupby(["OWNERSHIP_GROUP", "USAGE_TYPE"], as_index=False, dropna=False)
    .agg(number_of_associated_organizations=(org_col, "nunique"))
)

detail = detail.merge(
    detail_orgs,
    on=["OWNERSHIP_GROUP", "USAGE_TYPE"],
    how="left"
)
detail["number_of_associated_organizations"] = (
    detail["number_of_associated_organizations"].fillna(0).astype(int)
)
detail["row_type"] = "detail"

# Subtotal rows by ownership
subtotals = (
    buildings
    .groupby("OWNERSHIP_GROUP", as_index=False)
    .agg(
        number_of_buildings=(building_key, "nunique"),
        gross_square_footage=("EXT_GROSS_AREA", "sum"),
        number_of_rooms=("NUM_OF_ROOMS", "sum")
    )
)

subtotal_orgs = (
    room_orgs
    .groupby("OWNERSHIP_GROUP", as_index=False)
    .agg(number_of_associated_organizations=(org_col, "nunique"))
)

subtotals = subtotals.merge(subtotal_orgs, on="OWNERSHIP_GROUP", how="left")
subtotals["number_of_associated_organizations"] = (
    subtotals["number_of_associated_organizations"].fillna(0).astype(int)
)
subtotals["USAGE_TYPE"] = ""
subtotals["row_type"] = "subtotal"

# Grand total row
grand_total = pd.DataFrame([{
    "OWNERSHIP_GROUP": "",
    "USAGE_TYPE": "",
    "number_of_buildings": buildings[building_key].nunique(),
    "gross_square_footage": buildings["EXT_GROSS_AREA"].sum(),
    "number_of_rooms": buildings["NUM_OF_ROOMS"].sum(),
    "number_of_associated_organizations": room_orgs[org_col].nunique(),
    "row_type": "grand_total"
}])

# Combine and sort
combined = pd.concat([detail, subtotals, grand_total], ignore_index=True)

ownership_order = {"OWNED": 0, "LEASED": 1, "": 2}
row_order = {"detail": 0, "subtotal": 1, "grand_total": 2}

combined["ownership_sort"] = combined["OWNERSHIP_GROUP"].map(ownership_order).fillna(99)
combined["row_sort"] = combined["row_type"].map(row_order)
combined["usage_sort"] = combined["USAGE_TYPE"].astype(str)

combined = combined.sort_values(
    ["ownership_sort", "row_sort", "usage_sort"],
    kind="stable"
).reset_index(drop=True)

# Display ownership only when it changes from the previous row; totals remain blank
combined["Ownership Type"] = ""
detail_mask = combined["row_type"].eq("detail")
change_mask = combined["OWNERSHIP_GROUP"].ne(combined["OWNERSHIP_GROUP"].shift())
combined.loc[detail_mask & change_mask, "Ownership Type"] = combined.loc[
    detail_mask & change_mask, "OWNERSHIP_GROUP"
]

combined["Usage Type"] = np.where(detail_mask, combined["USAGE_TYPE"], "")

# Format gross square footage
combined["Gross Square Footage"] = combined["gross_square_footage"].round(0).astype("int64").map("{:,}".format)

final = combined.rename(columns={
    "number_of_buildings": "Number of Buildings",
    "number_of_rooms": "Number of Rooms",
    "number_of_associated_organizations": "Number of Associated Organizations"
})[
    [
        "Ownership Type",
        "Usage Type",
        "Number of Buildings",
        "Gross Square Footage",
        "Number of Rooms",
        "Number of Associated Organizations"
    ]
]

result = {
    "mit_buildings_owned_leased_summary": final
}
