import pandas as pd

# Tables
emp = tables["table_1"]
planets = tables["table_2"]
clear = tables["table_3"]

# PlanetID for "Omega III"
omega_id = planets.loc[planets["Name"].eq("Omega III"), "PlanetID"].iloc[0]

# Find the "Planet" row in clearance table (table_3)
planet_row = clear.loc[clear["Employee"].astype(str).str.strip().str.lower().eq("planet")].iloc[0]

# Columns (employees) that have planet == Omega III
planet_vals = planet_row.drop(labels=["Employee"])
cols_with_omega = planet_vals.index[planet_vals.eq(omega_id)]

# Convert column labels to employee IDs where possible
emp_ids = pd.to_numeric(pd.Index(cols_with_omega).astype(str), errors="coerce").dropna().astype(int).tolist()

# Map to employee names
out = (
    emp.loc[emp["ygh"].isin(emp_ids), ["Name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"employees_with_clearance_in_omega_iii": out}
