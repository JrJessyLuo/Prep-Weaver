import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['TransactionID','Date','Time','GasStationID']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    prepared['Time'] = pd.to_datetime(prepared['Time'], format='%H:%M:%S', errors='coerce').dt.time
    target = prepared[['TransactionID','Date','Time','GasStationID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['GasStationID', 'CZE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_stations = prepared_table_2

# Assume prepared_transactions and prepared_stations are dataframes synthesized per targets
merged = prepared_transactions.merge(prepared_stations, on='GasStationID', how='left')

# Normalize date/time
merged['Date'] = pd.to_datetime(merged['Date'], errors='coerce')
merged['Time'] = pd.to_datetime(merged['Time'], format='%H:%M:%S', errors='coerce').dt.time

# Build a datetime for filtering hour range
merged['DateTime'] = pd.to_datetime(merged['Date'].dt.date.astype(str) + ' ' + merged['Time'].astype(str), errors='coerce')

start = pd.Timestamp('2012-08-26 08:00:00')
end = pd.Timestamp('2012-08-26 09:00:00')

# Filter for 2012-08-26 between 08:00:00 (inclusive) and 09:00:00 (exclusive)
mask_time = (merged['DateTime'] >= start) & (merged['DateTime'] < end)

# Identify CZE transactions: depending on data, treat non-null/non-empty and not 'nan' as in CZE
# If CZE is a categorical/flag column, select rows where CZE is not null; adjust if a specific value denotes CZE
mask_cze = merged['CZE'].notna()

answer = merged.loc[mask_time & mask_cze].shape[0]

result = answer

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
