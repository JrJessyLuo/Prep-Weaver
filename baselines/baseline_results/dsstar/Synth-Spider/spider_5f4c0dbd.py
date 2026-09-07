import pandas as pd

# Source tables from the provided `tables` dict
df_planets = tables['table_1']   # Planets
df_shipments = tables['table_2'] # Shipments
df_packages = tables['table_3']  # Package details

# Reproduce the same logic as the reference code:
# 1) Join packages to shipments on Shipment=ShipmentID, then join to planets on Planet=PlanetID
df_joined = (
    df_packages
    .merge(df_shipments, left_on="Shipment", right_on="ShipmentID", how="left")
    .merge(df_planets, left_on="Planet", right_on="PlanetID", how="left")
)

# 2) Group by planet Name to sum Weight and sort as in the reference
weight_by_planet = (
    df_joined
    .groupby("Name", dropna=False, as_index=False)["Weight"]
    .sum()
    .sort_values(["Weight", "Name"], ascending=[False, True])
)

# Prepare final result mapping
result = {
    "weight_by_planet": weight_by_planet
}