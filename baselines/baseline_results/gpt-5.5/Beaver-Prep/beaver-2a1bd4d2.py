import pandas as pd
import numpy as np

buildings = tables["table_6"].copy()
addresses = tables["table_5"].copy()
rooms = tables["table_9"].copy()
employees = tables["table_10"].copy()

def clean_str(s):
    return s.astype("string").str.strip()

# -----------------------------
# Prepare building dimension
# -----------------------------
buildings["BUILDING_ID"] = clean_str(buildings["FCLT_BUILDING_KEY"])
buildings["BUILDING_NUMBER_NORM"] = clean_str(buildings["BUILDING_NUMBER"]).str.upper()

bt = clean_str(buildings["BUILDING_TYPE"]).str.upper()
buildings["BUILDING_TYPE_NAME"] = np.where(bt.eq("RESIDENT"), "RESIDENTIAL", bt)

parent = clean_str(buildings["PARENT_BUILDING_NUMBER"])
buildings["IS_NOT_SUBDIVISION"] = parent.isna() | parent.eq("") | parent.str.upper().eq("(NULL)")

buildings["GROSS_SQUARE_FOOTAGE"] = pd.to_numeric(buildings["EXT_GROSS_AREA"], errors="coerce")

bldg_dim = buildings[
    [
        "BUILDING_ID",
        "BUILDING_NUMBER_NORM",
        "BUILDING_TYPE_NAME",
        "IS_NOT_SUBDIVISION",
        "GROSS_SQUARE_FOOTAGE",
    ]
].drop_duplicates(subset=["BUILDING_ID"])

all_types = pd.Index(sorted(bldg_dim["BUILDING_TYPE_NAME"].dropna().unique()), name="BUILDING_TYPE_NAME")

building_counts = (
    bldg_dim[bldg_dim["IS_NOT_SUBDIVISION"]]
    .groupby("BUILDING_TYPE_NAME")["BUILDING_ID"]
    .nunique()
    .reindex(all_types, fill_value=0)
    .rename("NUMBER_OF_BUILDINGS_NOT_SUBDIVISIONS")
)

gross_sqft = (
    bldg_dim.groupby("BUILDING_TYPE_NAME")["GROSS_SQUARE_FOOTAGE"]
    .sum()
    .reindex(all_types, fill_value=0)
    .rename("TOTAL_GROSS_SQUARE_FOOTAGE")
)

# -----------------------------
# Prepare employee-to-building mapping
# -----------------------------
rooms_map = rooms[["BUILDING_ROOM", "BUILDING_COMPONENT"]].copy()
rooms_map["OFFICE_LOCATION_NORM"] = clean_str(rooms_map["BUILDING_ROOM"]).str.upper()
rooms_map["ROOM_BUILDING_NUMBER_NORM"] = clean_str(rooms_map["BUILDING_COMPONENT"]).str.upper()
rooms_map = rooms_map.dropna(subset=["OFFICE_LOCATION_NORM"]).drop_duplicates(
    subset=["OFFICE_LOCATION_NORM"]
)[["OFFICE_LOCATION_NORM", "ROOM_BUILDING_NUMBER_NORM"]]

emp = employees[["MIT_ID", "OFFICE_LOCATION"]].copy()
emp["OFFICE_LOCATION_NORM"] = clean_str(emp["OFFICE_LOCATION"]).str.upper()
emp["PARSED_BUILDING_NUMBER_NORM"] = emp["OFFICE_LOCATION_NORM"].str.extract(r"^([^-]+)", expand=False)

emp = emp.merge(rooms_map, on="OFFICE_LOCATION_NORM", how="left")
emp["BUILDING_NUMBER_NORM"] = emp["ROOM_BUILDING_NUMBER_NORM"].fillna(
    emp["PARSED_BUILDING_NUMBER_NORM"]
)

emp_joined = emp.merge(
    bldg_dim[["BUILDING_NUMBER_NORM", "BUILDING_TYPE_NAME"]].drop_duplicates(),
    on="BUILDING_NUMBER_NORM",
    how="inner",
)

employee_counts = (
    emp_joined.groupby("BUILDING_TYPE_NAME")["MIT_ID"]
    .nunique()
    .reindex(all_types, fill_value=0)
    .rename("NUMBER_OF_EMPLOYEES")
)

# -----------------------------
# Prepare building street addresses
# -----------------------------
addr = addresses.copy()
addr["ADDRESS_PURPOSE_NORM"] = clean_str(addr["ADDRESS_PURPOSE"]).str.upper()
addr = addr[addr["ADDRESS_PURPOSE_NORM"].eq("STREET")].copy()

addr["BUILDING_NUMBER_NORM"] = clean_str(addr["BUILDING_NUMBER"]).str.upper()

address_parts = [
    "STREET_NUMBER",
    "STREET_NUMBER_SUFFIX",
    "PRE_DIRECTIONAL",
    "STREET_NAME",
    "STREET_SUFFIX",
    "POST_DIRECTIONAL",
]

for col in address_parts:
    addr[col] = clean_str(addr[col])
    addr[col] = addr[col].mask(
        addr[col].isna() | addr[col].eq("") | addr[col].str.upper().isin(["NAN", "NONE", "<NA>"])
    )

addr["BUILDING_STREET_ADDRESS"] = addr[address_parts].apply(
    lambda r: " ".join([str(x) for x in r if pd.notna(x) and str(x).strip() != ""]),
    axis=1,
)
addr["BUILDING_STREET_ADDRESS"] = addr["BUILDING_STREET_ADDRESS"].replace("", pd.NA)

addr["CITY"] = clean_str(addr["CITY"]).str.upper()
addr["STATE"] = clean_str(addr["STATE"]).str.upper()
addr["POSTAL_CODE"] = addr["POSTAL_CODE"].astype("string").str.strip()

addr_joined = addr.merge(
    bldg_dim[["BUILDING_NUMBER_NORM", "BUILDING_TYPE_NAME"]].drop_duplicates(),
    on="BUILDING_NUMBER_NORM",
    how="inner",
)

address_counts = (
    addr_joined.groupby("BUILDING_TYPE_NAME")
    .agg(
        NUMBER_OF_UNIQUE_BUILDING_STREET_ADDRESS=("BUILDING_STREET_ADDRESS", "nunique"),
        NUMBER_OF_UNIQUE_CITY=("CITY", "nunique"),
        NUMBER_OF_UNIQUE_STATE=("STATE", "nunique"),
        NUMBER_OF_UNIQUE_POSTAL_CODE=("POSTAL_CODE", "nunique"),
    )
    .reindex(all_types, fill_value=0)
)

# -----------------------------
# Combine per-building-type result
# -----------------------------
summary = pd.concat(
    [building_counts, employee_counts, address_counts, gross_sqft],
    axis=1,
).reset_index()

summary["AVERAGE_GROSS_SQUARE_FOOTAGE_PER_EMPLOYEE"] = np.where(
    summary["NUMBER_OF_EMPLOYEES"] > 0,
    summary["TOTAL_GROSS_SQUARE_FOOTAGE"] / summary["NUMBER_OF_EMPLOYEES"],
    np.nan,
)

summary = summary.drop(columns=["TOTAL_GROSS_SQUARE_FOOTAGE"]).rename(
    columns={"BUILDING_TYPE_NAME": "BUILDING_TYPE"}
)

# -----------------------------
# Grand total row
# -----------------------------
total_employees = emp_joined["MIT_ID"].nunique()
total_gross_sqft = bldg_dim["GROSS_SQUARE_FOOTAGE"].sum(skipna=True)

total_row = pd.DataFrame(
    [
        {
            "BUILDING_TYPE": "TOTAL",
            "NUMBER_OF_BUILDINGS_NOT_SUBDIVISIONS": bldg_dim.loc[
                bldg_dim["IS_NOT_SUBDIVISION"], "BUILDING_ID"
            ].nunique(),
            "NUMBER_OF_EMPLOYEES": total_employees,
            "NUMBER_OF_UNIQUE_BUILDING_STREET_ADDRESS": addr_joined[
                "BUILDING_STREET_ADDRESS"
            ].nunique(dropna=True),
            "NUMBER_OF_UNIQUE_CITY": addr_joined["CITY"].nunique(dropna=True),
            "NUMBER_OF_UNIQUE_STATE": addr_joined["STATE"].nunique(dropna=True),
            "NUMBER_OF_UNIQUE_POSTAL_CODE": addr_joined["POSTAL_CODE"].nunique(dropna=True),
            "AVERAGE_GROSS_SQUARE_FOOTAGE_PER_EMPLOYEE": (
                total_gross_sqft / total_employees if total_employees > 0 else np.nan
            ),
        }
    ]
)

final = pd.concat([summary, total_row], ignore_index=True)

final = final[
    [
        "BUILDING_TYPE",
        "NUMBER_OF_BUILDINGS_NOT_SUBDIVISIONS",
        "NUMBER_OF_EMPLOYEES",
        "NUMBER_OF_UNIQUE_BUILDING_STREET_ADDRESS",
        "NUMBER_OF_UNIQUE_CITY",
        "NUMBER_OF_UNIQUE_STATE",
        "NUMBER_OF_UNIQUE_POSTAL_CODE",
        "AVERAGE_GROSS_SQUARE_FOOTAGE_PER_EMPLOYEE",
    ]
]

result = {"building_type_summary": final}
