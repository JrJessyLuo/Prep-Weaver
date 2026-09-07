import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Headphone_ID','Model']].drop_duplicates(subset=['Headphone_ID']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['Quantity'] = df['Quantity'].astype(str).str.replace('"', '', regex=False).str.strip()
    df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce').astype('Int64')
    target = df[['Headphone_ID', 'Store_ID', 'Quantity']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_headphones = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_inventory = prepared_table_2

# prepared_headphones and prepared_inventory are the synthesized per-table outputs
# Ensure numeric quantity for stock checks
inv = prepared_inventory.copy()
if 'Quantity' in inv.columns:
    inv['Quantity_num'] = pd.to_numeric(inv['Quantity'].astype(str).str.replace('"',''), errors='coerce').fillna(0)
else:
    inv['Quantity_num'] = 0

# Aggregate to know which Headphone_ID has any stock across stores
inv_any_stock = (
    inv.groupby('Headphone_ID', as_index=False)['Quantity_num']
       .sum()
       .rename(columns={'Quantity_num': 'total_qty'})
)

# Left-join headphones to aggregated inventory
merged = prepared_headphones.merge(inv_any_stock, on='Headphone_ID', how='left')

# Models not in stock in any store: total_qty is NaN or 0
result = merged.loc[merged['total_qty'].fillna(0) <= 0, ['Model']].drop_duplicates().reset_index(drop=True)

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
