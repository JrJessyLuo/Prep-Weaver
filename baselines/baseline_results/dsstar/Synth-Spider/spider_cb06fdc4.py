import pandas as pd

# Source DataFrames from provided `tables` mapping
df_clients = tables['table_1']
df_orders = tables['table_2']

# Left-join clients to orders to ensure clients with zero orders are retained
orders_with_clients = df_clients[["IdClient", "Name"]].merge(
    df_orders[["IdClient", "IdOrder"]],
    on="IdClient",
    how="left"
)

# Compute counts per client name; NaN IdOrder means zero orders
order_counts = (
    orders_with_clients
    .groupby("Name", dropna=False)["IdOrder"]
    .count()
    .reset_index(name="OrderCount")
)

# Ensure integer counts and sort as in the reference
order_counts["OrderCount"] = order_counts["OrderCount"].astype(int)
final_df = order_counts.sort_values(["OrderCount", "Name"], ascending=[False, True]).reset_index(drop=True)

# Package final result
result = {
    "client_order_counts": final_df
}