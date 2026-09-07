import pandas as pd

buildings = tables["table_4"].copy()
addresses = tables["table_8"].copy()

address_counts = (
    addresses.groupby("FCLT_BUILDING_KEY", as_index=False)
    .agg(address_count=("FCLT_BUILDING_ADDRESS_KEY", "nunique"))
)

result_df = (
    buildings.merge(address_counts, on="FCLT_BUILDING_KEY", how="left")
    .assign(address_count=lambda df: df["address_count"].fillna(0).astype(int))
    .groupby(
        ["BUILDING_NAME", "BUILDING_NUMBER", "DATE_BUILT", "BUILDING_TYPE"],
        dropna=False,
        as_index=False
    )
    .agg(
        address_count=("address_count", "first"),
        average_gross_area=("EXT_GROSS_AREA", "mean"),
        total_number_of_rooms=("NUM_OF_ROOMS", "sum")
    )
    .rename(columns={
        "BUILDING_NAME": "building_name",
        "BUILDING_NUMBER": "building_number",
        "DATE_BUILT": "construction_date",
        "BUILDING_TYPE": "building_type"
    })
    .sort_values("building_name", kind="mergesort")
    .reset_index(drop=True)
)

result = {
    "buildings_with_address_counts_area_and_rooms": result_df
}
