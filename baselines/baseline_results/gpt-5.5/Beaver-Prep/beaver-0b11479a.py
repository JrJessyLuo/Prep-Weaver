import pandas as pd

buildings = tables["table_4"].copy()
employees = tables["table_6"].copy()

# Extract building number from employee office locations, e.g. "7-390" -> "7", "W20-505E" -> "W20"
employees["BUILDING_NUMBER"] = (
    employees["OFFICE_LOCATION"]
    .astype("string")
    .str.strip()
    .str.upper()
    .str.extract(r"^([A-Z]*\d+[A-Z]*)", expand=False)
)

employee_counts = (
    employees.dropna(subset=["BUILDING_NUMBER"])
    .groupby("BUILDING_NUMBER", as_index=False)["MIT_ID"]
    .nunique()
    .rename(columns={"MIT_ID": "number_of_employees"})
)

buildings["built_date"] = pd.to_datetime(buildings["DATE_BUILT"], errors="coerce")
buildings["built_year"] = buildings["built_date"].dt.year

answer = (
    buildings[buildings["built_year"] < 1950]
    .merge(employee_counts, on="BUILDING_NUMBER", how="inner")
    .query("number_of_employees > 100")
    [["BUILDING_NAME_LONG", "built_year", "number_of_employees"]]
    .rename(columns={
        "BUILDING_NAME_LONG": "long_name",
        "built_year": "built_year",
        "number_of_employees": "number_of_employees"
    })
    .sort_values(["built_year", "long_name"])
    .reset_index(drop=True)
)

result = {"buildings_before_1950_with_over_100_employees": answer}
