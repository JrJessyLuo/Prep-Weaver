import pandas as pd
import numpy as np

def clean_str(s):
    return s.astype("string").str.strip()

def clean_code(s):
    return pd.to_numeric(s, errors="coerce").astype("Int64").astype("string")

# Source tables
rooms = tables["table_1"].copy()
room_orgs = tables["table_2"].copy()
buildings = tables["table_3"].copy()
space_units = tables["table_6"].copy()
space_usages = tables["table_10"].copy()

# Normalize keys
rooms["BUILDING_KEY_N"] = clean_str(rooms["BUILDING_KEY"])
rooms["FLOOR_N"] = clean_str(rooms["FLOOR_KEY"])
rooms["BUILDING_COMPONENT_N"] = clean_str(rooms["BUILDING_COMPONENT"])
rooms["SPACE_UNIT_CODE_N"] = clean_code(rooms["SPACE_UNIT_KEY"])
rooms["SPACE_USAGE_KEY_N"] = clean_code(rooms["SPACE_USAGE_KEY"])

room_orgs["BUILDING_COMPONENT_N"] = clean_str(room_orgs["BUILDING_COMPONENT"])
room_orgs["FLOOR_N"] = clean_str(room_orgs["FLOOR"])
room_orgs["SPACE_UNIT_CODE_N"] = clean_code(room_orgs["SPACE_UNIT_CODE"])

buildings["BUILDING_KEY_N"] = clean_str(buildings["BUILDING_KEY"])

space_units["SPACE_UNIT_CODE_N"] = clean_code(space_units["SPACE_UNIT_CODE"])

space_usages["SPACE_USAGE_KEY_N"] = clean_code(space_usages["space_usage_key"])

# Filter to building 36 rooms
b36_rooms = rooms.loc[rooms["BUILDING_KEY_N"].eq("36")].copy()

# Add organization IDs from table_2 at the room level
org_cols = [
    "BUILDING_ROOM",
    "BUILDING_COMPONENT_N",
    "FLOOR_N",
    "HR_ORG_UNIT_ID"
]
room_orgs_dedup = room_orgs[org_cols].drop_duplicates()

b36_rooms = b36_rooms.merge(
    room_orgs_dedup,
    on=["BUILDING_ROOM", "BUILDING_COMPONENT_N", "FLOOR_N"],
    how="left"
)

# Counts on the same building and floor
floor_counts = (
    b36_rooms
    .groupby(["BUILDING_KEY_N", "FLOOR_N"], dropna=False)
    .agg(
        number_of_organizations=("HR_ORG_UNIT_ID", "nunique"),
        number_of_space_units=("SPACE_UNIT_CODE_N", "nunique")
    )
    .reset_index()
)

# Building details
building_details = buildings.loc[
    buildings["BUILDING_KEY_N"].eq("36"),
    ["BUILDING_KEY_N", "BUILDING_NAME", "BUILDING_STREET_ADDRESS"]
].drop_duplicates("BUILDING_KEY_N")

# Space unit lookup
space_unit_lookup = space_units[
    ["SPACE_UNIT_CODE_N", "SPACE_UNIT"]
].drop_duplicates("SPACE_UNIT_CODE_N")

# Space usage lookup
space_usage_lookup = space_usages[
    ["SPACE_USAGE_KEY_N", "SPACE_USAGE"]
].drop_duplicates("SPACE_USAGE_KEY_N")

# Final result: distinct space unit / floor / usage combinations for building 36
out = (
    b36_rooms
    .merge(building_details, on="BUILDING_KEY_N", how="left")
    .merge(space_unit_lookup, on="SPACE_UNIT_CODE_N", how="left")
    .merge(space_usage_lookup, on="SPACE_USAGE_KEY_N", how="left")
    .merge(floor_counts, on=["BUILDING_KEY_N", "FLOOR_N"], how="left")
)

out["space_unit"] = out["SPACE_UNIT"].fillna(out["SPACE_UNIT_CODE_N"])

out = (
    out[[
        "space_unit",
        "SPACE_UNIT_CODE_N",
        "FLOOR_N",
        "BUILDING_NAME",
        "BUILDING_STREET_ADDRESS",
        "SPACE_USAGE",
        "number_of_organizations",
        "number_of_space_units"
    ]]
    .drop_duplicates()
    .rename(columns={
        "SPACE_UNIT_CODE_N": "space_unit_code",
        "FLOOR_N": "floor",
        "BUILDING_NAME": "building_name",
        "BUILDING_STREET_ADDRESS": "building_street_address",
        "SPACE_USAGE": "space_usage"
    })
    .sort_values(["floor", "space_unit", "space_usage"], na_position="last")
    .reset_index(drop=True)
)

result = {
    "building_36_space_units": out
}
