import pandas as pd

df_products = tables["table_1"].copy()
df_sales = tables["table_2"].copy()

id_cols = ["Id_Part1", "Id_Part2", "Id_Part3", "Id_Part4", "Id_Part5"]

# Build the item code used in receipts by concatenating non-null Id parts with "-"
df_products["ItemCode"] = df_products[id_cols].apply(
    lambda r: "-".join([str(v) for v in r.tolist() if pd.notna(v)]),
    axis=1
)

expensive_codes = set(df_products.loc[df_products["Price"] > 13, "ItemCode"])

expensive_receipts = (
    df_sales.loc[(df_sales["Attribute"] == "Item") & (df_sales["Value"].isin(expensive_codes)), "Receipt"]
    .drop_duplicates()
    .sort_values()
    .reset_index(drop=True)
    .to_frame(name="Receipt")
)

result = {"expensive_receipts": expensive_receipts}
