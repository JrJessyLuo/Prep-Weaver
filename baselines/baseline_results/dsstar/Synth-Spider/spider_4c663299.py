import pandas as pd
import numpy as np

# Access pre-loaded tables
df_items = tables['table_1']          # products
df_receipts_long = tables['table_2']  # receipts long
df_receipts_wide = tables['table_3']  # receipts wide (2 rows x many columns)

# 1) Identify product Id codes for Apple Pie items (kw contains 'Apple' and sw like 'Pie')
apple_pie_ids = set()
if isinstance(df_items, pd.DataFrame) and set(["Id", "kw", "sw"]).issubset(df_items.columns):
    def safe_lower(x):
        try:
            return str(x).lower()
        except Exception:
            return ""
    items_tmp = df_items.copy()
    items_tmp["kw_l"] = items_tmp["kw"].apply(safe_lower)
    items_tmp["sw_l"] = items_tmp["sw"].apply(safe_lower)
    mask = items_tmp["kw_l"].str.contains("apple", na=False) & items_tmp["sw_l"].str.contains("pie", na=False)
    apple_pie_ids = set(items_tmp.loc[mask, "Id"].dropna().astype(str))

# 2) From receipts long, find receipts that contain any of those Apple Pie item codes
receipts_with_apple_pie = set()
if isinstance(df_receipts_long, pd.DataFrame) and "Receipt" in df_receipts_long.columns and len(apple_pie_ids) > 0:
    item_cols = [c for c in df_receipts_long.columns if c != "Receipt"]
    df_codes = df_receipts_long[item_cols].astype(str)
    has_apple = df_codes.apply(lambda row: any(code in apple_pie_ids for code in row.values if code and code != "nan"), axis=1)
    receipts_with_apple_pie = set(df_receipts_long.loc[has_apple, "Receipt"].astype(str))

# 3) From receipts wide, identify receipts with CustomerId = 12
receipts_with_customer12 = set()
if isinstance(df_receipts_wide, pd.DataFrame) and df_receipts_wide.shape[0] >= 2:
    wide = df_receipts_wide.copy()
    cols = list(wide.columns)
    receipt_cols = cols[1:] if len(cols) > 1 else []
    if len(receipt_cols) > 0:
        top_labels = wide.iloc[0, :]
        bottom_vals = wide.iloc[1, :]
        for col in receipt_cols:
            label = str(top_labels[col]).strip()
            if label.lower() == "customerid":
                val = bottom_vals[col]
                if pd.notna(val) and int(str(val).strip()) == 12:
                    receipts_with_customer12.add(str(col))

# 4) Union of the two sets -> final Receipt numbers
final_receipts = sorted(receipts_with_apple_pie.union(receipts_with_customer12))

# Build final answer DataFrame
answer_df = pd.DataFrame({"Receipt": final_receipts})

# Assign to result dict as required
result = {"receipts_union_apple_pie_or_customer12": answer_df}