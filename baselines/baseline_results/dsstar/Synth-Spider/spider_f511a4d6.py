import pandas as pd

# Access pre-loaded tables
df_cyclists = tables['table_1']  # cyclists_info
df_purchases = tables['table_2']  # bike_purchases

# Reproduce the SAME logic as the reference code
# Determine keys and how to identify zero purchases
df_purchases = df_purchases.copy()
df_purchases["bike_purchase_combined"] = df_purchases["bike_purchase_combined"].astype(object)
valid_purchases = df_purchases[
    df_purchases["bike_purchase_combined"].notna() &
    (df_purchases["bike_purchase_combined"].astype(str).str.strip() != "")
]

purchased_ids = set(valid_purchases["cyclist_id"].unique())
all_cyclist_ids = set(df_cyclists["id"].unique())
zero_purchase_ids = sorted(list(all_cyclist_ids - purchased_ids))

# Cyclists with zero purchases
df_zero_purchases = df_cyclists[df_cyclists["id"].isin(zero_purchase_ids)].copy()

# Split nation_result into nation and result by the '|' delimiter (same as reference)
nr = df_cyclists["nation_result"].astype(str)
split_cols = nr.str.split("|", n=1, expand=True)
if split_cols.shape[1] == 1:
    split_cols[1] = pd.NA
split_cols.columns = ["nation", "result"]

# Attach to the cyclists DataFrame
df_cyclists_enriched = df_cyclists.copy()
df_cyclists_enriched[["nation", "result"]] = split_cols

# Final answer: name, nation, result for cyclists who did not purchase any racing bike
answer_df = (
    df_cyclists_enriched[df_cyclists_enriched["id"].isin(zero_purchase_ids)]
    .loc[:, ["name", "nation", "result"]]
    .reset_index(drop=True)
)

result = {"cyclists_no_racing_bike_purchases": answer_df}