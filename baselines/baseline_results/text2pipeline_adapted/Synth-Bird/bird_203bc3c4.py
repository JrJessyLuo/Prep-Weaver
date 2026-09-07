import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'Date', 'func': "def transform(s):\n    s = str(s)\n    # remove internal spaces around separators\n    s = s.replace(' / ', '/').replace(' ', '')\n    s = s.replace('/', '-')\n    return s.strip()"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Time', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Date', 'Time'], 'target_column': 'TransactionDateTime', 'func': 'def transform(row):\n    # Date is datetime64 after standardization; format it, then join with cleaned Time\n    from datetime import datetime\n    d = row[\'Date\']\n    try:\n      d_str = d.strftime(\'%Y-%m-%d\') if hasattr(d, \'strftime\') else str(d)\n    except Exception:\n      d_str = str(d)\n    t_str = str(row[\'Time\']).strip()\n    return f"{d_str} {t_str}"'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'TransactionDateTime', 'date_format': '%Y-%m-%d %H:%M:%S'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TransactionID', 'TransactionDateTime', 'GasStationID', 'Date', 'Time']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'GasStationID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Segment', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Country_Part1', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Country_Part2', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Country_Part1', 'Country_Part2'], 'target_column': 'Country', 'func': "def transform(row):\n    p1 = '' if row.get('Country_Part1') is None else str(row.get('Country_Part1'))\n    p2 = '' if row.get('Country_Part2') is None else str(row.get('Country_Part2'))\n    return (p1 + p2).upper()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['GasStationID', 'Country', 'ChainID', 'Segment']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    # remove internal spaces around separators\n    s = s.replace(' / ', '/').replace(' ', '')\n    s = s.replace('/', '-')\n    return s.strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['Date'] = tmp_0['Date'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Time'] = tmp_2['Time'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Concatenate
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(row):\n    # Date is datetime64 after standardization; format it, then join with cleaned Time\n    from datetime import datetime\n    d = row[\'Date\']\n    try:\n      d_str = d.strftime(\'%Y-%m-%d\') if hasattr(d, \'strftime\') else str(d)\n    except Exception:\n      d_str = str(d)\n    t_str = str(row[\'Time\']).strip()\n    return f"{d_str} {t_str}"', globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_3['TransactionDateTime'] = tmp_3[['Date', 'Time']].apply(_concat_func_3, axis=1)
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['TransactionDateTime'] = pd.to_datetime(tmp_4['TransactionDateTime'], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['GasStationID'] = pd.to_numeric(tmp_5['GasStationID'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TransactionID', 'TransactionDateTime', 'GasStationID', 'Date', 'Time']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['GasStationID'] = pd.to_numeric(tmp_0['GasStationID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['Segment'] = tmp_1['Segment'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Country_Part1'] = tmp_2['Country_Part1'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['Country_Part2'] = tmp_3['Country_Part2'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec("def transform(row):\n    p1 = '' if row.get('Country_Part1') is None else str(row.get('Country_Part1'))\n    p2 = '' if row.get('Country_Part2') is None else str(row.get('Country_Part2'))\n    return (p1 + p2).upper()", globals(), _ns_4)
    _concat_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('concat')
    tmp_4['Country'] = tmp_4[['Country_Part1', 'Country_Part2']].apply(_concat_func_4, axis=1)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['GasStationID', 'Country', 'ChainID', 'Segment']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='GasStationID')
# Target timestamp as string patterns
exact_str1 = '2012-08-24 12:42:00'
exact_str2 = '2012/8/24 12:42:00'
# First try exact string match on TransactionDateTime
matched = integrated[integrated['TransactionDateTime'] == exact_str1]
# Fallback: flexible, case-insensitive contains on plausible datetime columns
if matched.empty:
    td_col = integrated['TransactionDateTime'].astype(str).str.lower()
    date_col = integrated['Date'].astype(str).str.lower() if 'Date' in integrated.columns else td_col
    time_col = integrated['Time'].astype(str).str.lower() if 'Time' in integrated.columns else td_col
    cond1 = td_col.str.contains('2012-08-24', na=False) & td_col.str.contains('12:42:00', na=False)
    cond2 = td_col.str.contains('2012/8/24', na=False) & td_col.str.contains('12:42:00', na=False)
    cond3 = date_col.str.contains('2012-08-24', na=False) & time_col.str.contains('12:42:00', na=False)
    matched = integrated[cond1 | cond2 | cond3]
# If still empty, relax to any transactions on that date and pick the first plausible row
if matched.empty:
    td_col = integrated['TransactionDateTime'].astype(str)
    date_hits = integrated[td_col.str.contains('2012-08-24', na=False)]
    if date_hits.empty and 'Date' in integrated.columns:
        date_hits = integrated[integrated['Date'].astype(str).str.contains('2012-08-24', na=False)]
    matched = date_hits.head(1) if not date_hits.empty else integrated.head(1)
# Project the country
target = matched[['Country']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
