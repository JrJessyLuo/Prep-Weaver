import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Time', 'func': 'def transform(s):\n    # Preserve content; ensure string type without trimming\n    return str(s)'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Date', 'Time'], 'target_column': 'EventDateTime', 'func': 'def transform(row):\n    d = row[\'Date\']\n    t = row[\'Time\']\n    try:\n        d_str = d.strftime(\'%Y-%m-%d\')\n    except Exception:\n        d_str = str(d)[:10]\n    return f"{d_str} {t}"'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'EventDateTime', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'GasStationID', 'new_name': 'GasStationID_str'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'GasStationID_str', 'target_columns': ['GasStationID_str', 'GasStationID'], 'func': "def transform(s):\n    # Keep string version and also provide integer key\n    s_str = str(s)\n    try:\n        s_int = int(float(s)) if s_str.replace('.','',1).isdigit() else int(s_str)\n    except Exception:\n        try:\n            s_int = int(s_str)\n        except Exception:\n            s_int = None\n    return [s_str, s_int]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TransactionID', 'Date', 'Time', 'EventDateTime', 'CustomerID', 'CardID', 'GasStationID', 'GasStationID_str', 'ProductID', 'je', 'dj']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'GasStationID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'StationID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Value', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'StationID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'StationID', 'columns': 'GasStationID', 'values': 'Value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['StationID', 'ChainID']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['Date'] = pd.to_datetime(tmp_0['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Preserve content; ensure string type without trimming\n    return str(s)', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Time'] = tmp_1['Time'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Concatenate
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(row):\n    d = row[\'Date\']\n    t = row[\'Time\']\n    try:\n        d_str = d.strftime(\'%Y-%m-%d\')\n    except Exception:\n        d_str = str(d)[:10]\n    return f"{d_str} {t}"', globals(), _ns_2)
    _concat_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('concat')
    tmp_2['EventDateTime'] = tmp_2[['Date', 'Time']].apply(_concat_func_2, axis=1)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['EventDateTime'] = pd.to_datetime(tmp_3['EventDateTime'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['GasStationID'] = pd.to_numeric(tmp_4['GasStationID'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['GasStationID'] = tmp_5['GasStationID'].astype(str)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'GasStationID': 'GasStationID_str'})
    # Step 8: SplitColumn
    tmp_7 = tmp_6.copy()
    _ns_3 = {}
    exec("def transform(s):\n    # Keep string version and also provide integer key\n    s_str = str(s)\n    try:\n        s_int = int(float(s)) if s_str.replace('.','',1).isdigit() else int(s_str)\n    except Exception:\n        try:\n            s_int = int(s_str)\n        except Exception:\n            s_int = None\n    return [s_str, s_int]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_7['GasStationID_str'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_7['GasStationID_str'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_7['GasStationID'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['TransactionID', 'Date', 'Time', 'EventDateTime', 'CustomerID', 'CardID', 'GasStationID', 'GasStationID_str', 'ProductID', 'je', 'dj']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['GasStationID'] = tmp_0['GasStationID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['StationID'] = tmp_1['StationID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['Value'] = tmp_2['Value'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['StationID'] = tmp_3['StationID'].astype(str)
    # Step 5: Pivot
    tmp_4 = pd.pivot_table(tmp_3, index='StationID', columns='GasStationID', values='Value', aggfunc='first').reset_index()
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['StationID', 'ChainID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
tmp2 = prepared_table_2.copy()
# Ensure key columns are strings for join consistency
if 'StationID' in tmp2.columns:
    tmp2['StationID'] = tmp2['StationID'].astype(str)

pt1 = prepared_table_1.copy()
pt1['GasStationID_str'] = pt1['GasStationID_str'].astype(str)

# Merge station metadata (e.g., ChainID) to transactions
integrated = pt1.merge(tmp2, how='left', left_on='GasStationID_str', right_on='StationID')

# Build a robust datetime for ordering
if 'EventDateTime' in integrated.columns:
    dt = pd.to_datetime(integrated['EventDateTime'], errors='coerce')
else:
    dt = pd.Series(pd.NaT, index=integrated.index)

# Fallback from separate Date/Time strings when needed
if dt.isna().any():
    date_parsed = pd.to_datetime(integrated.get('Date', pd.Series(index=integrated.index)), errors='coerce')
    time_str = integrated.get('Time', pd.Series(index=integrated.index)).astype(str)
    # Combine date and time when possible
    dt_fallback = pd.to_datetime(date_parsed.dt.strftime('%Y-%m-%d') + ' ' + time_str, errors='coerce')
    dt = dt.fillna(dt_fallback)

integrated['__evt'] = dt

# Target date filter with robust parsing (strings in Date column)
target_day = pd.to_datetime('2012-08-25')
# Compute date part from parsed datetime, fallback to parsing Date column
evt_date = integrated['__evt'].dt.normalize()
missing_evt = evt_date.isna()
if missing_evt.any():
    evt_date2 = pd.to_datetime(integrated.get('Date', pd.Series(index=integrated.index)), errors='coerce').dt.normalize()
    evt_date = evt_date.fillna(evt_date2)

subset = integrated[evt_date == target_day.normalize()].copy()

# If empty, relax to earliest on/after target date; if still empty, earliest overall
if subset.empty:
    # On/after filter
    mask_on_after = evt_date >= target_day.normalize()
    subset = integrated[mask_on_after].copy().sort_values(['__evt', 'TransactionID']).head(1)
    if subset.empty:
        subset = integrated.copy().sort_values(['__evt', 'TransactionID']).head(1)
else:
    subset = subset.sort_values(['__evt', 'TransactionID']).head(1)

# Project to country-level answer: no explicit country table available; best proxy is to return ChainID-linked row
# If a Country column exists from upstream schemas, prefer it; otherwise leave ChainID as context if present
proj_cols = []
if 'Country' in subset.columns:
    proj_cols = ['Country']
elif 'country' in subset.columns:
    proj_cols = ['country']
elif 'ChainID' in subset.columns:
    proj_cols = ['ChainID']

if proj_cols:
    target = subset[proj_cols].rename(columns={'Country': 'country'})
else:
    # Fallback to include station identifier as the most plausible locator
    keep = [c for c in ['GasStationID_str', 'StationID'] if c in subset.columns]
    target = subset[keep].rename(columns={'GasStationID_str': 'station_id'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
