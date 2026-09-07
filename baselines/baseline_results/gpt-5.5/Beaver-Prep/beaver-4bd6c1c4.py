import pandas as pd

floors = tables["table_4"].copy()
buildings = tables["table_8"].copy()

floor_counts = (
    floors.dropna(subset=["FCLT_BUILDING_KEY", "FCLT_FLOOR_KEY"])
    .groupby("FCLT_BUILDING_KEY", as_index=False)
    .agg(num_floors=("FCLT_FLOOR_KEY", "nunique"))
)

max_floors = floor_counts["num_floors"].max()
top_buildings = floor_counts[floor_counts["num_floors"] == max_floors]

answer = (
    top_buildings.merge(
        buildings,
        left_on="FCLT_BUILDING_KEY",
        right_on="FAC_BUILDING_KEY",
        how="left"
    )
    .assign(building_name=lambda df: df["BUILDING_NAME_LONG"].fillna(df["BUILDING_NAME"]))
    [["building_name"]]
    .drop_duplicates()
    .sort_values("building_name")
    .reset_index(drop=True)
)

result = {"buildings_with_most_floors": answer}
