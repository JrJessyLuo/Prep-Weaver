import pandas as pd

# Source tables from the provided `tables` dict
fclt_floor = tables['table_4']          # FCLT_FLOOR.pkl
fac_building = tables['table_8']        # FAC_BUILDING.pkl

# Compute distinct floor counts per building key
floor_counts = (
    fclt_floor
    .dropna(subset=["FCLT_BUILDING_KEY", "FLOOR"])
    .groupby("FCLT_BUILDING_KEY")["FLOOR"]
    .nunique()
    .reset_index(name="DISTINCT_FLOOR_COUNT")
)

# Prepare FAC_BUILDING minimal mapping (ensure key is string for safe merge)
fac_building_min = fac_building[["FAC_BUILDING_KEY", "BUILDING_NUMBER", "BUILDING_NAME_LONG"]].copy()
fac_building_min["FAC_BUILDING_KEY"] = fac_building_min["FAC_BUILDING_KEY"].astype(str)
floor_counts["FCLT_BUILDING_KEY"] = floor_counts["FCLT_BUILDING_KEY"].astype(str)

# Merge to attach building info
merged = floor_counts.merge(
    fac_building_min,
    left_on="FCLT_BUILDING_KEY",
    right_on="FAC_BUILDING_KEY",
    how="left"
)

# Identify the maximum DISTINCT_FLOOR_COUNT
max_floor_count = merged["DISTINCT_FLOOR_COUNT"].max()

# Filter buildings with the maximum floor count and select requested fields
top_buildings = (
    merged[merged["DISTINCT_FLOOR_COUNT"] == max_floor_count]
    .loc[:, ["FCLT_BUILDING_KEY", "BUILDING_NUMBER", "BUILDING_NAME_LONG", "DISTINCT_FLOOR_COUNT"]]
    .sort_values(["BUILDING_NAME_LONG", "BUILDING_NUMBER"], na_position="last")
    .reset_index(drop=True)
)

# Final answer: list the names of the buildings with the most floors
answer = top_buildings.loc[:, ["BUILDING_NAME_LONG"]].rename(columns={"BUILDING_NAME_LONG": "BUILDING_NAME"})

# Package result as required
result = {
    "buildings_with_most_floors": answer
}