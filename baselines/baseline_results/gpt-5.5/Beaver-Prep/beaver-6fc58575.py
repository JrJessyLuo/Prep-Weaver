import pandas as pd
import numpy as np

rooms = tables["table_1"].copy()
buildings = tables["table_5"].copy()
floors = tables["table_10"].copy()

# Standardize join keys as strings
rooms["BUILDING_KEY"] = rooms["BUILDING_KEY"].astype(str)
rooms["FLOOR_KEY"] = rooms["FLOOR_KEY"].astype(str)
buildings["FAC_BUILDING_KEY"] = buildings["FAC_BUILDING_KEY"].astype(str)
floors["FCLT_FLOOR_KEY"] = floors["FCLT_FLOOR_KEY"].astype(str)

# Keep only needed building/floor attributes
building_cols = buildings[[
    "FAC_BUILDING_KEY",
    "BUILDING_NAME",
    "BUILDING_NAME_LONG",
    "ASSIGNABLE_AREA"
]].rename(columns={
    "FAC_BUILDING_KEY": "BUILDING_KEY",
    "ASSIGNABLE_AREA": "BUILDING_ASSIGNABLE_AREA"
})

floor_cols = floors[[
    "FCLT_FLOOR_KEY",
    "ASSIGNABLE_AREA"
]].rename(columns={
    "FCLT_FLOOR_KEY": "FLOOR_KEY",
    "ASSIGNABLE_AREA": "FLOOR_ASSIGNABLE_AREA"
})

df = (
    rooms
    .merge(building_cols, on="BUILDING_KEY", how="left")
    .merge(floor_cols, on="FLOOR_KEY", how="left")
)

# Use ROOM_FULL_NAME when available; otherwise fall back to SPACE_ID / building-room identifiers
df["room_full_name"] = (
    df["ROOM_FULL_NAME"]
    .combine_first(df["SPACE_ID"])
    .combine_first(df["fac_room_key"])
)

df["building_name"] = df["BUILDING_NAME_LONG"].combine_first(df["BUILDING_NAME"])

df["percent_room_area_over_assignable_floor_area"] = np.where(
    df["FLOOR_ASSIGNABLE_AREA"].notna() & (df["FLOOR_ASSIGNABLE_AREA"] != 0),
    df["AREA"] / df["FLOOR_ASSIGNABLE_AREA"] * 100,
    np.nan
)

df["percent_room_area_over_assignable_building_area"] = np.where(
    df["BUILDING_ASSIGNABLE_AREA"].notna() & (df["BUILDING_ASSIGNABLE_AREA"] != 0),
    df["AREA"] / df["BUILDING_ASSIGNABLE_AREA"] * 100,
    np.nan
)

final = df[[
    "room_full_name",
    "building_name",
    "FLOOR",
    "ORGANIZATION_NAME",
    "DEPT_CODE",
    "AREA",
    "FLOOR_ASSIGNABLE_AREA",
    "BUILDING_ASSIGNABLE_AREA",
    "percent_room_area_over_assignable_floor_area",
    "percent_room_area_over_assignable_building_area"
]].rename(columns={
    "FLOOR": "floor_number",
    "ORGANIZATION_NAME": "organization_occupying_room",
    "DEPT_CODE": "department_occupying_room",
    "AREA": "room_area"
})

result = {
    "room_occupancy_area_percentages": final.reset_index(drop=True)
}
