import pandas as pd

customers = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# table_2 is transposed: rows are attributes, columns are orders
orders = (
    t2.set_index("order_id")
      .T
      .reset_index()
      .rename(columns={"index": "order_id"})
)

# Clean types
orders["order_id"] = pd.to_numeric(orders["order_id"], errors="coerce").astype("Int64")
orders["customer_id"] = pd.to_numeric(orders.get("customer_id"), errors="coerce").astype("Int64")

# Count orders per customer
order_counts = (
    orders.dropna(subset=["customer_id"])
          .groupby("customer_id", as_index=False)
          .agg(number_of_orders=("order_id", "count"))
)

# All customers with 0 where no orders
out = (
    customers[["customer_id", "customer_name"]]
    .merge(order_counts, on="customer_id", how="left")
)
out["number_of_orders"] = out["number_of_orders"].fillna(0).astype(int)

result = {"customer_order_counts": out[["customer_name", "customer_id", "number_of_orders"]]}
