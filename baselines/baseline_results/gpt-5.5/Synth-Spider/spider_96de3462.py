import pandas as pd

df = tables["table_1"].copy()

# Normalize invoice_id (e.g., "\"1\"" -> "1")
df["invoice_id"] = df["invoice_id"].astype(str).str.extract(r"(\d+)", expand=False).fillna(df["invoice_id"])

# Unpivot status columns to get the (invoice_id, status) pairs
m = df.melt(id_vars=["invoice_id"], value_vars=["Finish", "Starting", "Working"],
            var_name="status", value_name="status_value")

out = (
    m[m["status_value"].notna()][["invoice_id", "status"]]
    .drop_duplicates()
    .sort_values(["invoice_id", "status"], kind="stable")
    .reset_index(drop=True)
)

result = {"invoice_payment_statuses": out}
