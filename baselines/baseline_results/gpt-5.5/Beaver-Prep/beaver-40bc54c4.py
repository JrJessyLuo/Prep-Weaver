import pandas as pd

def _key(s):
    return s.astype("string").str.strip()

# Building names and official room counts
building_frames = []

if "table_7" in tables:
    b = tables["table_7"].copy()
    bld = pd.DataFrame({
        "building_component": _key(b["FAC_BUILDING_KEY"]),
        "building_name": b.get("BUILDING_NAME", pd.Series(index=b.index, dtype="object")),
        "building_name_long": b.get("BUILDING_NAME_LONG", pd.Series(index=b.index, dtype="object")),
        "official_num_rooms": b.get("NUM_OF_ROOMS", pd.Series(index=b.index, dtype="float64")),
    })
    bld["building_name"] = bld["building_name"].combine_first(bld["building_name_long"])
    building_frames.append(bld[["building_component", "building_name", "official_num_rooms"]])

if "table_6" in tables:
    b = tables["table_6"].copy()
    bld = pd.DataFrame({
        "building_component": _key(b["BUILDING_KEY"]),
        "building_name": b.get("BUILDING_NAME", pd.Series(index=b.index, dtype="object")),
        "official_num_rooms": pd.NA,
    })
    building_frames.append(bld)

buildings = (
    pd.concat(building_frames, ignore_index=True)
    .dropna(subset=["building_component"])
    .sort_values(["building_component", "building_name"])
    .drop_duplicates("building_component", keep="first")
)

# Room square footage and room counts by building component
rooms = tables["table_3"].copy()
rooms["building_component"] = _key(
    rooms["BUILDING_COMPONENT"].combine_first(rooms["BUILDING_KEY"])
)

rooms_unique = rooms.drop_duplicates(["building_component", "BUILDING_ROOM"])

room_agg = (
    rooms_unique.groupby("building_component", as_index=False)
    .agg(
        square_footage_for_all_rooms=("ROOM_SQUARE_FOOTAGE", "sum"),
        room_count_from_rooms=("BUILDING_ROOM", "nunique"),
        floor_count_from_rooms=("FLOOR_KEY", "nunique"),
    )
)

# Floor counts from floor table
floors = tables["table_10"].copy()
floors["building_component"] = _key(floors["BUILDING_KEY"])

floor_agg = (
    floors.drop_duplicates(["building_component", "FLOOR_KEY"])
    .groupby("building_component", as_index=False)
    .agg(total_number_of_floors=("FLOOR_KEY", "nunique"))
)

# Facility organization counts
fac_rooms = tables["table_4"].copy()
fac_rooms["building_component"] = _key(fac_rooms["BUILDING_KEY"])
fac_rooms["facility_org_id"] = fac_rooms["ORGANIZATION_KEY"].where(
    fac_rooms["ORGANIZATION_KEY"].notna(),
    fac_rooms["ORGANIZATION_NAME"]
)

org_agg = (
    fac_rooms.groupby("building_component", as_index=False)
    .agg(total_number_of_facility_organizations=("facility_org_id", "nunique"))
)

# Supervisors/supervisees by matching supervisor department names to facility organization names
org_map = fac_rooms[["building_component", "ORGANIZATION_NAME"]].dropna().drop_duplicates()
org_map["org_norm"] = (
    org_map["ORGANIZATION_NAME"]
    .astype(str)
    .str.upper()
    .str.replace(r"[^A-Z0-9]+", "", regex=True)
)

sup = tables["table_2"].copy()
sup["dept_token"] = (
    sup["dept_names"]
    .fillna("")
    .astype(str)
    .str.split(r"\s*[,;/|]\s*", regex=True)
)
sup = sup.explode("dept_token")
sup["dept_norm"] = (
    sup["dept_token"]
    .astype(str)
    .str.upper()
    .str.replace(r"^D_", "", regex=True)
    .str.replace(r"[^A-Z0-9]+", "", regex=True)
)
sup = sup[sup["dept_norm"].ne("")]

sup_org = org_map.merge(
    sup[["MIT_ID", "NUM_OF_SUPERVISEES", "dept_norm"]],
    left_on="org_norm",
    right_on="dept_norm",
    how="inner",
)

sup_org = sup_org.drop_duplicates(["building_component", "MIT_ID"])

sup_agg = (
    sup_org.groupby("building_component", as_index=False)
    .agg(
        total_number_of_supervisors=("MIT_ID", "nunique"),
        total_number_of_supervisees=("NUM_OF_SUPERVISEES", "sum"),
    )
)

# Assemble final answer
base_components = pd.DataFrame({
    "building_component": pd.concat([
        buildings["building_component"],
        room_agg["building_component"],
        floor_agg["building_component"],
        org_agg["building_component"],
        sup_agg["building_component"],
    ], ignore_index=True).dropna().drop_duplicates()
})

out = (
    base_components
    .merge(buildings, on="building_component", how="left")
    .merge(room_agg, on="building_component", how="left")
    .merge(floor_agg, on="building_component", how="left")
    .merge(org_agg, on="building_component", how="left")
    .merge(sup_agg, on="building_component", how="left")
)

out["total_number_of_floors"] = out["total_number_of_floors"].combine_first(
    out["floor_count_from_rooms"]
)
out["total_number_of_rooms"] = out["official_num_rooms"].combine_first(
    out["room_count_from_rooms"]
)

out["square_footage_for_all_rooms"] = out["square_footage_for_all_rooms"].fillna(0)

for col in [
    "total_number_of_floors",
    "total_number_of_rooms",
    "total_number_of_facility_organizations",
    "total_number_of_supervisors",
    "total_number_of_supervisees",
]:
    out[col] = out[col].fillna(0).astype("int64")

out = out[
    [
        "building_component",
        "building_name",
        "square_footage_for_all_rooms",
        "total_number_of_floors",
        "total_number_of_rooms",
        "total_number_of_facility_organizations",
        "total_number_of_supervisors",
        "total_number_of_supervisees",
    ]
].sort_values("building_component").reset_index(drop=True)

result = {"building_component_summary": out}
