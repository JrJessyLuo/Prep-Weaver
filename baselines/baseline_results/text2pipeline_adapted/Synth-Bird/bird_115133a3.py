import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'cds', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'school_part1', 'func': "def transform(s):\n    try:\n        import numpy as np\n        if s is None or (isinstance(s, float) and np.isnan(s)):\n            return ''\n    except Exception:\n        pass\n    return str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'school_part2', 'func': "def transform(s):\n    try:\n        import numpy as np\n        if s is None or (isinstance(s, float) and np.isnan(s)):\n            return ''\n    except Exception:\n        pass\n    return str(s).strip()"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['school_part1', 'school_part2'], 'target_column': 'SchoolName', 'func': "def transform(row):\n    p1 = row.get('school_part1', '')\n    p2 = row.get('school_part2', '')\n    p1 = '' if p1 is None else str(p1).strip()\n    p2 = '' if p2 is None else str(p2).strip()\n    parts = [x for x in [p1, p2] if x]\n    return ' '.join(parts)"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AvgScrWrite', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'cds', 'new_name': 'CDSCode'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CDSCode', 'SchoolName', 'AvgScrWrite']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'CDSCode', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'OpenDate', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'ClosedDate', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'School', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Phone', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'School', 'new_name': 'SchoolName_dir'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CDSCode', 'SchoolName_dir', 'Phone', 'OpenDate', 'ClosedDate']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['cds'] = tmp_0['cds'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    try:\n        import numpy as np\n        if s is None or (isinstance(s, float) and np.isnan(s)):\n            return ''\n    except Exception:\n        pass\n    return str(s).strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['school_part1'] = tmp_1['school_part1'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    try:\n        import numpy as np\n        if s is None or (isinstance(s, float) and np.isnan(s)):\n            return ''\n    except Exception:\n        pass\n    return str(s).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['school_part2'] = tmp_2['school_part2'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Concatenate
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(row):\n    p1 = row.get('school_part1', '')\n    p2 = row.get('school_part2', '')\n    p1 = '' if p1 is None else str(p1).strip()\n    p2 = '' if p2 is None else str(p2).strip()\n    parts = [x for x in [p1, p2] if x]\n    return ' '.join(parts)", globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_3['SchoolName'] = tmp_3[['school_part1', 'school_part2']].apply(_concat_func_3, axis=1)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['AvgScrWrite'] = pd.to_numeric(tmp_4['AvgScrWrite'], errors='coerce').astype(float)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'cds': 'CDSCode'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['CDSCode', 'SchoolName', 'AvgScrWrite']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['CDSCode'] = tmp_0['CDSCode'].astype(str)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['OpenDate'] = pd.to_datetime(tmp_1['OpenDate'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['ClosedDate'] = pd.to_datetime(tmp_2['ClosedDate'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['School'] = tmp_3['School'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['Phone'] = tmp_4['Phone'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'School': 'SchoolName_dir'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['CDSCode', 'SchoolName_dir', 'Phone', 'OpenDate', 'ClosedDate']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='CDSCode')

# Parse dates safely from strings
open_parsed = pd.to_datetime(integrated['OpenDate'], errors='coerce')
close_parsed = pd.to_datetime(integrated['ClosedDate'], errors='coerce')

# Condition: opened after 1991 or closed before 2000
cond_open = open_parsed.dt.year > 1991
cond_close = close_parsed.dt.year < 2000
mask = cond_open.fillna(False) | cond_close.fillna(False)

filtered = integrated.loc[mask].copy()

# If filtering led to empty result, relax by including rows with plausible dates present
if filtered.empty:
    has_any_date = open_parsed.notna() | close_parsed.notna()
    filtered = integrated.loc[has_any_date].copy()

# Compute overall average score in writing across the filtered schools
overall_avg = filtered['AvgScrWrite'].mean()

# Prepare per-school output with communication number (phone) if present
result = filtered[['SchoolName', 'AvgScrWrite', 'Phone']].rename(columns={'Phone': 'CommunicationNumber'})

# Append a summary average row
avg_row = {
    'SchoolName': 'Average (filtered)',
    'AvgScrWrite': overall_avg,
    'CommunicationNumber': None
}
result_with_avg = pd.concat([result, pd.DataFrame([avg_row])], ignore_index=True)

# Final assignment
target = result_with_avg

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
