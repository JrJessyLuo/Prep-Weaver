import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['TransactionID','Date','Time','GasStationID']].copy()
    df['Date'] = pd.to_datetime(df['Date'].astype(str).str.replace(' / ', '-', regex=False).str.replace('/', '-', regex=False).str.strip(), errors='coerce').dt.strftime('%Y-%m-%d')
    df['Time'] = pd.to_datetime(df['Time'].astype(str).str.strip(), format='%H:%M:%S', errors='coerce').dt.strftime('%H:%M:%S')
    target = df[['TransactionID','Date','Time','GasStationID']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['GasStationID','Country_Part1','Country_Part2']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_transactions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_stations = prepared_table_2

# Assume prepared_transactions has Date and Time normalized to strings like '2012-08-24' and '12:42:00'
# and prepared_stations has country parts as given.

target = prepared_transactions.merge(prepared_stations, on='GasStationID', how='left')

# Normalize possible Date formats in source (e.g., '2012 / 08 / 24' -> '2012-08-24') if not already done
# Here we defensively parse to datetime and back to date string for filtering
parsed_dt = pd.to_datetime(target['Date'].astype(str).str.replace(' / ', '-', regex=False), errors='coerce')
target['Date_norm'] = parsed_dt.dt.strftime('%Y-%m-%d')

# Filter to the specific deal datetime
mask = (target['Date_norm'] == '2012-08-24') & (target['Time'].astype(str) == '12:42:00')
filtered = target.loc[mask].copy()

# Compose country from parts (e.g., 'CZ' + 'E' -> 'CZE')
filtered['Country'] = (filtered['Country_Part1'].fillna('') + filtered['Country_Part2'].fillna('')).str.strip()

# Select the country for the matching deal(s)
answer = filtered[['TransactionID', 'Country']]

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
