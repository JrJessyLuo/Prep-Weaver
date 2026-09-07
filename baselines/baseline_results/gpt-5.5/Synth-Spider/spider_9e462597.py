import pandas as pd

customers = tables["table_1"][["customer_id"]].drop_duplicates()
orders = tables["table_2"][["customer_id"]].drop_duplicates()

no_order_customers = (
    customers.merge(orders, on="customer_id", how="left", indicator=True)
    .query('_merge == "left_only"')[["customer_id"]]
    .sort_values("customer_id")
    .reset_index(drop=True)
)

result = {"customers_without_orders": no_order_customers}
