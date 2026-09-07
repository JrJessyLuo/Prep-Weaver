import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Product master: Code = ProductID, Popis = full product name
t1["Code"] = pd.to_numeric(t1["Code"], errors="coerce")

# Quantity sold (je) appears as a quoted string like "\"28\""
qty = (
    t2["je"]
    .astype(str)
    .str.replace('"', "", regex=False)
    .str.strip()
)
t2["qty"] = pd.to_numeric(qty, errors="coerce")

# If qty is missing/unparseable, fall back to counting transactions as 1
t2["qty"] = t2["qty"].fillna(1)

top5 = (
    t2.groupby("ProductID", as_index=False)["qty"].sum()
      .sort_values("qty", ascending=False)
      .head(5)
)

top5_named = (
    top5.merge(t1[["Code", "Popis"]], left_on="ProductID", right_on="Code", how="left")
        .rename(columns={"Popis": "product_full_name"})
        [["product_full_name"]]
)

result = {"top_five_best_selling_products": top5_named.reset_index(drop=True)}
