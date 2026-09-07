import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['invoice_id']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    filtered = table_1.loc[table_1['column'].eq('invoice_payment'), ['value']].copy()
    split_cols = filtered['value'].astype(str).str.split('-', n=1, expand=True)
    filtered['invoice_id'] = split_cols[0].astype(str)
    filtered['payment_status'] = split_cols[1]
    target = filtered[['invoice_id', 'payment_status']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_invoices = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_payments = prepared_table_2

# prepared_invoices: columns -> ['invoice_id']
# prepared_payments: columns -> ['invoice_id','payment_status']

# Join invoices to payments on invoice_id
joined = prepared_invoices.merge(prepared_payments, on='invoice_id', how='inner')

# Select distinct invoice ids and payment statuses
result = joined[['invoice_id','payment_status']].drop_duplicates()

target = result

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
