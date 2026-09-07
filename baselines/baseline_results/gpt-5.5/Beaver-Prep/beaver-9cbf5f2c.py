import pandas as pd

buildings = tables["table_4"].copy()
floors = tables["table_8"].copy()
rooms = tables["table_10"].copy()
hr = tables["table_9"].copy()

# Standardize join keys
buildings["BUILDING_KEY"] = buildings["FCLT_BUILDING_KEY"].astype(str).str.strip()
floors["BUILDING_KEY"] = floors["FCLT_BUILDING_KEY"].astype(str).str.strip()
rooms["BUILDING_KEY"] = rooms["BUILDING_COMPONENT"].astype(str).str.strip()

rooms["HR_ORG_UNIT_ID_JOIN"] = pd.to_numeric(rooms["HR_ORG_UNIT_ID"], errors="coerce").astype("Int64")
hr["HR_ORG_UNIT_ID_JOIN"] = pd.to_numeric(hr["HR_ORG_UNIT_ID"], errors="coerce").astype("Int64")

# HR departments occupying each building
room_hr = rooms.dropna(subset=["HR_ORG_UNIT_ID_JOIN"]).merge(
    hr[["HR_ORG_UNIT_ID_JOIN", "HR_DEPARTMENT_NAME"]],
    on="HR_ORG_UNIT_ID_JOIN",
    how="inner"
)

dept_by_building = (
    room_hr.dropna(subset=["HR_DEPARTMENT_NAME"])
    .drop_duplicates(["BUILDING_KEY", "HR_DEPARTMENT_NAME"])
    .groupby("BUILDING_KEY", as_index=False)
    .agg(
        HR_DEPARTMENT_NAMES=(
            "HR_DEPARTMENT_NAME",
            lambda s: "; ".join(sorted(s.astype(str).unique()))
        )
    )
)

# Building square footage summarized from floor records
area_by_building = (
    floors.groupby("BUILDING_KEY", as_index=False)
    .agg(
        TOTAL_GROSS_SQUARE_FOOTAGE=("EXT_GROSS_AREA", "sum"),
        TOTAL_ASSIGNABLE_SQUARE_FOOTAGE=("ASSIGNABLE_AREA", "sum"),
        AVERAGE_ASSIGNABLE_SQUARE_FOOTAGE=("ASSIGNABLE_AREA", "mean")
    )
)

# Building names and built year
building_info = buildings[["BUILDING_KEY", "BUILDING_NAME", "DATE_BUILT"]].drop_duplicates("BUILDING_KEY")
building_info["BUILT_YEAR"] = pd.to_datetime(
    building_info["DATE_BUILT"],
    errors="coerce"
).dt.year.astype("Int64")

# Final result: one row per building key with HR departments occupying it
out = (
    dept_by_building
    .merge(building_info[["BUILDING_KEY", "BUILDING_NAME", "BUILT_YEAR"]], on="BUILDING_KEY", how="left")
    .merge(area_by_building, on="BUILDING_KEY", how="left")
)

out = out[
    [
        "BUILDING_KEY",
        "BUILDING_NAME",
        "HR_DEPARTMENT_NAMES",
        "TOTAL_GROSS_SQUARE_FOOTAGE",
        "TOTAL_ASSIGNABLE_SQUARE_FOOTAGE",
        "AVERAGE_ASSIGNABLE_SQUARE_FOOTAGE",
        "BUILT_YEAR"
    ]
].sort_values("BUILDING_KEY").reset_index(drop=True)

result = {
    "building_hr_department_square_footage": out
}
