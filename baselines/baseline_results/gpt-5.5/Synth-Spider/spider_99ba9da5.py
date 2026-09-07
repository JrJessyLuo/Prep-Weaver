import pandas as pd

df_cap = tables["table_1"].copy()
df_items = tables["table_2"].copy()

# Parse warehouse id from the encoded code field in table_1
df_cap["wh_id"] = pd.to_numeric(
    df_cap["NumberWithQuoteSuffix"].astype(str).str.extract(r"(\d+)")[0],
    errors="coerce"
)

# Reconstruct the warehouse "code"
df_cap["Code"] = df_cap["QuotePrefix"].fillna("").astype(str) + df_cap["NumberWithQuoteSuffix"].fillna("").astype(str)

# Current occupancy per warehouse from table_2
occ = df_items.groupby("wh", as_index=False).size().rename(columns={"wh": "wh_id", "size": "occupancy"})

# Compare occupancy to capacity
m = occ.merge(df_cap[["wh_id", "Capacity", "Code"]], on="wh_id", how="inner")
out = m.loc[m["occupancy"] > m["Capacity"], ["Code"]].drop_duplicates().reset_index(drop=True)

result = {"warehouses_above_capacity": out}
