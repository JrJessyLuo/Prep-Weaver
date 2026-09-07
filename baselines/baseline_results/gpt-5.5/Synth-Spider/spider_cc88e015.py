import pandas as pd

stores = tables["table_1"].copy()
inv = tables["table_2"].copy()

# Clean quantity to numeric
inv["Quantity"] = (
    inv["Quantity"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.replace(",", "", regex=False)
)
inv["Quantity"] = pd.to_numeric(inv["Quantity"], errors="coerce").fillna(0)

# Total headphones in stock per store
stock_by_store = inv.groupby("Store_ID", as_index=False)["Quantity"].sum()

# Stores with no headphones in stock (no rows in inv or total qty == 0)
stores_stock = stores[["Store_ID", "Name"]].merge(stock_by_store, on="Store_ID", how="left")
stores_stock["Quantity"] = stores_stock["Quantity"].fillna(0)

out = (
    stores_stock.loc[stores_stock["Quantity"].eq(0), ["Name"]]
    .drop_duplicates()
    .rename(columns={"Name": "store_name"})
    .reset_index(drop=True)
)

result = {"stores_without_headphones_in_stock": out}
