import pandas as pd
import numpy as np

buildings = tables["table_2"].copy()
addresses = tables["table_9"].copy()
building_addr_fallback = tables["table_5"].copy()

def is_null_like(s):
    return (
        s.isna()
        | s.astype(str).str.strip().str.upper().isin(["", "NULL", "(NULL)", "NAN"])
    )

# Current MIT buildings that are not subdivisions
filtered = buildings[
    is_null_like(buildings["PARENT_BUILDING_NUMBER"])
    & buildings["SITE"].astype(str).str.strip().str.upper().eq("MIT")
].copy()

# Build street address from address component table
street_addresses = addresses[
    addresses["ADDRESS_PURPOSE"].astype(str).str.strip().str.upper().eq("STREET")
].copy()

def clean_part(x):
    if pd.isna(x):
        return None
    x = str(x).strip()
    if x.upper() in ["", "NULL", "(NULL)", "NAN"]:
        return None
    return x

address_parts = [
    "STREET_NUMBER",
    "STREET_NUMBER_SUFFIX",
    "PRE_DIRECTIONAL",
    "STREET_NAME",
    "STREET_SUFFIX",
    "POST_DIRECTIONAL",
]

street_addresses["STREET_ADDRESS_FROM_COMPONENTS"] = street_addresses[address_parts].apply(
    lambda r: " ".join([p for p in (clean_part(v) for v in r) if p]),
    axis=1
)

street_addresses = (
    street_addresses[["FCLT_BUILDING_KEY", "STREET_ADDRESS_FROM_COMPONENTS"]]
    .drop_duplicates(subset=["FCLT_BUILDING_KEY"])
)

# Fallback street address table
fallback_addresses = (
    building_addr_fallback[["BUILDING_NUMBER", "BUILDING_STREET_ADDRESS"]]
    .drop_duplicates(subset=["BUILDING_NUMBER"])
)

detail = (
    filtered
    .merge(street_addresses, on="FCLT_BUILDING_KEY", how="left")
    .merge(fallback_addresses, on="BUILDING_NUMBER", how="left")
)

detail["STREET_ADDRESS"] = detail["STREET_ADDRESS_FROM_COMPONENTS"].combine_first(
    detail["BUILDING_STREET_ADDRESS"]
)

detail["FULL_NAME"] = detail["BUILDING_NAME_LONG"].combine_first(detail["BUILDING_NAME"])

detail = detail.sort_values(
    by=["BUILDING_SORT", "BUILDING_NUMBER"],
    na_position="last"
)

final_cols = [
    "BUILDING_NUMBER",
    "FULL_NAME",
    "STREET_ADDRESS",
    "BUILDING_TYPE",
    "OCCUPANCY_DATE",
    "OWNERSHIP_TYPE",
    "SITE_LOCATION",
]

detail_out = detail.rename(
    columns={
        "DATE_OCCUPIED": "OCCUPANCY_DATE",
        "SITE": "SITE_LOCATION",
    }
)[final_cols]

ownership = filtered["OWNERSHIP_TYPE"].astype(str).str.strip().str.upper()
owned_count = int((ownership == "OWNED").sum())
leased_count = int((ownership == "LEASED").sum())
all_count = int(len(filtered))

summary = pd.DataFrame(
    [
        [None, f"{owned_count} Owned Buildings", None, None, None, None, None],
        [None, f"{leased_count} Leased Buildings", None, None, None, None, None],
        [None, f"{all_count} Buildings", None, None, None, None, None],
    ],
    columns=final_cols,
)

answer = pd.concat([detail_out, summary], ignore_index=True)

result = {
    "mit_non_subdivision_buildings": answer
}
