import pandas as pd
import numpy as np

def _prep_1(table_1):
    items_long = table_1.melt(id_vars=['Receipt'], value_vars=[1, 2, 3, 4, 5], var_name='pos', value_name='item')
    items_long['item'] = items_long['item'].astype('string')
    items_long['item'] = items_long['item'].where(~items_long['item'].isin(['nan', 'NaN', '<NA>']), pd.NA)
    items_long = items_long.dropna(subset=['item'])
    items_long = items_long.sort_values(['Receipt', 'pos'])
    items_long['rn'] = items_long.groupby('Receipt').cumcount() + 1
    items_long = items_long[items_long['rn'].between(1, 5)]
    target = items_long.pivot(index='Receipt', columns='rn', values='item').reindex(columns=[1, 2, 3, 4, 5]).reset_index()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df_long = table_1.melt(id_vars=['ReceiptNumber'], var_name='ReceiptNumber_melt', value_name='value')
    df_long['ReceiptNumber_melt'] = df_long['ReceiptNumber_melt'].astype(str)
    df_pivot = df_long.pivot(index='ReceiptNumber_melt', columns='ReceiptNumber', values='value').reset_index()
    df_pivot = df_pivot.rename(columns={'ReceiptNumber_melt': 'ReceiptNumber'})
    df_pivot['ReceiptNumber'] = pd.to_numeric(df_pivot['ReceiptNumber'], errors='coerce').astype('Int64')
    df_pivot['CustomerId'] = pd.to_numeric(df_pivot['CustomerId'], errors='coerce').astype('Int64')
    df_pivot['Date'] = pd.to_datetime(df_pivot['Date'], errors='coerce', dayfirst=True)
    target = df_pivot[['ReceiptNumber', 'Date', 'CustomerId']].sort_values('ReceiptNumber').reset_index(drop=True)
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_items = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_receipts = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])

# prepared_items: columns ['Receipt','1','2','3','4','5']
# prepared_receipts: rows like (ReceiptNumber, Date, CustomerId)

# Integrate on receipt number
joined = prepared_items.merge(prepared_receipts, left_on='Receipt', right_on='ReceiptNumber', how='outer')

# Detect whether any of the item columns indicates an apple flavor pie.
# Heuristic: match codes containing 'APIE' or 'APPLE' (case-insensitive) in any item column.
item_cols = ['1','2','3','4','5']
for c in item_cols:
    if c not in joined.columns:
        joined[c] = pd.NA

def has_apple_pie(row):
    for c in item_cols:
        v = row[c]
        if pd.isna(v):
            continue
        s = str(v).upper()
        if ('APIE' in s) or ('APPLE' in s):
            return True
    return False

joined['apple_pie_flag'] = joined.apply(has_apple_pie, axis=1)

# Flag receipts for customer id 12
joined['cust12_flag'] = (joined['CustomerId'].astype(str) == '12')

# Select receipts satisfying either condition
result_receipts = joined.loc[(joined['apple_pie_flag']) | (joined['cust12_flag']), 'Receipt'].dropna().astype(int).drop_duplicates().sort_values()

answer = result_receipts.tolist()

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
