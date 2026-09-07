import pandas as pd

floors = tables["table_1"].copy()
buildings = tables["table_10"].copy()

floors["floor_number"] = pd.to_numeric(floors["FLOOR"], errors="coerce")
floors["floor_number"] = floors["floor_number"].fillna(floors["FLOOR_SORT_SEQUENCE"])

max_floor_number = floors["floor_number"].max()
top_floors = floors.loc[floors["floor_number"] == max_floor_number].copy()

out = (
    top_floors.merge(
        buildings[["FCLT_BUILDING_KEY", "BUILDING_NAME"]],
        on="FCLT_BUILDING_KEY",
        how="left"
    )
    [["BUILDING_NAME", "FLOOR"]]
    .drop_duplicates()
    .rename(columns={"BUILDING_NAME": "name", "FLOOR": "floor"})
    .reset_index(drop=True)
)

result = {"building_with_largest_floor_number": out}
