import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Store_ID','Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['Quantity'] = df['Quantity'].astype(str).str.replace('"', '', regex=False).str.strip()
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    target = df[['Store_ID', 'Headphone_ID', 'Quantity']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
stores = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
store_headphone_stock = prepared_table_2

# Assume prepared tables are dataframes: stores, store_headphone_stock
# Normalize Quantity to numeric (handles quotes) and aggregate per store
inv = store_headphone_stock.copy()
inv['Quantity'] = pd.to_numeric(inv['Quantity'], errors='coerce').fillna(0)
# A store has any headphones if total quantity across headphone SKUs > 0
has_hp = inv.groupby('Store_ID', as_index=False)['Quantity'].sum().rename(columns={'Quantity':'Total_HP_Qty'})

# Left-join stores to headphone availability
merged = stores.merge(has_hp, on='Store_ID', how='left')

# Stores with no headphone rows or zero total quantity
no_hp = merged[(merged['Total_HP_Qty'].isna()) | (merged['Total_HP_Qty'] <= 0)]

# Final answer: store names
answer = no_hp[['Name']].drop_duplicates().sort_values('Name')

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
