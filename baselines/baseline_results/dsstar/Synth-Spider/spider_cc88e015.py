import pandas as pd

# Access pre-loaded tables
df_stores = tables['table_1']  # spider_cc88e015_input_0.pkl
df_qty = tables['table_2']     # spider_cc88e015_input_1.pkl
# tables['table_3'] is not needed for this task

# Standardize Quantity to numeric:
def clean_quantity(s):
    if pd.isna(s):
        return None
    s_str = str(s).strip()
    if (len(s_str) >= 2) and ((s_str[0] == s_str[-1]) and s_str[0] in ['"', "'"]):
        s_str = s_str[1:-1].strip()
    return s_str

df_qty_clean = df_qty.copy()
df_qty_clean["Quantity_clean"] = df_qty_clean["Quantity"].apply(clean_quantity)
df_qty_clean["Quantity_num"] = pd.to_numeric(df_qty_clean["Quantity_clean"], errors="coerce").fillna(0).astype(int)
df_qty_clean = df_qty_clean.drop(columns=["Quantity", "Quantity_clean"]).rename(columns={"Quantity_num": "Quantity"})

# Aggregate total Quantity per store (sum over headphones)
qty_per_store = (
    df_qty_clean.groupby("Store_ID", as_index=False)["Quantity"]
    .sum()
    .rename(columns={"Quantity": "Total_Quantity"})
)

# Join totals to stores
stores_with_totals = df_stores.merge(qty_per_store, on="Store_ID", how="left")

# Identify stores with total Quantity == 0 or missing
stores_with_totals["Total_Quantity_filled"] = stores_with_totals["Total_Quantity"].fillna(0).astype(int)
stores_zero_or_missing = stores_with_totals[
    (stores_with_totals["Total_Quantity"].isna()) | (stores_with_totals["Total_Quantity_filled"] == 0)
].copy()

# Final answer: store names with zero or missing total quantities
answer_df = stores_zero_or_missing[["Name"]].rename(columns={"Name": "Store_Name"}).reset_index(drop=True)

# Package into result dict as required
result = {
    "stores_without_headphones": answer_df
}