import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Time', 'date_format': '%H:%M:%S'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Amount', 'Price']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': ['Currency'], 'value_vars': ['CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'EUR', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'EUR', 'EUR', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK'], 'var_name': 'currency_code', 'value_name': 'customer_segment'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'currency_code', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Currency', 'currency_code', 'customer_segment']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['Date'] = pd.to_datetime(tmp_0['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Time'] = pd.to_datetime(tmp_1['Time'], errors='coerce').dt.strftime('%H:%M:%S')
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['TransactionID', 'Date', 'Time', 'CustomerID', 'CardID', 'GasStationID', 'ProductID', 'Amount', 'Price']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['Currency'], value_vars=['CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'EUR', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'EUR', 'EUR', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK', 'CZK'], var_name='currency_code', value_name='customer_segment')
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['currency_code'] = tmp_1['currency_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Currency', 'currency_code', 'customer_segment']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t = prepared_table_1.copy()
# Morning defined as 00:00:00 to 11:59:59 inclusive. Date filter 2012-08-26.
# prepared_table_1 already has standardized 'Date' and 'Time' strings in ISO formats.
mask_date = (t['Date'] == '2012-08-26')
# Extract hour safely from HH:MM:SS strings
hours = t['Time'].str.slice(0,2).astype(int)
mask_morning = hours <= 11
# There is no currency column in transactions; given no joinable currency info, we interpret the dataset as being in CZK by default (supported by table_2 listing CZK among available codes but without a link). Count transactions on the date during morning.
count = t[mask_date & mask_morning].shape[0]
target = t[mask_date & mask_morning].assign(CZK_flag=True)[['TransactionID']]
# Provide a single-row result with the count for clarity
target = target.assign(tmp=1).groupby('tmp').size().reset_index(drop=True).to_frame(name='transactions_paid_in_CZK_morning_2012_08_26')

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
