import pandas as pd

# Source DataFrames from provided `tables` dict
# Mapping per guideline:
# tables['table_2'] -> clients/agencies (spider_dec606a6_input_1.pkl)
# tables['table_3'] -> invoices (spider_dec606a6_input_2.pkl)
df_ca = tables['table_2']  # columns: client_id, agency_id, attribute, value
df_inv = tables['table_3'] # columns: invoice_id, client_id, invoice_details_Finish, invoice_details_Starting, invoice_details_Working

# 1) Pivot client/agency attributes to wide format
if not df_ca.empty:
    df_ca_pivot = df_ca.pivot_table(
        index=["client_id", "agency_id"],
        columns="attribute",
        values="value",
        aggfunc="first"
    ).reset_index()
else:
    df_ca_pivot = df_ca.copy()

# 2) Derive invoice_status and details per invoice by melting/selecting non-null among Finish/Starting/Working
status_cols = {
    "invoice_details_Finish": "Finish",
    "invoice_details_Starting": "Starting",
    "invoice_details_Working": "Working"
}

df_inv_long = df_inv.melt(
    id_vars=["invoice_id", "client_id"],
    value_vars=list(status_cols.keys()),
    var_name="invoice_detail_col",
    value_name="invoice_detail_value"
)

df_inv_long["invoice_status"] = df_inv_long["invoice_detail_col"].map(status_cols)

df_inv_long_nonnull = df_inv_long.dropna(subset=["invoice_detail_value"]).rename(
    columns={"invoice_detail_value": "invoice_detail"}
).drop(columns=["invoice_detail_col"])

# 3) Join with pivoted client/agency attributes on client_id
df_consolidated = df_inv_long_nonnull.merge(df_ca_pivot, on="client_id", how="left")

# 4) Select and rename columns to show:
# - invoice status codes and details
# - corresponding client id and details
# - corresponding agency id and details (if available in attributes)
# The pivoted attributes include 'client_details' and 'sic_code' per reference output.
# We will include available columns safely.
cols_present = df_consolidated.columns

selected_cols = ["invoice_id", "invoice_status", "invoice_detail", "client_id", "client_details", "agency_id"]
selected_cols = [c for c in selected_cols if c in cols_present]

# Build final answer DataFrame
answer_df = df_consolidated[selected_cols].sort_values(["invoice_id", "invoice_status"]).reset_index(drop=True)

# Package final result as required
result = {
    "invoice_status_with_client_agency_details": answer_df
}