import pandas as pd

customers = tables["table_1"]
orders = tables["table_2"]

# Customers with no orders
no_order_ids = (
    customers.loc[~customers["customer_id"].isin(orders["customer_id"].dropna().unique()), ["customer_id"]]
    .drop_duplicates()
    .sort_values("customer_id")
    .reset_index(drop=True)
)

result = {"customers_without_orders": no_order_ids}
