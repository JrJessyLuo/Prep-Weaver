import pandas as pd

inv = tables["table_1"].copy()
shp = tables["table_2"].copy()

# Parse dates to consistent datetime dtype (handles mixed formats)
inv["invoice_date"] = pd.to_datetime(inv["invoice_date"], errors="coerce")
shp["shipment_date"] = pd.to_datetime(shp["shipment_date"], errors="coerce", dayfirst=True)

out = inv.merge(
    shp[["invoice_number", "shipment_date"]],
    on="invoice_number",
    how="left"
)

out = out[["invoice_number", "invoice_status_code", "invoice_date", "shipment_date"]].sort_values(
    ["invoice_number", "shipment_date"],
    na_position="last"
).reset_index(drop=True)

result = {"invoices_with_status_and_shipment_dates": out}
