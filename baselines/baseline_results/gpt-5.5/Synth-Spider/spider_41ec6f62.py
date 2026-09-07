import pandas as pd

emp = tables["table_1"]
kv = tables["table_2"]

fry_id = emp.loc[emp["Name"].eq("Phillip J. Fry"), "EmployeeID"].iloc[0]

mgr = kv[kv["Attribute"].eq("Manager")].copy()
mgr["Value_num"] = pd.to_numeric(mgr["Value"], errors="coerce")

out = (
    mgr.loc[mgr["Value_num"].eq(fry_id), ["ShipmentID"]]
    .drop_duplicates()
    .sort_values("ShipmentID")
    .reset_index(drop=True)
)

result = {"shipments_under_phillip_j_fry": out}
