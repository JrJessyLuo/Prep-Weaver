import pandas as pd
import numpy as np

# Source DataFrames from provided `tables` dict
df_invoices = tables['table_1'].copy()
df_payments = tables['table_2'].copy()

# Identify invoices without payments
invoices_without_payments = df_invoices[~df_invoices['invoice_id'].isin(df_payments['invoice_id'])].copy()

# Map status: first non-null/non-empty among ['wc', 'ks', 'gz']
status_cols = ['wc', 'ks', 'gz']

def coalesce_status(row):
    for c in status_cols:
        val = row.get(c)
        if pd.notna(val) and str(val).strip() != "":
            return val
    return np.nan

invoices_without_payments['invoice_status'] = invoices_without_payments.apply(coalesce_status, axis=1)
invoices_without_payments['invoice_status'] = invoices_without_payments['invoice_status'].fillna('Unknown')

# Prepare final answer: invoice ids and statuses for invoices without a payment
final_df = invoices_without_payments[['invoice_id', 'invoice_status']].reset_index(drop=True)

# Package result
result = {"invoices_without_payments_status": final_df}