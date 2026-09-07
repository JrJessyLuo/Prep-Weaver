import pandas as pd

hp = tables["table_1"].copy()
inv = tables["table_2"].copy()

# Normalize quantity to numeric
inv["Quantity_num"] = (
    inv["Quantity"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.extract(r"(-?\d+)", expand=False)
    .astype(float)
    .fillna(0)
    .astype(int)
)

# Headphones that are in stock in at least one store
in_stock_ids = set(
    inv.groupby("Headphone_ID", as_index=False)["Quantity_num"].sum()
       .loc[lambda d: d["Quantity_num"] > 0, "Headphone_ID"]
)

# Models not in stock in any store
out_df = hp.loc[~hp["Headphone_ID"].isin(in_stock_ids), ["Model"]].drop_duplicates().reset_index(drop=True)

result = {"headphone_models_not_in_stock_any_store": out_df}
