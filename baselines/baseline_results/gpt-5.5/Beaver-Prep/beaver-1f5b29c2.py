import pandas as pd
import numpy as np

def clean_str(s):
    return s.astype("string").str.strip().replace({"": pd.NA})

def fmt_int(x):
    if pd.isna(x):
        return ""
    return f"{float(x):,.0f}"

def fmt_pct(x):
    if pd.isna(x):
        return ""
    return f"{float(x):.2f}"

rooms = tables["table_3"].copy()
buildings = tables["table_6"].copy() if "table_6" in tables else tables["table_4"].copy()

rooms["building_key"] = clean_str(rooms["BUILDING_KEY"])
rooms["Floor Number"] = clean_str(rooms["FLOOR"]).fillna("")
rooms["Room Number"] = clean_str(rooms["ROOM"]).fillna("")
rooms["Organization Name"] = clean_str(rooms["ORGANIZATION_NAME"]).fillna("")
rooms["Area"] = pd.to_numeric(rooms["AREA"], errors="coerce").fillna(0)

room_key = clean_str(rooms["fac_room_key"]) if "fac_room_key" in rooms.columns else pd.Series(pd.NA, index=rooms.index)
fallback_room_key = (
    rooms["building_key"].fillna("")
    + "-"
    + rooms["Floor Number"].fillna("")
    + "-"
    + rooms["Room Number"].fillna("")
)
rooms["room_uid"] = room_key.fillna(fallback_room_key)
rooms.loc[rooms["room_uid"].eq("--") | rooms["room_uid"].isna(), "room_uid"] = rooms.index.astype(str)

bldg_key_col = "FCLT_BUILDING_KEY" if "FCLT_BUILDING_KEY" in buildings.columns else "FAC_BUILDING_KEY"
buildings["building_key"] = clean_str(buildings[bldg_key_col])

name_long = clean_str(buildings["BUILDING_NAME_LONG"]) if "BUILDING_NAME_LONG" in buildings.columns else pd.Series(pd.NA, index=buildings.index)
name_short = clean_str(buildings["BUILDING_NAME"]) if "BUILDING_NAME" in buildings.columns else pd.Series(pd.NA, index=buildings.index)
buildings["Building Name"] = name_long.fillna(name_short).fillna(buildings["building_key"])

buildings["Ownership Type"] = clean_str(buildings["OWNERSHIP_TYPE"]).fillna("")
buildings["building_sort"] = clean_str(buildings["BUILDING_SORT"]) if "BUILDING_SORT" in buildings.columns else buildings["building_key"]
buildings["building_sort"] = buildings["building_sort"].fillna(buildings["building_key"])

buildings_dim = buildings[
    ["building_key", "Building Name", "Ownership Type", "building_sort"]
].drop_duplicates("building_key")

df = rooms.merge(buildings_dim, on="building_key", how="left")
df["Building Name"] = df["Building Name"].fillna(df["building_key"]).fillna("")
df["Ownership Type"] = df["Ownership Type"].fillna("")
df["building_sort"] = df["building_sort"].fillna(df["building_key"]).fillna("")

if "table_9" in tables:
    floors = tables["table_9"].copy()
    floors["building_key"] = clean_str(floors["FCLT_BUILDING_KEY"])
    floors["Floor Number"] = clean_str(floors["FLOOR"]).fillna("")
    floors["floor_sort"] = pd.to_numeric(floors["FLOOR_SORT_SEQUENCE"], errors="coerce")
    floors_dim = floors[["building_key", "Floor Number", "floor_sort"]].drop_duplicates(
        ["building_key", "Floor Number"]
    )
    df = df.merge(floors_dim, on=["building_key", "Floor Number"], how="left")
else:
    df["floor_sort"] = np.nan

floor_numeric = pd.to_numeric(df["Floor Number"], errors="coerce")
df["floor_sort"] = df["floor_sort"].fillna(floor_numeric).fillna(999999)
df["room_sort"] = pd.to_numeric(
    df["Room Number"].astype(str).str.extract(r"(\d+)", expand=False),
    errors="coerce"
).fillna(999999)

building_area = df.groupby("building_key", dropna=False)["Area"].sum()
grand_area = df["Area"].sum()

detail_keys = [
    "building_key", "Building Name", "building_sort",
    "Floor Number", "floor_sort",
    "Room Number", "room_sort",
    "Ownership Type", "Organization Name"
]

detail = (
    df.groupby(detail_keys, dropna=False)
      .agg(**{"Number of Rooms": ("room_uid", "nunique"), "Area": ("Area", "sum")})
      .reset_index()
)
detail["Area %"] = detail["Area"] / detail["building_key"].map(building_area) * 100
detail["row_level"] = 0

floor_keys = [
    "building_key", "Building Name", "building_sort",
    "Floor Number", "floor_sort",
    "Ownership Type"
]

floor_subtotal = (
    df.groupby(floor_keys, dropna=False)
      .agg(**{"Number of Rooms": ("room_uid", "nunique"), "Area": ("Area", "sum")})
      .reset_index()
)
floor_subtotal["Room Number"] = "Floor Subtotal"
floor_subtotal["room_sort"] = 9999998
floor_subtotal["Organization Name"] = "All Organizations"
floor_subtotal["Area %"] = floor_subtotal["Area"] / floor_subtotal["building_key"].map(building_area) * 100
floor_subtotal["row_level"] = 1

building_keys = ["building_key", "Building Name", "building_sort", "Ownership Type"]

building_subtotal = (
    df.groupby(building_keys, dropna=False)
      .agg(**{"Number of Rooms": ("room_uid", "nunique"), "Area": ("Area", "sum")})
      .reset_index()
)
building_subtotal["Floor Number"] = "All Floors"
building_subtotal["floor_sort"] = 9999998
building_subtotal["Room Number"] = "Building Subtotal"
building_subtotal["room_sort"] = 9999998
building_subtotal["Organization Name"] = "All Organizations"
building_subtotal["Area %"] = np.where(grand_area != 0, building_subtotal["Area"] / grand_area * 100, np.nan)
building_subtotal["row_level"] = 2

grand_total = pd.DataFrame([{
    "building_key": "",
    "Building Name": "Grand Total",
    "building_sort": "~~~~",
    "Floor Number": "",
    "floor_sort": 9999999,
    "Room Number": "",
    "room_sort": 9999999,
    "Ownership Type": "",
    "Organization Name": "All Organizations",
    "Number of Rooms": df["room_uid"].nunique(),
    "Area": grand_area,
    "Area %": 100.0 if grand_area != 0 else np.nan,
    "row_level": 3
}])

report = pd.concat(
    [detail, floor_subtotal, building_subtotal, grand_total],
    ignore_index=True,
    sort=False
)

report = report.sort_values(
    ["building_sort", "Building Name", "floor_sort", "Floor Number", "row_level", "room_sort", "Room Number", "Organization Name"],
    kind="mergesort"
).reset_index(drop=True)

final_cols = [
    "Building Name",
    "Floor Number",
    "Room Number",
    "Ownership Type",
    "Organization Name",
    "Number of Rooms",
    "Area",
    "Area %"
]

report = report[final_cols].copy()
report["Number of Rooms"] = report["Number of Rooms"].apply(fmt_int)
report["Area"] = report["Area"].apply(fmt_int)
report["Area %"] = report["Area %"].apply(fmt_pct)

result = {"room_area_report": report}
