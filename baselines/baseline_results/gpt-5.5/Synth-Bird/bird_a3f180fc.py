import pandas as pd

disp = tables["table_2"].copy()
clients = tables["table_5"].copy()
districts = tables["table_3"].copy()

# Clients who have the right (OWNER) to issue permanent orders / apply for loans
owner_client_ids = (
    disp.loc[(disp["attribute"] == "type") & (disp["value"] == "OWNER"), "client_id"]
    .dropna()
    .drop_duplicates()
)

out = clients.loc[clients["client_id"].isin(owner_client_ids), ["client_id", "district_id"]].copy()

# Add district name (A2) as "district"
out = out.merge(districts[["district_id", "A2"]], on="district_id", how="left")
out = out.rename(columns={"A2": "district"})[["client_id", "district"]].drop_duplicates().sort_values("client_id").reset_index(drop=True)

result = {"clients_id_and_district": out}
