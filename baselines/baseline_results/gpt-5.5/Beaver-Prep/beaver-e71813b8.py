import pandas as pd

rooms = tables["table_1"].copy()

# Filter to building 45
b45 = rooms[rooms["BUILDING_KEY"].astype(str).str.strip().eq("45")].copy()

# Create a usable full room name, falling back to building-room key when ROOM_FULL_NAME is missing
b45["room_full_name"] = b45["ROOM_FULL_NAME"].where(
    b45["ROOM_FULL_NAME"].notna() & (b45["ROOM_FULL_NAME"].astype(str).str.strip() != ""),
    b45["fac_room_key"]
)

# Count rooms per major use within building 45
b45["room_count_per_major_use"] = (
    b45.groupby("MAJOR_USE_DESC", dropna=False)["fac_room_key"]
       .transform("count")
)

# Total area occupied by each organization within building 45
b45["total_area_by_organization"] = (
    b45.groupby("ORGANIZATION_NAME", dropna=False)["AREA"]
       .transform("sum")
)

# Final room-level listing
out = b45[
    [
        "fac_room_key",
        "room_full_name",
        "AREA",
        "MAJOR_USE_DESC",
        "ORGANIZATION_NAME",
        "room_count_per_major_use",
        "total_area_by_organization",
    ]
].rename(
    columns={
        "fac_room_key": "room_key",
        "AREA": "area",
        "MAJOR_USE_DESC": "major_use",
        "ORGANIZATION_NAME": "organization",
    }
)

out = out.sort_values(["major_use", "organization", "room_key"], na_position="last").reset_index(drop=True)

result = {
    "building_45_rooms": out
}
