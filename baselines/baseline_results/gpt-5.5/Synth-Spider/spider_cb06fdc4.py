import pandas as pd

clients = tables["table_1"][["IdClient", "Name"]].copy()
orders = tables["table_2"][["IdOrder", "IdClient"]].copy()

order_counts = (
    orders.groupby("IdClient", as_index=False)
    .agg(number_of_orders=("IdOrder", "count"))
)

out = (
    clients.merge(order_counts, on="IdClient", how="left")
    .assign(number_of_orders=lambda d: d["number_of_orders"].fillna(0).astype(int))
    [["Name", "number_of_orders"]]
)

result = {"client_order_counts": out}
