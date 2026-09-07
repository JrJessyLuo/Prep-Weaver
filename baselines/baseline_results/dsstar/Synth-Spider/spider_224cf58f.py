import pandas as pd

# Source DataFrames from provided 'tables' dict
customers = tables['table_1']
orders = tables['table_2']

# Reproduce the same logic: left join customers to orders on customer_id
joined = customers.merge(orders, on="customer_id", how="left", suffixes=("_cust", "_ord"))

# Identify customers with no orders: rows where order_id is NaN
no_order_customers = joined[joined['order_id'].isna()][['customer_id']].drop_duplicates().sort_values('customer_id').reset_index(drop=True)

# Prepare final result mapping as required
result = {
    "customers_without_orders": no_order_customers
}