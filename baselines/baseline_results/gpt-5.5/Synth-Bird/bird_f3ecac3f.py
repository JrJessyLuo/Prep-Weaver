import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()
t3 = tables["table_3"].copy()

# Customers whose transactions are in euro
eur_customers = t1.loc[t1["huobi"].astype(str).str.upper().eq("EUR"), ["CustomerID"]].drop_duplicates()

# Normalize ProductID in products table (remove quotes) and cast to numeric for joining
t2["ProductID_clean"] = (
    t2["ProductID"].astype(str)
      .str.replace('"', '', regex=False)
      .str.strip()
)
t2["ProductID_int"] = pd.to_numeric(t2["ProductID_clean"], errors="coerce")

# Filter euro transactions and join to product descriptions
eur_tx = t3.merge(eur_customers, on="CustomerID", how="inner")
out = eur_tx.merge(t2[["ProductID_int", "Description"]], left_on="ProductID", right_on="ProductID_int", how="left")

result_df = out[["Description"]].dropna().drop_duplicates().reset_index(drop=True)

result = {"euro_transaction_product_descriptions": result_df}
