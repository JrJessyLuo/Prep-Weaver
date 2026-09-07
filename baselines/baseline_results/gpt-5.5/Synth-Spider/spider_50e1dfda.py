import pandas as pd

clients = tables["table_1"].copy()
orders = tables["table_2"].copy()

# Normalize IdOrder (some rows contain multiple order ids separated by commas)
orders["IdOrder"] = orders["IdOrder"].astype(str)
orders = orders.assign(
    IdOrder=orders["IdOrder"].str.split(",")
).explode("IdOrder")
orders["IdOrder"] = orders["IdOrder"].astype(str).str.strip()
orders = orders[orders["IdOrder"].ne("") & orders["IdOrder"].ne("nan")]

out = orders.merge(
    clients[["IdClient", "Name"]],
    on="IdClient",
    how="left"
)[["IdOrder", "Name"]].drop_duplicates().sort_values(["IdOrder", "Name"]).reset_index(drop=True)

result = {"orders_with_client_names": out}
