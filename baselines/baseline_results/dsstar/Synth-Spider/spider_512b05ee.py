import pandas as pd

# Source tables from provided dict
df_invoices = tables['table_1'].copy()
df_shipments = tables['table_2'].copy()

# Clean invoice number similar to reference
def clean_invoice_number(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    if len(s) >= 2 and ((s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'")):
        s = s[1:-1]
    s = s.replace('"', '').replace("'", "")
    return pd.to_numeric(s, errors="coerce").astype("Int64")

df_invoices_clean = df_invoices.copy()
df_invoices_clean["invoice_number_clean"] = clean_invoice_number(df_invoices_clean["invoice_number"]).astype(float).astype("Int64")

# Parse evt to datetime as in reference
def parse_evt_datetime(evt):
    if pd.isna(evt):
        return pd.NaT
    s = str(evt).strip()
    if ":" in s:
        parts = s.split(":", 1)
        if len(parts) == 2:
            ts = parts[1].strip()
            dt = pd.to_datetime(ts, errors="coerce")
            if pd.isna(dt):
                return pd.to_datetime(s, errors="coerce")
            return dt
    return pd.to_datetime(s, errors="coerce")

df_invoices_clean["evt_ts"] = df_invoices_clean["evt"].apply(parse_evt_datetime)

# Combine shipment date and time into a single datetime (not required for final grouping, but kept per reference)
df_shipments_dt = df_shipments.copy()
df_shipments_dt["shipment_ts"] = pd.to_datetime(
    df_shipments_dt["shipment_date_part"].astype(str) + " " + df_shipments_dt["shipment_time_part"].astype(str),
    errors="coerce"
)

# Merge on cleaned key
merged = df_invoices_clean.merge(
    df_shipments_dt,
    left_on="invoice_number_clean",
    right_on="invoice_number",
    how="inner",
    suffixes=("_inv", "_ship")
)

# Count distinct shipments per invoice
shipment_counts = (
    merged.groupby("invoice_number_clean")["shipment_id"]
    .nunique()
    .reset_index(name="shipment_count")
)

eligible_invoices = shipment_counts[shipment_counts["shipment_count"] >= 2]["invoice_number_clean"]

# Final result: invoice ids and their evt_ts (dates) for those with >=2 shipments
final_df = (
    merged[merged["invoice_number_clean"].isin(eligible_invoices)]
    .loc[:, ["invoice_number_clean", "evt_ts"]]
    .drop_duplicates()
    .sort_values(["invoice_number_clean", "evt_ts"])
    .reset_index(drop=True)
)

# Assign to result dict as required
result = {"invoices_with_2plus_shipments_dates_ids": final_df}