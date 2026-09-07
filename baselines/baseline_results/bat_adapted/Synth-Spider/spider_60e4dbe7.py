import pandas as pd
import numpy as np

def _prep_1(table_1):
    import ast
    df = table_1.copy()
    list_cols = ['product_id','parent_product_id','product_name','product_price','product_size','product_description']
    df[list_cols] = df[list_cols].applymap(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    df = df.explode(list_cols, ignore_index=True)
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce').astype('Int64')
    df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce')
    target = df[['product_id','product_name','product_price','product_color']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['product_id','order_item_id','order_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
products_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
order_items_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])

# Assume products_prepared and order_items_prepared are the synthesized tables
# Count order items per product
order_counts = order_items_prepared.groupby('product_id', dropna=False)['order_item_id'].nunique().reset_index(name='order_item_count')

# Left join counts to products
prod_with_counts = products_prepared.merge(order_counts, on='product_id', how='left')
prod_with_counts['order_item_count'] = prod_with_counts['order_item_count'].fillna(0)

# Filter products listed in less than two orders (interpreted as fewer than 2 order line items)
filtered = prod_with_counts[prod_with_counts['order_item_count'] < 2]

# Select required columns
answer = filtered[['product_id', 'product_name', 'product_price', 'product_color']]

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
