import pandas as pd

# Clients: pivot/transpose table_1 into a normal client dimension table
clients_raw = tables["table_1"].copy()
clients = (
    clients_raw.set_index("IdClient")
    .T.reset_index()
    .rename(columns={"index": "KH", "Name": "client_name"})
)
clients["KH"] = pd.to_numeric(clients["KH"], errors="coerce").astype("Int64")

# Orders: count number of orders per client (KH)
orders = tables["table_2"].copy()
order_counts = (
    orders.groupby("KH", as_index=False)
    .size()
    .rename(columns={"size": "times_ordered"})
)

# Combine and ensure all clients are listed (even with 0 orders)
out = (
    clients[["KH", "client_name"]]
    .merge(order_counts, on="KH", how="left")
)
out["times_ordered"] = out["times_ordered"].fillna(0).astype(int)

out = out[["client_name", "times_ordered"]].sort_values("client_name").reset_index(drop=True)

result = {"client_order_counts": out}
