import pandas as pd

customers = tables["table_1"]
orders = tables["table_2"]

jeromy_ids = customers.loc[
    customers["customer_name"].astype(str).str.strip().str.lower() == "jeromy",
    "customer_id"
].dropna().unique()

out = orders.loc[orders["customer_id"].isin(jeromy_ids), ["order_id", "order_date_only", "order_status_code"]].copy()
out["order_date_only"] = pd.to_datetime(out["order_date_only"], errors="coerce")

out = out.rename(columns={"order_date_only": "order_date"}).sort_values(["order_date", "order_id"]).reset_index(drop=True)

result = {"jeromy_orders": out}
