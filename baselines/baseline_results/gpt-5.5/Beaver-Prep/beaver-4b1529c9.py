import pandas as pd
import numpy as np

buildings = tables["table_4"].copy()
addresses = tables["table_1"].copy()
orgs = tables["table_8"].copy()
floors = tables["table_7"].copy()

# Aggregate floor square footage by building for total and average square footage
floor_agg = (
    floors.groupby("FCLT_BUILDING_KEY", as_index=False)
    .agg(
        floor_assignable_square_footage=("ASSIGNABLE_AREA", "sum"),
        total_square_footage=("EXT_GROSS_AREA", "sum"),
        average_square_footage=("EXT_GROSS_AREA", "mean"),
    )
)

# Prepare address data
addr = addresses[
    [
        "BUILDING_NUMBER",
        "BUILDING_NAME",
        "BUILDING_STREET_ADDRESS",
        "BLDG_GROSS_SQUARE_FOOTAGE",
        "BLDG_ASSIGNABLE_SQUARE_FOOTAGE",
    ]
].copy()

addr = addr.rename(
    columns={
        "BUILDING_NAME": "address_building_name",
        "BUILDING_STREET_ADDRESS": "street_address_raw",
        "BLDG_GROSS_SQUARE_FOOTAGE": "address_gross_square_footage",
        "BLDG_ASSIGNABLE_SQUARE_FOOTAGE": "address_assignable_square_footage",
    }
)

# Parse possible city/state from street address if embedded; otherwise default to Cambridge, MA
addr["street_address"] = addr["street_address_raw"].astype("string").str.strip()

parts = addr["street_address"].str.split(",", expand=True)
if parts.shape[1] >= 3:
    addr["street_address"] = parts[0].astype("string").str.strip()
    addr["city"] = parts[1].astype("string").str.strip()
    addr["state"] = parts[2].astype("string").str.extract(r"([A-Za-z]{2})", expand=False).str.upper()
elif parts.shape[1] == 2:
    addr["street_address"] = parts[0].astype("string").str.strip()
    city_state = parts[1].astype("string").str.strip()
    addr["city"] = city_state.str.replace(r"\s+[A-Za-z]{2}(\s+\d{5})?$", "", regex=True).str.strip()
    addr["state"] = city_state.str.extract(r"\b([A-Za-z]{2})\b", expand=False).str.upper()
else:
    addr["city"] = pd.NA
    addr["state"] = pd.NA

addr["city"] = addr["city"].fillna("Cambridge")
addr["state"] = addr["state"].fillna("MA")

addr = addr.drop_duplicates(subset=["BUILDING_NUMBER"])

# Prepare organization / HR department data
org_lookup = (
    orgs[["ORGANIZATION_NUMBER", "HR_DEPARTMENT_NAME"]]
    .dropna(subset=["ORGANIZATION_NUMBER"])
    .drop_duplicates(subset=["ORGANIZATION_NUMBER"])
)

# Join buildings to address, floor aggregates, and HR department
df = buildings.merge(addr, on="BUILDING_NUMBER", how="left")

df = df.merge(
    floor_agg,
    left_on="FCLT_BUILDING_KEY",
    right_on="FCLT_BUILDING_KEY",
    how="left",
)

df = df.merge(
    org_lookup,
    left_on="COST_CENTER_CODE",
    right_on="ORGANIZATION_NUMBER",
    how="left",
)

# Choose best available square footage values
df["assignable_square_footage"] = (
    df["ASSIGNABLE_AREA"]
    .combine_first(df["address_assignable_square_footage"])
    .combine_first(df["floor_assignable_square_footage"])
)

df["total_square_footage"] = (
    df["total_square_footage"]
    .combine_first(df["EXT_GROSS_AREA"])
    .combine_first(df["address_gross_square_footage"])
)

df["average_square_footage"] = df["average_square_footage"].combine_first(df["total_square_footage"])

df["building_name"] = (
    df["BUILDING_NAME_LONG"]
    .combine_first(df["BUILDING_NAME"])
    .combine_first(df["address_building_name"])
)

out = df[
    [
        "building_name",
        "BUILDING_NUMBER",
        "BUILDING_HEIGHT",
        "street_address",
        "city",
        "state",
        "HR_DEPARTMENT_NAME",
        "assignable_square_footage",
        "total_square_footage",
        "average_square_footage",
    ]
].copy()

out = out.rename(
    columns={
        "BUILDING_NUMBER": "building_number",
        "BUILDING_HEIGHT": "building_height",
        "HR_DEPARTMENT_NAME": "hr_department_name",
    }
)

out = out.sort_values(
    by=["assignable_square_footage", "total_square_footage", "average_square_footage"],
    ascending=[False, False, False],
    na_position="last",
).reset_index(drop=True)

result = {"buildings_square_footage": out}
