import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['TransactionID','CustomerID','ProductID','Price']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['ProductID'] = df['ProductID'].astype(str).str.strip().str.strip('"')
    df['Description'] = df['Description'].astype(str)
    df = df[['ProductID','Description']].drop_duplicates(subset=['ProductID'], keep='first')
    target = df[['ProductID','Description']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['CustomerID','huobi']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_products = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_customers = prepared_table_3

target = prepared_transactions.merge(prepared_customers, on='CustomerID', how='left').merge(prepared_products, on='ProductID', how='left')
# filter transactions where customer currency is EUR (euro)
result = target[target['huobi'].str.upper().eq('EUR')]['Description'].dropna().drop_duplicates().sort_values()

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
