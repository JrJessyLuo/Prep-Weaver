import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['invoice_id','wc','ks','gz']].copy()
    df[['wc','ks','gz']] = df[['wc','ks','gz']].replace('nan', pd.NA)
    df['status'] = df[['wc','ks','gz']].bfill(axis=1).iloc[:,0]
    target = df[['invoice_id','status']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['invoice_id','payment_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_invoices = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_payments = prepared_table_2

merged = prepared_invoices.merge(prepared_payments, on='invoice_id', how='left'); no_pay = merged[merged['payment_id'].isna()][['invoice_id','status']]; target = no_pay

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
