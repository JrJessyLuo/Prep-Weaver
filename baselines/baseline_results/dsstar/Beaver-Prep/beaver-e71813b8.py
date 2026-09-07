import pandas as pd

# Source tables from the provided 'tables' dict
fac_rooms = tables['table_1'].copy()

# Ensure BUILDING_KEY is string and filter for Building 45
fac_rooms["BUILDING_KEY"] = fac_rooms["BUILDING_KEY"].astype(str)
fac_rooms_bldg_45 = fac_rooms[fac_rooms["BUILDING_KEY"] == "45"].copy()

# Select and rename needed columns
cols_map = {
    "ROOM_FULL_NAME": "room_full_name",
    "AREA": "area",
    "MAJOR_USE_DESC": "major_use_desc",
    "ORGANIZATION_NAME": "organization_name",
    "ROOM": "room"
}
selected = fac_rooms_bldg_45[list(cols_map.keys())].rename(columns=cols_map)

# Clean up potential oddities
selected["area"] = pd.to_numeric(selected["area"], errors="coerce")

# Aggregation A: room count per major use
rooms_per_major_use = (
    selected
    .groupby("major_use_desc", dropna=False)
    .agg(room_count=("room", "nunique"))
    .reset_index()
)

# Aggregation B: total area per organization
area_per_org = (
    selected
    .groupby("organization_name", dropna=False, as_index=False)["area"]
    .sum(min_count=1)
    .rename(columns={"area": "total_area"})
)

# Prepare final detailed room list augmented with aggregates
# Merge room-level with room counts per major use
detailed_with_major_counts = selected.merge(
    rooms_per_major_use, on="major_use_desc", how="left"
)

# Merge with total area per organization
final_rooms = detailed_with_major_counts.merge(
    area_per_org, on="organization_name", how="left"
)

# Order columns for clarity
final_rooms = final_rooms[[
    "room", "room_full_name", "area", "major_use_desc",
    "organization_name", "room_count", "total_area"
]]

# Build result mapping as required
result = {
    "building45_rooms_with_counts_and_org_areas": final_rooms,
    "rooms_per_major_use": rooms_per_major_use.sort_values("room_count", ascending=False).reset_index(drop=True),
    "area_per_organization": area_per_org.sort_values("total_area", ascending=False).reset_index(drop=True),
}