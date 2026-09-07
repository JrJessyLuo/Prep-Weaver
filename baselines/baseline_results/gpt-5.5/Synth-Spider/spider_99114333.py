import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

mac_clients = t2[t2["sic_client_combined"].astype(str).str.contains(r"\bMac\b", na=False)]

out = mac_clients.merge(t1, on="agency_id", how="left")[["agency_details"]].drop_duplicates().reset_index(drop=True)

result = {"agency_details_for_mac_client": out}
