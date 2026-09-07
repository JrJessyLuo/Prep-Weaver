import pandas as pd

customers = tables["table_1"].copy()
orders_wide = tables["table_2"].copy()

# Treat each row in table_2 as an order
orders_wide = orders_wide.reset_index().rename(columns={"index": "Order_ID"})

dish_cols = [c for c in orders_wide.columns if c not in ["Order_ID", "Customer_ID", "Branch_ID"]]

orders_long = orders_wide.melt(
    id_vars=["Order_ID", "Customer_ID", "Branch_ID"],
    value_vars=dish_cols,
    var_name="dish_name",
    value_name="quantity",
)

orders_long = orders_long.dropna(subset=["quantity"])
orders_long = orders_long[orders_long["quantity"] > 0]

out = orders_long.merge(
    customers[["Customer_ID", "Name"]],
    on="Customer_ID",
    how="left",
).rename(columns={"Name": "customer_name"})

out = out[["Order_ID", "customer_name", "dish_name", "quantity"]].sort_values(
    by="quantity", ascending=False
).reset_index(drop=True)

result = {"orders_customer_dish": out}
