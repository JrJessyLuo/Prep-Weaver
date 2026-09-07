import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['client_id','agency_id','attribute','value']].copy()
    target['attribute'] = target['attribute'].astype('string').str.strip()
    target['value'] = target['value'].astype('string').str.strip()
    target = target.dropna(subset=['client_id','agency_id','attribute'])
    target = target.drop_duplicates(subset=['client_id','agency_id','attribute','value']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['invoice_id','client_id','invoice_details_Finish','invoice_details_Starting','invoice_details_Working']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['agency_id','staff_id','staff_details']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_invoices = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_agencies = prepared_table_3

# prepared tables are provided as dataframes: prepared_invoices, prepared_clients, prepared_agencies
# 1) Join invoices to client-agency metadata on client_id
ivc = prepared_invoices.merge(prepared_clients, on='client_id', how='left', suffixes=('', '_clientmeta'))

# 2) Join to agency details on agency_id
ivc_ag = ivc.merge(prepared_agencies, on='agency_id', how='left', suffixes=('', '_agency'))

# 3) Select columns to show invoice status codes/details plus client and agency identifiers/details
# Pivot client attribute/value pairs into columns for readability (client_details, sic_code, agency_details if present)
client_attrs = ivc_ag.pivot_table(index=['invoice_id','client_id','agency_id','invoice_details_Finish','invoice_details_Starting','invoice_details_Working','staff_id','staff_details'], 
                                  columns='attribute', values='value', aggfunc='first').reset_index()
client_attrs.columns = [c if not isinstance(c, tuple) else (c[1] if c[1] else c[0]) for c in client_attrs.columns]

# Build final view. If an explicit agency_details attribute exists in client metadata, keep it; otherwise we can expose staff_details as agency_details_proxy.
cols_base = ['invoice_id','client_id','agency_id','invoice_details_Finish','invoice_details_Starting','invoice_details_Working']
possible_client_detail_cols = [c for c in client_attrs.columns if c not in cols_base + ['staff_id','staff_details']]
final_cols = cols_base + possible_client_detail_cols + ['staff_details']
final = client_attrs[final_cols].sort_values(['invoice_id','client_id','agency_id'])

target = final

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
