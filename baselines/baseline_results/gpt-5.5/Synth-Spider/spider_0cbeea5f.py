import pandas as pd

df1 = tables["table_1"].copy()
df2 = tables["table_2"].copy()

# Build plane -> location mapping from the transposed/encoded table_2
value_row = df2.set_index("plane_name").loc["value"]
plane_cols = [c for c in value_row.index if c != "plane_name"]
plane_location = (
    value_row[plane_cols]
    .rename("hangar_location")
    .reset_index()
    .rename(columns={"index": "plane"})
)

# Join and aggregate by hangar location
joined = df1.merge(plane_location, on="plane", how="left")

out = (
    joined.groupby("hangar_location", as_index=False)
    .agg(
        pilot_count=("pilot", "nunique"),
        average_age=("age", "mean"),
    )
    .sort_values("hangar_location")
    .reset_index(drop=True)
)

result = {"hangar_locations_pilots_and_average_ages": out}
