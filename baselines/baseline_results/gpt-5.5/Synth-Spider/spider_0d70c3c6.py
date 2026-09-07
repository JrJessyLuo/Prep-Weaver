import pandas as pd

products = tables["table_1"].copy()
order_items_raw = tables["table_2"].copy()

# table_2 is stored transposed (row keys in 'order_item_id'); normalize to long/wide records
order_items = (
    order_items_raw.set_index("order_item_id")
    .T.reset_index(drop=True)
    .rename_axis(None, axis=1)
)

# Ensure expected columns exist and types are numeric where needed
if "product_id" in order_items.columns:
    ordered_product_ids = pd.to_numeric(order_items["product_id"], errors="coerce").dropna().astype(int).unique()
else:
    ordered_product_ids = pd.array([], dtype="int64")

# Products with no order items
out = products.loc[~products["product_id"].isin(ordered_product_ids), ["product_name"]].drop_duplicates().reset_index(drop=True)

result = {"products_without_orders": out}
