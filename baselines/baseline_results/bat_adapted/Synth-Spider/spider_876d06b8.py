import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['ISBN','Title']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    parts = df['ISBN_amount'].astype(str).str.rsplit('-', n=1, expand=True)
    df['ISBN'] = parts[0]
    df['Quantity'] = pd.to_numeric(parts[1], errors='coerce')
    target = df[['IdOrder', 'ISBN', 'Quantity']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['IdOrder']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
books = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
order_lines = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
orders = prepared_table_3

# Assume prepared tables exist: books, order_lines, orders
# order_lines has ISBN and Quantity parsed from ISBN_amount (e.g., '8233771378567-1')

ol_books = order_lines.merge(books, on='ISBN', how='inner')
# Optional join to orders (kept to honor integration plan; not strictly needed for the count)
ol_full = ol_books.merge(orders, on='IdOrder', how='left')

# Filter for the target title and sum quantities
answer = int(ol_full.loc[ol_full['Title'].str.strip().str.lower() == 'pride and prejudice', 'Quantity'].sum())
result = pd.DataFrame({'number_of_orders_received_for_pride_and_prejudice': [answer]})

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
