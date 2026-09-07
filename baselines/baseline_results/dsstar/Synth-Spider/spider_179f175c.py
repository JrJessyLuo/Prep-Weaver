import pandas as pd

# Access preloaded tables
df_emp = tables['table_1']          # spider_179f175c_input_0.pkl
df_planets = tables['table_2']      # spider_179f175c_input_1.pkl
df_input2 = tables['table_3']       # spider_179f175c_input_2.pkl
# tables['table_4'] planet_1_Client.pkl (not needed)
# tables['table_5'] planet_1_Has_Clearance.pkl (not needed)
# tables['table_6'] planet_1_Package.pkl (not needed)

# Parse shipments from input_2 to get (Shipment, Manager, Planet)
df_norm = df_input2.copy()
df_norm["ShipmentID"] = df_norm["ShipmentID"].astype(str).str.strip()
df_norm.set_index("ShipmentID", inplace=True)
shipment_cols = [c for c in df_norm.columns if str(c).strip().isdigit()]
shipment_cols = sorted(shipment_cols, key=lambda x: int(str(x)))

# Identify the exact index labels for 'Manager' and 'Planet'
idx_map = {i.lower().strip(): i for i in df_norm.index}
manager_key = idx_map.get("manager", None)
planet_key = idx_map.get("planet", None)

shipments = pd.DataFrame([
    {
        "Shipment": int(str(col)),
        "Manager": pd.to_numeric(df_norm.loc[manager_key, col], errors="ignore") if manager_key in df_norm.index else None,
        "Planet": pd.to_numeric(df_norm.loc[planet_key, col], errors="ignore") if planet_key in df_norm.index else None,
    }
    for col in shipment_cols
])

# Build employee lookup from Name_Position "Name|Position"
# Extract Name and Position
name_pos = df_emp["Name_Position"].str.split("|", n=1, expand=True)
name_pos.columns = ["Name", "Position"]
emp_lookup = pd.concat([df_emp[["EmployeeID"]], name_pos], axis=1)

# Find Turanga Leela's EmployeeID
leela_id = emp_lookup.loc[emp_lookup["Name"].str.strip().str.lower() == "turanga leela", "EmployeeID"].iloc[0]

# Find PlanetID for Mars
mars_id = df_planets.loc[df_planets["Name"].str.strip().str.lower() == "mars", "PlanetID"].iloc[0]

# Filter shipments managed by Leela on Mars
ans = shipments[(shipments["Manager"] == leela_id) & (shipments["Planet"] == mars_id)][["Shipment"]].reset_index(drop=True)

# Prepare result mapping
result = {
    "shipments_on_mars_managed_by_leela": ans
}