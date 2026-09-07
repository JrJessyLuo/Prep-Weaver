import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['invoice_number','invoice_status_code','invoice_date']].copy()
    target['invoice_number'] = pd.to_numeric(target['invoice_number'], errors='coerce').astype('Int64')
    target['invoice_date'] = pd.to_datetime(target['invoice_date'], errors='coerce')
    target = target.dropna(subset=['invoice_number']).drop_duplicates(subset=['invoice_number']).reset_index(drop=True)
    target = target.loc[:, ['invoice_number','invoice_status_code','invoice_date']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['invoice_number','shipment_date']].copy()
    df['shipment_date'] = pd.to_datetime(df['shipment_date'], errors='coerce', dayfirst=True, infer_datetime_format=True)
    df.loc[df['shipment_date'].isna(), 'shipment_date'] = pd.to_datetime(table_1.loc[df['shipment_date'].isna(), 'shipment_date'], errors='coerce', dayfirst=False, infer_datetime_format=True)
    target = df[['invoice_number','shipment_date']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_invoices = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_shipments = prepared_table_2

target = prepared_invoices.merge(prepared_shipments, on='invoice_number', how='left')[['invoice_number','invoice_status_code','invoice_date','shipment_date']].sort_values('invoice_number')

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
