import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df[['event_type','event_datetime']] = df['evt'].str.split(':', n=1, expand=True)
    df['event_datetime'] = pd.to_datetime(df['event_datetime'], errors='coerce')
    target = df[['invoice_number','event_type','event_datetime']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.copy()
    prepared['shipment_datetime'] = pd.to_datetime(prepared['shipment_date_part'].astype(str) + ' ' + prepared['shipment_time_part'].astype(str), errors='coerce')
    target = prepared[['invoice_number', 'shipment_id', 'shipment_datetime']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_invoices = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_shipments = prepared_table_2

# prepared_invoices expected columns: invoice_number (str), event_type (str), event_datetime (datetime)
# prepared_shipments expected columns: invoice_number (str), shipment_id (int/str), shipment_datetime (datetime)

# Keep only the invoice date from the invoices table. Prefer the 'Issued' event as the invoice date; if absent, fall back to earliest event.
inv = prepared_invoices.copy()
# If event_datetime not yet datetime, parse it
if not pd.api.types.is_datetime64_any_dtype(inv['event_datetime']):
    inv['event_datetime'] = pd.to_datetime(inv['event_datetime'], errors='coerce')

# Choose issued event when available per invoice
issued = inv[inv['event_type'].str.lower() == 'issued']
issued = issued.sort_values(['invoice_number', 'event_datetime']).drop_duplicates('invoice_number', keep='first')

# For invoices without 'Issued', take earliest event
earliest = inv.sort_values(['invoice_number', 'event_datetime']).drop_duplicates('invoice_number', keep='first')

# Combine preference
inv_dates = pd.concat([issued, earliest[~earliest['invoice_number'].isin(issued['invoice_number'])]])
inv_dates = inv_dates[['invoice_number', 'event_datetime']].rename(columns={'event_datetime': 'invoice_date'})

# Count shipments per invoice
sh = prepared_shipments.copy()
ship_counts = sh.groupby('invoice_number', as_index=False)['shipment_id'].nunique().rename(columns={'shipment_id': 'shipment_count'})

# Join and filter invoices with at least 2 shipments
merged = inv_dates.merge(ship_counts, on='invoice_number', how='inner')
result = merged[merged['shipment_count'] >= 2][['invoice_number', 'invoice_date']].sort_values(['invoice_date', 'invoice_number'])

# Final output: dates and ids (invoice_number)
answer = result.rename(columns={'invoice_number': 'invoice_id', 'invoice_date': 'date'})

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
