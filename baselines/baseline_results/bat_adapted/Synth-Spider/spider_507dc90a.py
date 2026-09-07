import pandas as pd
import numpy as np

def _prep_1(table_1):
    names_row = table_1.loc[table_1['IdClient'].eq('Name')]
    long = names_row.melt(id_vars=['IdClient'], var_name='IdClient', value_name='Name')
    target = long[['IdClient','Name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['IdOrder','KH']].rename(columns={'KH':'IdClient'})
    target = prepared.groupby('IdOrder', as_index=False).agg({'IdClient':'first'})[['IdOrder','IdClient']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['IdOrder']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_clients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_orders = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_order_lines = prepared_table_3

# prepared_clients columns: IdClient (as string or int consistent with prepared_orders), Name
# prepared_orders columns: IdOrder, IdClient
# prepared_order_lines columns: IdOrder

# Optionally validate orders have at least one line; if not needed, skip this block
orders_with_lines = prepared_orders.merge(prepared_order_lines[['IdOrder']].drop_duplicates(), on='IdOrder', how='inner')

# Count orders per client
order_counts = orders_with_lines.groupby('IdClient', as_index=False).agg(OrderCount=('IdOrder', 'nunique'))

# Join client names
result = prepared_clients.merge(order_counts, on='IdClient', how='left')
result['OrderCount'] = result['OrderCount'].fillna(0).astype(int)

# Final projection: client name and number of orders
answer = result[['Name', 'OrderCount']]

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
