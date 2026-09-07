import pandas as pd
import numpy as np

rooms = tables["table_1"].copy()

# Department of Facilities rooms
org = rooms["ORGANIZATION_NAME"].astype("string").str.strip().str.upper()
dof_rooms = rooms[
    org.eq("DOF")
    | org.str.contains("DEPARTMENT OF FACILITIES", na=False)
    | org.str.contains(r"\bFACILITIES\b", na=False)
].copy()

dof_rooms["AREA"] = pd.to_numeric(dof_rooms["AREA"], errors="coerce").fillna(0)
dof_rooms["ACCESS_LEVEL"] = pd.to_numeric(dof_rooms["ACCESS_LEVEL"], errors="coerce")

room_key_col = "fac_room_key" if "fac_room_key" in dof_rooms.columns else "ROOM"

detail = (
    dof_rooms.groupby(["BUILDING_KEY", "FLOOR_KEY"], dropna=False)
    .agg(
        number_of_rooms=(room_key_col, "nunique"),
        total_area=("AREA", "sum"),
        room_access_level=("ACCESS_LEVEL", "max"),
    )
    .reset_index()
)

detail["floor_count"] = 1
detail["average_area_per_floor"] = detail["total_area"]

# Building metadata
bldg = tables["table_3"].copy()
bldg_meta = pd.DataFrame()
bldg_meta["BUILDING_KEY"] = bldg["FAC_BUILDING_KEY"].astype(str)

if "BUILDING_NAME" in bldg.columns and "BUILDING_NAME_LONG" in bldg.columns:
    bldg_meta["building_name"] = bldg["BUILDING_NAME"].combine_first(bldg["BUILDING_NAME_LONG"])
elif "BUILDING_NAME" in bldg.columns:
    bldg_meta["building_name"] = bldg["BUILDING_NAME"]
elif "BUILDING_NAME_LONG" in bldg.columns:
    bldg_meta["building_name"] = bldg["BUILDING_NAME_LONG"]
else:
    bldg_meta["building_name"] = pd.NA

if "ACCESS_LEVEL_CODE" in bldg.columns:
    bldg_meta["building_access_level"] = bldg["ACCESS_LEVEL_CODE"]
elif "ACCESS_LEVEL_NAME" in bldg.columns:
    bldg_meta["building_access_level"] = bldg["ACCESS_LEVEL_NAME"]
else:
    bldg_meta["building_access_level"] = pd.NA

bldg_meta["building_sort"] = bldg["BUILDING_SORT"] if "BUILDING_SORT" in bldg.columns else bldg_meta["BUILDING_KEY"]
bldg_meta = bldg_meta.drop_duplicates("BUILDING_KEY")

# Address / zip / city metadata, if present
addr = tables["table_10"].copy()

def find_col(df, keywords):
    for col in df.columns:
        u = col.upper()
        if any(k in u for k in keywords):
            return col
    return None

zip_col = find_col(addr, ["ZIP", "POSTAL"])
city_col = find_col(addr, ["CITY"])

addr_meta = pd.DataFrame({"BUILDING_KEY": addr["BUILDING_KEY"].astype(str)})
addr_meta["building_name_addr"] = addr["BUILDING_NAME"] if "BUILDING_NAME" in addr.columns else pd.NA
addr_meta["zip_code"] = addr[zip_col] if zip_col else pd.NA
addr_meta["city"] = addr[city_col] if city_col else pd.NA
addr_meta = addr_meta.drop_duplicates("BUILDING_KEY")

# Floor sort metadata
floors = tables["table_2"].copy()
floor_sort = floors[["BUILDING_KEY", "FLOOR_KEY", "FLOOR_SORT_SEQUENCE"]].drop_duplicates(
    ["BUILDING_KEY", "FLOOR_KEY"]
)

detail["BUILDING_KEY"] = detail["BUILDING_KEY"].astype(str)
detail["FLOOR_KEY"] = detail["FLOOR_KEY"].astype(str)

detail = (
    detail.merge(bldg_meta, on="BUILDING_KEY", how="left")
    .merge(addr_meta, on="BUILDING_KEY", how="left")
    .merge(floor_sort, on=["BUILDING_KEY", "FLOOR_KEY"], how="left")
)

detail["building_name"] = detail["building_name"].combine_first(detail["building_name_addr"])
detail["access_level"] = detail["building_access_level"].combine_first(detail["room_access_level"])
detail["row_type"] = "Detail"
detail["row_order"] = 0

def first_non_null(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else pd.NA

# Building subtotals
subtotals = (
    detail.groupby("BUILDING_KEY", dropna=False)
    .agg(
        number_of_rooms=("number_of_rooms", "sum"),
        total_area=("total_area", "sum"),
        floor_count=("FLOOR_KEY", "size"),
        building_name=("building_name", first_non_null),
        access_level=("access_level", first_non_null),
        building_sort=("building_sort", first_non_null),
    )
    .reset_index()
)

subtotals["FLOOR_KEY"] = "Subtotal"
subtotals["average_area_per_floor"] = subtotals["total_area"] / subtotals["floor_count"].replace(0, np.nan)
subtotals["zip_code"] = pd.NA
subtotals["city"] = pd.NA
subtotals["FLOOR_SORT_SEQUENCE"] = np.inf
subtotals["row_type"] = "Subtotal"
subtotals["row_order"] = 1

# Grand total
grand_total = pd.DataFrame(
    {
        "BUILDING_KEY": ["Grand Total"],
        "FLOOR_KEY": [""],
        "number_of_rooms": [detail["number_of_rooms"].sum()],
        "total_area": [detail["total_area"].sum()],
        "floor_count": [len(detail)],
        "average_area_per_floor": [
            detail["total_area"].sum() / len(detail) if len(detail) else np.nan
        ],
        "building_name": [pd.NA],
        "access_level": [pd.NA],
        "zip_code": [pd.NA],
        "city": [pd.NA],
        "building_sort": ["ZZZZZZZZ"],
        "FLOOR_SORT_SEQUENCE": [np.inf],
        "row_type": ["Grand Total"],
        "row_order": [2],
    }
)

combined = pd.concat([detail, subtotals, grand_total], ignore_index=True, sort=False)

combined["building_sort"] = combined["building_sort"].fillna(combined["BUILDING_KEY"]).astype(str)
combined["FLOOR_SORT_SEQUENCE"] = pd.to_numeric(combined["FLOOR_SORT_SEQUENCE"], errors="coerce").fillna(np.inf)

combined = combined.sort_values(
    ["row_order", "building_sort", "BUILDING_KEY", "FLOOR_SORT_SEQUENCE", "FLOOR_KEY"],
    kind="stable",
)

# Put grand total last after building detail/subtotal rows
combined["_grand_flag"] = combined["row_type"].eq("Grand Total").astype(int)
combined = combined.sort_values(
    ["_grand_flag", "building_sort", "BUILDING_KEY", "row_order", "FLOOR_SORT_SEQUENCE", "FLOOR_KEY"],
    kind="stable",
)

out = combined[
    [
        "BUILDING_KEY",
        "FLOOR_KEY",
        "number_of_rooms",
        "total_area",
        "average_area_per_floor",
        "building_name",
        "access_level",
        "zip_code",
        "city",
    ]
].rename(
    columns={
        "BUILDING_KEY": "Building Key",
        "FLOOR_KEY": "Floor Key",
        "number_of_rooms": "Number of Rooms",
        "total_area": "Total Area",
        "average_area_per_floor": "Average Area per Floor",
        "building_name": "Building Name",
        "access_level": "Access Level",
        "zip_code": "Zip Code",
        "city": "City",
    }
)

def fmt_int_commas(x):
    if pd.isna(x):
        return ""
    return f"{int(round(float(x))):,}"

def fmt_access(x):
    if pd.isna(x):
        return ""
    try:
        fx = float(x)
        return str(int(fx)) if fx.is_integer() else str(x)
    except Exception:
        return str(x)

for col in ["Number of Rooms", "Total Area", "Average Area per Floor"]:
    out[col] = out[col].apply(fmt_int_commas)

out["Access Level"] = out["Access Level"].apply(fmt_access)
out["Building Name"] = out["Building Name"].fillna("")
out["Zip Code"] = out["Zip Code"].fillna("")
out["City"] = out["City"].fillna("")
out["Floor Key"] = out["Floor Key"].replace("<NA>", "").fillna("")

result = {"facilities_building_floor_area_with_totals": out.reset_index(drop=True)}
