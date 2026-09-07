import pandas as pd
import numpy as np

def _prep_1(table_1):
    name_rows = table_1[table_1['attribute'].eq('Name')].copy()
    name_rows = name_rows[['IdClient','details']].rename(columns={'details':'Name'})
    target = name_rows.drop_duplicates(subset=['IdClient'])[['IdClient','Name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['IdOrder','IdClient']].copy()
    df['IdClient_clean'] = df['IdClient'].astype(str).str.strip('"')
    target = df[['IdOrder','IdClient_clean']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['IdOrder_num','IdOrder_suffix','amount']].copy()
    df['IdOrder'] = df['IdOrder_num'].astype(str) + df['IdOrder_suffix'].astype(str)
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    target = df[['IdOrder','amount']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
clients_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
orders_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
order_lines_prepared = prepared_table_3

# Assume input DataFrames: table_1, table_2, table_3

# Prepare clients: select Name attribute and cast IdClient to string for consistent joins
clients_prepared = (
    table_1.loc[table_1['attribute'] == 'Name', ['IdClient', 'details']]
           .rename(columns={'details': 'Name'})
)
clients_prepared['IdClient'] = clients_prepared['IdClient'].astype(str).str.strip()

# Prepare orders: clean IdClient and keep IdOrder
orders_prepared = table_2[['IdOrder', 'IdClient']].copy()
orders_prepared['IdOrder'] = orders_prepared['IdOrder'].astype(str).str.strip()
orders_prepared['IdClient_clean'] = (
    orders_prepared['IdClient'].astype(str).str.strip().str.replace('^\"|\"$', '', regex=True)
)
orders_prepared = orders_prepared[['IdOrder', 'IdClient_clean']]

# Prepare order lines: compose IdOrder and coerce amount numeric
order_lines_prepared = table_3[['IdOrder_num', 'IdOrder_suffix', 'amount']].copy()
order_lines_prepared['IdOrder'] = order_lines_prepared['IdOrder_num'].astype(str) + order_lines_prepared['IdOrder_suffix'].astype(str)
order_lines_prepared['IdOrder'] = order_lines_prepared['IdOrder'].str.strip()
order_lines_prepared['amount'] = pd.to_numeric(order_lines_prepared['amount'], errors='coerce').fillna(0).astype(int)
order_lines_prepared = order_lines_prepared[['IdOrder', 'amount']]

# Integration: lines -> orders -> clients
lines_orders = order_lines_prepared.merge(orders_prepared, on='IdOrder', how='inner')
full = lines_orders.merge(clients_prepared, left_on='IdClient_clean', right_on='IdClient', how='inner')

# Aggregate total amounts of books per client name
answer = (full.groupby('Name', as_index=False)['amount'].sum()
               .rename(columns={'amount': 'total_books_ordered'}))

target = answer

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
