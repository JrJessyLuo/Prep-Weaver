import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['product_id','product_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df_long = df.melt(id_vars=['order_item_id'], var_name='col_id', value_name='value')
    df_wide = df_long.pivot(index='col_id', columns='order_item_id', values='value').reset_index(drop=True)
    target = df_wide[['order_id','product_id']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
products = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_table_3 = _prep_3(tables['table_2'])
order_items_long = prepared_table_3

# Assume products is already the selected columns from table_1
# For table_3, unpivot to long format using the first row as order_id values and second row as product_id values

def prepare_order_items_long(table_3):
    # table_3 has rows labeled by 'order_item_id' with subsequent columns 1..N holding values
    # Extract rows
    row_map = {r['order_item_id']: r for _, r in table_3.iterrows()}
    # Collect numeric column labels (as strings in DataFrame)
    value_cols = [c for c in table_3.columns if c != 'order_item_id']
    order_ids = [row_map['order_id'][c] for c in value_cols]
    product_ids = [row_map['product_id'][c] for c in value_cols]
    df = pd.DataFrame({'order_id': order_ids, 'product_id': product_ids})
    # Ensure dtypes are numeric where possible
    df['order_id'] = pd.to_numeric(df['order_id'], errors='coerce')
    df['product_id'] = pd.to_numeric(df['product_id'], errors='coerce')
    # Drop any rows with missing ids
    df = df.dropna(subset=['product_id'])
    return df

# prepared tables available as variables: products (cols: product_id, product_name) and table_3
order_items_long = prepare_order_items_long(table_3)

# Left-anti join: products without any matching order_items
ordered_products = order_items_long[['product_id']].drop_duplicates()
result = products.merge(ordered_products, on='product_id', how='left', indicator=True)
result = result[result['_merge'] == 'left_only']

# Final projection: product names without an order
answer = result[['product_name']].drop_duplicates().reset_index(drop=True)

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
