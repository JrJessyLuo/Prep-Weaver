import pandas as pd

# Source tables from the provided `tables` dict
df_client_attr = tables['table_1']
df_orders = tables['table_2']
df_order_lines = tables['table_3']
# The following tables are provided but not used for this task:
# tables['table_4'], tables['table_5'], tables['table_6']

# Normalize orders.IdClient (strip quotes and cast to Int64)
df_orders_norm = df_orders.copy()
df_orders_norm["IdClient"] = (
    df_orders_norm["IdClient"]
    .astype(str)
    .str.strip()
    .str.replace(r'^"|"$', '', regex=True)
)
df_orders_norm["IdClient"] = pd.to_numeric(df_orders_norm["IdClient"], errors="coerce").astype("Int64")

# Compose IdOrder in order_lines to match orders.IdOrder
df_order_lines_norm = df_order_lines.copy()
df_order_lines_norm["IdOrder"] = (
    df_order_lines_norm["IdOrder_num"].astype(str)
    + df_order_lines_norm["IdOrder_suffix"].astype(str)
)

# Join orders (normalized) with order_lines (composed IdOrder)
merged = df_orders_norm.merge(
    df_order_lines_norm[["ISBN", "amount", "IdOrder"]],
    on="IdOrder",
    how="left",
    validate="one_to_many"
)

# Aggregate total books per client_id (sum of 'amount')
merged["amount"] = merged["amount"].fillna(0)
client_total_books = (
    merged.groupby("IdClient", dropna=False, as_index=False)["amount"]
    .sum()
    .rename(columns={"amount": "total_books"})
)
# Cast IdClient back to int where possible for cleaner display
if pd.api.types.is_integer_dtype(client_total_books["IdClient"]):
    client_total_books["IdClient"] = client_total_books["IdClient"].astype("int64", errors="ignore")

# Map IdClient -> Name from client attributes where attribute == "Name"
client_names = (
    df_client_attr.loc[df_client_attr["attribute"] == "Name", ["IdClient", "details"]]
    .rename(columns={"details": "Name"})
)

# Merge totals with names; keep only clients present in totals
client_totals_with_names = client_total_books.merge(client_names, on="IdClient", how="left")

# Reorder columns to show Name then total_books (and keep IdClient for reference)
final_df = client_totals_with_names[["IdClient", "Name", "total_books"]].sort_values(["IdClient"]).reset_index(drop=True)

# Assign the final answer to `result` as required
result = {"client_total_books_by_name": final_df}