import pandas as pd

# Access pre-loaded DataFrames from the provided `tables` dict
df0 = tables['table_1']  # columns: Receipt (int), Ordinal (int), Item (str)
df1 = tables['table_2']  # columns: sjb (int), Date (obj), khid (int)

# Filter df1 for khid == 15 to get list of sjb (receipt IDs)
sjb_list = df1.loc[df1["khid"] == 15, "sjb"].dropna().astype(int).unique().tolist()

# Subset df0 to rows where Receipt is in that list
filtered = df0[df0["Receipt"].isin(sjb_list)].copy()

# Get distinct items
distinct_items = (
    filtered.loc[:, ["Item"]]
    .dropna()
    .drop_duplicates()
    .sort_values(by="Item")
    .reset_index(drop=True)
)

# Package final answer as required
result = {"distinct_items_for_khid_15": distinct_items}