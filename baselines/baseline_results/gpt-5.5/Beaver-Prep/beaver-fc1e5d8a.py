import pandas as pd
import numpy as np

rooms = tables["table_1"].copy()
buildings = tables["table_4"].copy()
floors = tables["table_9"].copy()

def unique_join(s):
    vals = s.dropna().astype(str).str.strip()
    vals = vals[vals.ne("")]
    return ", ".join(sorted(vals.unique())) if len(vals) else pd.NA

# Room-level aggregations by building
room_agg = (
    rooms.groupby("BUILDING_KEY", as_index=False)
    .agg(
        department_names=("DEPT_CODE", unique_join),
        organizations=("ORGANIZATION_NAME", unique_join),
        total_number_of_rooms=("fac_room_key", "nunique")
    )
)

# Floor order / labels by building
floor_work = floors.copy()
floor_work["floor_order"] = pd.to_numeric(floor_work["LEVEL_ID"], errors="coerce")
floor_work["floor_order"] = floor_work["floor_order"].fillna(
    pd.to_numeric(floor_work["FLOOR_SORT_SEQUENCE"], errors="coerce")
)

valid_floors = floor_work.dropna(subset=["floor_order"]).copy()

lowest = (
    valid_floors.sort_values(["BUILDING_KEY", "floor_order"])
    .drop_duplicates("BUILDING_KEY", keep="first")
    [["BUILDING_KEY", "FLOOR"]]
    .rename(columns={"FLOOR": "lowest_floor_number"})
)

highest = (
    valid_floors.sort_values(["BUILDING_KEY", "floor_order"], ascending=[True, False])
    .drop_duplicates("BUILDING_KEY", keep="first")
    [["BUILDING_KEY", "FLOOR"]]
    .rename(columns={"FLOOR": "highest_floor_number"})
)

floor_agg = lowest.merge(highest, on="BUILDING_KEY", how="outer")

# Building names
building_dim = (
    buildings[["FAC_BUILDING_KEY", "BUILDING_NAME"]]
    .drop_duplicates()
    .rename(columns={"FAC_BUILDING_KEY": "BUILDING_KEY", "BUILDING_NAME": "building_name"})
)

out = (
    building_dim
    .merge(room_agg, on="BUILDING_KEY", how="left")
    .merge(floor_agg, on="BUILDING_KEY", how="left")
)

# Prefer room-derived count; fall back to building table NUM_OF_ROOMS if needed
room_count_fallback = (
    buildings[["FAC_BUILDING_KEY", "NUM_OF_ROOMS"]]
    .drop_duplicates()
    .rename(columns={"FAC_BUILDING_KEY": "BUILDING_KEY"})
)
out = out.merge(room_count_fallback, on="BUILDING_KEY", how="left")
out["total_number_of_rooms"] = out["total_number_of_rooms"].fillna(out["NUM_OF_ROOMS"]).astype("Int64")

out = (
    out[[
        "BUILDING_KEY",
        "building_name",
        "department_names",
        "organizations",
        "highest_floor_number",
        "lowest_floor_number",
        "total_number_of_rooms"
    ]]
    .sort_values("BUILDING_KEY", key=lambda s: s.astype(str))
    .reset_index(drop=True)
)

result = {"building_department_organization_floor_room_summary": out}
