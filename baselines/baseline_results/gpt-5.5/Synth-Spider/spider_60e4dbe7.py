import pandas as pd

# Load tables
products = tables["table_1"].copy()
order_items = tables["table_3"].copy()

# Ensure join keys are comparable
products["product_id"] = pd.to_numeric(products["product_id"], errors="coerce")
order_items["product_id"] = pd.to_numeric(order_items["product_id"], errors="coerce")

# Count distinct orders per product and keep products listed in < 2 orders
order_counts = (
    order_items.dropna(subset=["product_id", "order_id"])
    .groupby("product_id", as_index=False)["order_id"]
    .nunique()
    .rename(columns={"order_id": "num_orders"})
)

eligible_product_ids = order_counts.loc[order_counts["num_orders"] < 2, "product_id"]

# Select requested product fields
cols = [c for c in ["product_id", "product_name", "product_price", "product_color"] if c in products.columns]
out = (
    products.loc[products["product_id"].isin(eligible_product_ids), cols]
    .drop_duplicates()
    .sort_values("product_id")
    .reset_index(drop=True)
)

result = {"products_listed_in_less_than_two_orders": out}
