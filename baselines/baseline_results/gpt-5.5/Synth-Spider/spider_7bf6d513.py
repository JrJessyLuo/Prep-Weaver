import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Convert table_2 (wide plane columns) into a long mapping: plane -> location
loc_row = t2[t2["plane_name"].astype(str).str.lower() == "location"]
plane_locs = (
    loc_row
    .drop(columns=["plane_name"])
    .melt(var_name="pln", value_name="location")
    .dropna(subset=["location"])
)

# Join pilots' planes with plane locations
pilots_with_locs = t1.merge(plane_locs, on="pln", how="inner")

# Pilots who have planes in both Austin and Boston
need = {"Austin", "Boston"}
qualified = (
    pilots_with_locs.groupby("pn")["location"]
    .apply(lambda s: need.issubset(set(s)))
    .loc[lambda x: x]
    .index
)

out = pd.DataFrame({"pilot_name": sorted(qualified)})

result = {"pilots_in_austin_and_boston": out}
