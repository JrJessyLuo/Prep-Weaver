import pandas as pd

inv_evt = tables["table_1"].copy()
ship = tables["table_2"].copy()

# Normalize invoice_number for joining (remove embedded quotes, cast to int)
inv_evt["invoice_number"] = (
    inv_evt["invoice_number"]
    .astype(str)
    .str.extract(r"(\d+)", expand=False)
    .astype("Int64")
)

# Extract datetime from evt like "Paid:2018-03-09 07:16:07"
inv_evt["invoice_datetime"] = pd.to_datetime(
    inv_evt["evt"].astype(str).str.split(":", n=1).str[1],
    errors="coerce"
)

# Use earliest known invoice datetime as the invoice "date"
inv_dates = (
    inv_evt.dropna(subset=["invoice_number"])
    .groupby("invoice_number", as_index=False)["invoice_datetime"]
    .min()
)
inv_dates["invoice_date"] = inv_dates["invoice_datetime"].dt.date
inv_dates = inv_dates.drop(columns=["invoice_datetime"])

# Invoices related to at least 2 shipments
inv_with_2_ship = (
    ship.groupby("invoice_number", as_index=False)["shipment_id"]
    .nunique()
    .rename(columns={"shipment_id": "num_shipments"})
)
inv_with_2_ship = inv_with_2_ship.loc[inv_with_2_ship["num_shipments"] >= 2, ["invoice_number"]]

out = (
    inv_with_2_ship.merge(inv_dates, on="invoice_number", how="left")
    .rename(columns={"invoice_number": "invoice_id"})
    .sort_values(["invoice_id"], kind="mergesort")
    .reset_index(drop=True)
)

result = {"invoices_related_to_at_least_2_shipments": out}
