import pandas as pd

# Access input DataFrames from the provided `tables` dictionary
customers = tables['table_1']
orders = tables['table_2']

# The 'orders' DataFrame appears pivot-like with the first column as a row label (e.g., 'customer_id')
# and subsequent columns as order_ids with values. We will reshape it to long format and extract
# the order_id -> customer_id mapping as in the reference logic.

orders = orders.copy()
label_col = 'order_id'
first_label = orders.iloc[0, 0]
row_id_name = str(first_label) if pd.notna(first_label) else "row_id"

# Rename the first column to the detected row id name
orders_renamed = orders.rename(columns={label_col: row_id_name})

# Melt to long format
long_orders = orders_renamed.melt(id_vars=[row_id_name], var_name="order_id", value_name="value")

# Detect and extract the order_id -> customer_id mapping row
unique_row_ids = orders_renamed[row_id_name].unique()
if "customer_id" in unique_row_ids:
    customer_orders_long = long_orders[long_orders[row_id_name] == "customer_id"].copy()
    customer_orders_long["order_id"] = pd.to_numeric(customer_orders_long["order_id"], errors="coerce")
    customer_orders_long["customer_id"] = pd.to_numeric(customer_orders_long["value"], errors="coerce").astype("Int64")
    customer_orders = customer_orders_long.drop(columns=[row_id_name, "value"]).dropna(subset=["order_id", "customer_id"])
else:
    raise ValueError("Could not detect 'customer_id' label row in orders data to derive order_id -> customer_id mapping.")

# Join orders with customers to enrich with customer info
orders_with_customers = customer_orders.merge(customers, on="customer_id", how="left")

# Group by customer to count unique orders
order_counts = (
    orders_with_customers.groupby(["customer_id", "customer_name"], dropna=False)
    .agg(order_count=("order_id", "nunique"))
    .reset_index()
)

# Left-join counts back to customers to include customers with zero orders
customers_with_counts = customers.merge(order_counts, on=["customer_id", "customer_name"], how="left")
customers_with_counts["order_count"] = customers_with_counts["order_count"].fillna(0).astype(int)

# Prepare final answer DataFrame with required columns
final_df = customers_with_counts[["customer_id", "customer_name", "order_count"]].sort_values(
    ["order_count", "customer_id"]
).reset_index(drop=True)

# Assign result as required
result = {
    "customers_order_counts": final_df
}