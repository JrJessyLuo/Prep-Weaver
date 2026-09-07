import pandas as pd
import numpy as np

rooms = tables["table_1"].copy()
buildings = tables["table_6"].copy()
room_names = tables["table_5"].copy()

def norm_str(s):
    return s.astype("string").str.strip()

# Standardize join keys
rooms["building_key_join"] = norm_str(rooms["BUILDING_KEY"])
rooms["floor_join"] = norm_str(rooms["FLOOR"])
rooms["building_room_join"] = norm_str(rooms["fac_room_key"])

buildings["building_key_join"] = norm_str(buildings["FAC_BUILDING_KEY"])

room_names["building_room_join"] = norm_str(room_names["BUILDING_ROOM"])
room_names = room_names[["building_room_join", "BUILDING_ROOM_NAME"]].drop_duplicates("building_room_join")

# Add room display names from room dimension where available
rooms = rooms.merge(room_names, on="building_room_join", how="left")

rooms["room_full_name_final"] = (
    rooms["ROOM_FULL_NAME"]
    .combine_first(rooms["BUILDING_ROOM_NAME"])
    .combine_first(rooms["SPACE_ID"])
    .combine_first(rooms["fac_room_key"])
)

# Compute floor and building room-area totals
rooms["room_area_sqft"] = pd.to_numeric(rooms["AREA"], errors="coerce")

rooms["floor_area_sqft"] = rooms.groupby(
    ["building_key_join", "floor_join"], dropna=False
)["room_area_sqft"].transform("sum")

rooms["building_room_area_sqft"] = rooms.groupby(
    "building_key_join", dropna=False
)["room_area_sqft"].transform("sum")

# Join building details
building_cols = [
    "building_key_join",
    "BUILDING_NAME",
    "BUILDING_NAME_LONG",
    "ASSIGNABLE_AREA",
    "EXT_GROSS_AREA",
]
buildings_small = buildings[building_cols].drop_duplicates("building_key_join")

df = rooms.merge(buildings_small, on="building_key_join", how="left")

# Prefer official assignable building area; fall back to summed room area
df["building_area_sqft"] = pd.to_numeric(df["ASSIGNABLE_AREA"], errors="coerce")
df["building_area_sqft"] = df["building_area_sqft"].where(
    df["building_area_sqft"].gt(0),
    df["building_room_area_sqft"]
)

df["percent_of_floor_area"] = np.where(
    df["floor_area_sqft"].gt(0),
    df["room_area_sqft"] / df["floor_area_sqft"] * 100,
    np.nan
)

df["percent_of_building_area"] = np.where(
    df["building_area_sqft"].gt(0),
    df["room_area_sqft"] / df["building_area_sqft"] * 100,
    np.nan
)

output = pd.DataFrame({
    "room_key": df["fac_room_key"],
    "room_full_name": df["room_full_name_final"],
    "building_key": df["BUILDING_KEY"],
    "building_name": df["BUILDING_NAME"].combine_first(df["BUILDING_NAME_LONG"]),
    "building_name_long": df["BUILDING_NAME_LONG"],
    "floor_number": df["FLOOR"],
    "room_number": df["ROOM"],
    "organization_key": df["ORGANIZATION_KEY"],
    "organization_occupying": df["ORGANIZATION_NAME"],
    "department_code": df["DEPT_CODE"],
    "department_name": df["ORGANIZATION_NAME"],
    "room_area_sqft": df["room_area_sqft"],
    "floor_area_sqft": df["floor_area_sqft"],
    "building_area_sqft": df["building_area_sqft"],
    "percent_of_floor_area": df["percent_of_floor_area"],
    "percent_of_building_area": df["percent_of_building_area"],
})

output = output.sort_values(
    ["building_key", "floor_number", "room_number"],
    na_position="last"
).reset_index(drop=True)

result = {
    "room_area_percentages": output
}
