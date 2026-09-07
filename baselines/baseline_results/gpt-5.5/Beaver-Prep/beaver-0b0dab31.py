import pandas as pd
import numpy as np

# Identify the Stata building from the buildings table
buildings = tables["table_5"].copy()
stata_building_keys = buildings.loc[
    buildings["BUILDING_NAME_LONG"].astype(str).str.contains("stata", case=False, na=False)
    | buildings["BUILDING_NAME"].astype(str).str.contains("stata", case=False, na=False),
    "FCLT_BUILDING_KEY"
].astype(str).unique()

# Use the current full room table
rooms = tables["table_2"].copy()

# Filter to Stata building rooms with a department name
stata_rooms = rooms[
    rooms["BUILDING_KEY"].astype(str).isin(stata_building_keys)
    & rooms["ORGANIZATION_NAME"].notna()
].copy()

# Department-level aggregates by floor
dept = (
    stata_rooms
    .groupby(["FLOOR_KEY", "ORGANIZATION_NAME"], dropna=False)
    .agg(
        num_rooms=("fac_room_key", "count"),
        total_area=("AREA", "sum")
    )
    .reset_index()
)

dept["avg_area"] = dept["total_area"] / dept["num_rooms"]

# Floor subtotals
floor_subtotals = (
    stata_rooms
    .groupby("FLOOR_KEY", dropna=False)
    .agg(
        num_rooms=("fac_room_key", "count"),
        total_area=("AREA", "sum")
    )
    .reset_index()
)
floor_subtotals["avg_area"] = floor_subtotals["total_area"] / floor_subtotals["num_rooms"]

# Grand total
grand_total = pd.DataFrame([{
    "num_rooms": stata_rooms["fac_room_key"].count(),
    "total_area": stata_rooms["AREA"].sum()
}])
grand_total["avg_area"] = grand_total["total_area"] / grand_total["num_rooms"]

# Build ordered output with department rows followed by each floor subtotal
rows = []
for floor_key, g in dept.sort_values(["FLOOR_KEY", "ORGANIZATION_NAME"]).groupby("FLOOR_KEY", sort=False):
    g = g.sort_values("ORGANIZATION_NAME").copy()
    first = True

    for _, r in g.iterrows():
        rows.append({
            "Floor Key": floor_key if first else "",
            "Department Name": r["ORGANIZATION_NAME"],
            "Number of Rooms": r["num_rooms"],
            "Total Area": r["total_area"],
            "Average Area": r["avg_area"]
        })
        first = False

    st = floor_subtotals.loc[floor_subtotals["FLOOR_KEY"] == floor_key].iloc[0]
    rows.append({
        "Floor Key": "",
        "Department Name": "",
        "Number of Rooms": st["num_rooms"],
        "Total Area": st["total_area"],
        "Average Area": st["avg_area"]
    })

# Add grand total row
gt = grand_total.iloc[0]
rows.append({
    "Floor Key": "",
    "Department Name": "",
    "Number of Rooms": gt["num_rooms"],
    "Total Area": gt["total_area"],
    "Average Area": gt["avg_area"]
})

out = pd.DataFrame(rows)

# Round to integers and format with commas
for col in ["Number of Rooms", "Total Area", "Average Area"]:
    out[col] = out[col].round(0).astype("Int64").map(lambda x: "" if pd.isna(x) else f"{x:,}")

result = {
    "stata_floor_department_room_area_summary": out
}
