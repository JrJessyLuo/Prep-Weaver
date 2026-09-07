import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['Receipt','Ordinal','Item']].copy()
    target['Receipt'] = pd.to_numeric(target['Receipt'], errors='coerce').astype('Int64')
    target['Ordinal'] = pd.to_numeric(target['Ordinal'], errors='coerce').astype('Int64')
    target['Item'] = target['Item'].astype('string')
    target['Item'] = target['Item'].str.replace(r'[\u2010\u2011\u2012\u2013\u2014\u2212]', '-', regex=True)
    target['Item'] = target['Item'].str.replace(r'\s*-\s*', '-', regex=True)
    target['Item'] = target['Item'].str.replace(r'\s+', ' ', regex=True).str.strip()
    target = target.dropna(subset=['Receipt','Ordinal','Item'])
    target = target.drop_duplicates(subset=['Receipt','Ordinal','Item']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['sjb','khid']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_receipt_items = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sales_headers = prepared_table_2

target = prepared_sales_headers.merge(prepared_receipt_items, left_on='sjb', right_on='Receipt', how='inner')
# Filter for the requested customer id
customer_items = target[target['khid'] == 15]
# Get distinct items bought by this customer
answer = sorted(customer_items['Item'].dropna().unique().tolist())

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
