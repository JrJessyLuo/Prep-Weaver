import pandas as pd

customers = tables["table_1"]
orders = tables["table_2"]

customers_with_orders = orders["customer_id"].dropna().unique()
count_no_orders = (~customers["customer_id"].isin(customers_with_orders)).sum()

result = {
    "customers_without_orders_count": pd.DataFrame(
        {"num_customers_without_orders": [int(count_no_orders)]}
    )
}
