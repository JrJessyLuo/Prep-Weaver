import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Ensure join keys are comparable
t1["Receipt"] = pd.to_numeric(t1["Receipt"], errors="coerce")
t2["sjb"] = pd.to_numeric(t2["sjb"], errors="coerce")

items_15 = (
    t2.loc[t2["khid"].eq(15), ["sjb"]]
      .merge(t1[["Receipt", "Item"]], left_on="sjb", right_on="Receipt", how="inner")
      .loc[:, ["Item"]]
      .dropna()
      .drop_duplicates()
      .sort_values("Item")
      .reset_index(drop=True)
)

result = {"distinct_items_bought_by_customer_15": items_15}
