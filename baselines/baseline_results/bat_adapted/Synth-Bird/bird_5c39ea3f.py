import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time
    df = df[(df['Date'] == pd.to_datetime('2012-08-26').date()) & (df['Time'] < pd.to_datetime('12:00:00').time())]
    target = df[['TransactionID','Date','Time','CustomerID','CardID','GasStationID','ProductID','Amount','Price']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.drop(columns=[table_1.columns[0]])
    long_df = df.melt(var_name='Currency', value_name='CustomerID_Segment')
    long_df['CustomerID'] = long_df['CustomerID_Segment'].astype(str).str.extract(r'^(\d+)')[0]
    long_df = long_df.dropna(subset=['CustomerID'])
    long_df['CustomerID'] = long_df['CustomerID'].astype(int)
    target = long_df[['CustomerID','Currency']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_customer_currency = prepared_table_2

# prepared_transactions: assumed already selected columns from table_1
# prepared_customer_currency: constructed by unpivoting table_2

# Example construction for prepared_customer_currency from original table_2 (wide one-row frame) if needed:
# cols = [c for c in table_2.columns if c != 'Currency']
# records = []
# for c in cols:
#     val = table_2.iloc[0][c]
#     if pd.notna(val) and isinstance(val, str) and '-' in val:
#         cust_id_str = val.split('-', 1)[0]
#         if cust_id_str.isdigit():
#             records.append({'CustomerID': int(cust_id_str), 'Currency': str(c)})
# prepared_customer_currency = pd.DataFrame(records)

# Integrate on CustomerID
trx_with_curr = prepared_transactions.merge(prepared_customer_currency, on='CustomerID', how='left')

# Filter by date and morning time (00:00:00 to 11:59:59) and CZK currency
# Normalize date formats to yyyy-mm-dd
trx_with_curr['Date_norm'] = pd.to_datetime(trx_with_curr['Date']).dt.date
trx_with_curr['Time_norm'] = pd.to_datetime(trx_with_curr['Time'], format='%H:%M:%S', errors='coerce').dt.time

is_target_date = trx_with_curr['Date_norm'] == pd.to_datetime('2012-08-26').date()
# Morning defined as hour < 12
hour_series = pd.to_datetime(trx_with_curr['Time'], format='%H:%M:%S', errors='coerce').dt.hour
is_morning = hour_series.ge(0) & hour_series.lt(12)

is_czk = trx_with_curr['Currency'] == 'CZK'

answer = int(trx_with_curr[is_target_date & is_morning & is_czk].shape[0])

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
