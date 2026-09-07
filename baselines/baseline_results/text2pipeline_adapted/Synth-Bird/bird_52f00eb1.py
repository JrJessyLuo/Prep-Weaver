import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Time', 'date_format': '%H:%M:%S'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Amount', 'func': 'def transform(s):\n    s = \'\' if s is None else str(s)\n    if s.startswith(\'"\') and s.endswith(\'"\'):\n        return s[1:-1].strip()\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TransactionID', 'Date', 'Time', 'GasStationID']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['GasStationID', 'CZE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['Date'] = pd.to_datetime(tmp_0['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Time'] = pd.to_datetime(tmp_1['Time'], errors='coerce').dt.strftime('%H:%M:%S')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['GasStationID'] = pd.to_numeric(tmp_2['GasStationID'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = \'\' if s is None else str(s)\n    if s.startswith(\'"\') and s.endswith(\'"\'):\n        return s[1:-1].strip()\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['Amount'] = tmp_3['Amount'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['TransactionID', 'Date', 'Time', 'GasStationID']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['GasStationID'] = pd.to_numeric(tmp_0['GasStationID'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['GasStationID', 'CZE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='GasStationID')
# Filter date 2012-08-26 and time between 08:00:00 (inclusive) and 09:00:00 (exclusive)
# Ensure Time is comparable as time; prepared_table_1 already standardized times
mask_date = (integrated['Date'] == pd.to_datetime('2012-08-26').date())
# Convert to datetime.time if needed
if integrated['Time'].dtype == 'object':
    tseries = pd.to_datetime(integrated['Time'], errors='coerce').dt.time
else:
    tseries = integrated['Time']
start_t = pd.to_datetime('08:00:00').time()
end_t = pd.to_datetime('09:00:00').time()
mask_time = tseries >= start_t
mask_time &= tseries < end_t
# CZE stations: CZE column present and not null/empty
mask_cze = integrated['CZE'].notna() & (integrated['CZE'].astype(str).str.len() > 0)
result = integrated.loc[mask_date & mask_time & mask_cze]
count_df = pd.DataFrame({'count_in_CZE_8to9_on_2012_08_26': [len(result)]})
target = count_df

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
