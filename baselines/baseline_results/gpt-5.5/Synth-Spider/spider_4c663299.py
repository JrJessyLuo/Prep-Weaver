import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]
t3 = tables["table_3"]

# Receipts that include an apple-flavor pie item
apple_pie_ids = t1.loc[
    t1["kw"].astype(str).str.contains("apple", case=False, na=False)
    & t1["sw"].astype(str).str.contains("pie", case=False, na=False),
    "Id"
].dropna().unique()

items_long = (
    t2.melt(id_vars=["Receipt"], value_vars=[c for c in t2.columns if c != "Receipt"], value_name="ItemId")
      .dropna(subset=["ItemId"])
)

receipts_with_apple_pie = items_long.loc[items_long["ItemId"].isin(apple_pie_ids), "Receipt"].unique()

# Receipts shopped by customer id 12 (table_3 is transposed key-value)
receipt_meta = (
    t3.set_index("ReceiptNumber").T.reset_index()
      .rename(columns={"index": "Receipt"})
)
receipt_meta["Receipt"] = pd.to_numeric(receipt_meta["Receipt"], errors="coerce")
receipt_meta["CustomerId"] = pd.to_numeric(receipt_meta.get("CustomerId"), errors="coerce")

receipts_customer_12 = receipt_meta.loc[receipt_meta["CustomerId"] == 12, "Receipt"].dropna().astype(int).unique()

# Union of both sets
all_receipts = sorted(set(map(int, receipts_with_apple_pie)).union(set(map(int, receipts_customer_12))))

result = {
    "receipt_numbers": pd.DataFrame({"Receipt": all_receipts})
}
