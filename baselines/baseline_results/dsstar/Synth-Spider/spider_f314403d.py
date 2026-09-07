import pandas as pd

# Source DataFrames from provided `tables` dict
invoices = tables['table_1'].copy()
shipments = tables['table_2'].copy()

# Parse dates
invoices_parsed = invoices.copy()
invoices_parsed["invoice_date"] = pd.to_datetime(invoices_parsed["invoice_date"], errors="coerce")

shipments_parsed = shipments.copy()

# Attempt to parse shipment_date with multiple possible formats to mirror mixed inputs
shipment_date = pd.to_datetime(
    shipments_parsed["shipment_date"],
    format="%d/%m/%Y %I:%M:%S %p",
    errors="coerce"
)
# Fill remaining NaT via general parser (handles 'Mar 07, 2018 01:57:14', '2018-03-18 22:23:19', etc.)
mask_na = shipment_date.isna()
if mask_na.any():
    shipment_date.loc[mask_na] = pd.to_datetime(shipments_parsed.loc[mask_na, "shipment_date"], errors="coerce")
shipments_parsed["shipment_date"] = shipment_date

# Join on invoice_number (inner as in reference code)
joined = pd.merge(
    invoices_parsed,
    shipments_parsed,
    on="invoice_number",
    how="inner",
    suffixes=("_invoice", "_shipment")
)

# Select needed columns
cols_needed = ["invoice_number", "invoice_status_code", "invoice_date", "shipment_date"]
joined_subset = joined[cols_needed].copy()

# Aggregate to one row per invoice with earliest shipment_date
agg_df = (
    joined_subset
    .sort_values(["invoice_number", "shipment_date"])
    .groupby("invoice_number", as_index=False)
    .agg({
        "invoice_status_code": "first",
        "invoice_date": "first",
        "shipment_date": "min"
    })
)

# Final answer
result = {
    "invoices_with_status_and_shipment_dates": agg_df
}