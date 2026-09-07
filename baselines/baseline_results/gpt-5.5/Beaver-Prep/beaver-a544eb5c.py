import pandas as pd

buildings = tables["table_3"].copy()
floors = tables["table_4"].copy()

floor_totals = (
    floors.groupby("FCLT_BUILDING_KEY", as_index=False)
    .agg(
        total_assignable_area=("ASSIGNABLE_AREA", "sum"),
        total_non_assignable_area=("NON_ASSIGNABLE_AREA", "sum"),
    )
)

result_df = (
    buildings[
        [
            "FCLT_BUILDING_KEY",
            "BUILDING_NAME",
            "BUILDING_NUMBER",
            "NUM_OF_ROOMS",
        ]
    ]
    .merge(floor_totals, on="FCLT_BUILDING_KEY", how="left")
    .fillna(
        {
            "total_assignable_area": 0,
            "total_non_assignable_area": 0,
        }
    )
    .rename(
        columns={
            "BUILDING_NAME": "building_name",
            "BUILDING_NUMBER": "building_number",
            "NUM_OF_ROOMS": "total_room_count",
        }
    )
    [
        [
            "building_name",
            "building_number",
            "total_assignable_area",
            "total_non_assignable_area",
            "total_room_count",
        ]
    ]
    .sort_values("total_assignable_area", ascending=False)
    .reset_index(drop=True)
)

result = {"building_area_summary": result_df}
