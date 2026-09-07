import pandas as pd

planets = tables["table_1"]
shipments = tables["table_2"]
packages = tables["table_3"]

# Join packages to shipments to get planet per package
pkg_ship = packages.merge(
    shipments[["ShipmentID", "Planet"]],
    left_on="Shipment",
    right_on="ShipmentID",
    how="inner"
)

# Sum package weights per planet
by_planet = (
    pkg_ship.groupby("Planet", as_index=False)["Weight"]
    .sum()
    .rename(columns={"Weight": "total_weight"})
)

# Add planet names
out = by_planet.merge(
    planets[["PlanetID", "Name"]],
    left_on="Planet",
    right_on="PlanetID",
    how="left"
)

out = out[["Name", "total_weight"]].sort_values("Name").reset_index(drop=True)

result = {"total_weight_by_planet": out}
