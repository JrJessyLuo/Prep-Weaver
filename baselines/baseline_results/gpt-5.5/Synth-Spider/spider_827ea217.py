import pandas as pd

inv = tables["table_1"].copy()
pay = tables["table_2"].copy()

# Infer invoice "status" from the first non-null among the status-like columns
status_cols = [c for c in ["wc", "ks", "gz"] if c in inv.columns]
inv["status"] = inv[status_cols].bfill(axis=1).iloc[:, 0] if status_cols else pd.NA

# Invoices without a payment (anti-join)
no_payment = inv[~inv["invoice_id"].isin(pay["invoice_id"])][["invoice_id", "status"]].reset_index(drop=True)

result = {"invoices_without_payment": no_payment}
