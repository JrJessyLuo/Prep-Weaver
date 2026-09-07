import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# EmployeeID for Turanga Leela
t1[["EmployeeName", "Position"]] = t1["Name_Position"].astype(str).str.split("|", n=1, expand=True)
leela_id = t1.loc[t1["EmployeeName"].eq("Turanga Leela"), "EmployeeID"].iloc[0]

# PlanetID for Mars
mars_id = t2.loc[t2["Name"].eq("Mars"), "PlanetID"].iloc[0]

# table_3 is transposed key-value; convert to natural shipment table
ship_long = t3.melt(id_vars=["ShipmentID"], var_name="Shipment", value_name="value")
ship_wide = (
    ship_long.pivot_table(index="Shipment", columns="ShipmentID", values="value", aggfunc="first")
    .reset_index()
)
ship_wide["Shipment"] = pd.to_numeric(ship_wide["Shipment"], errors="coerce")

# Filter shipments on Mars managed by Turanga Leela
ship_wide["Manager"] = pd.to_numeric(ship_wide["Manager"], errors="coerce")
ship_wide["Planet"] = pd.to_numeric(ship_wide["Planet"], errors="coerce")

out = (
    ship_wide.loc[(ship_wide["Manager"].eq(leela_id)) & (ship_wide["Planet"].eq(mars_id)), ["Shipment"]]
    .rename(columns={"Shipment": "ShipmentID"})
    .sort_values("ShipmentID")
    .reset_index(drop=True)
)

result = {"shipments_on_mars_managed_by_turanga_leela": out}
