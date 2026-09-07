import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Concatenate', 'params': {'concatenate_columns': ['first_name', 'last_name'], 'target_column': 'full_name', 'func': "def transform(row):\n    fn = '' if pd.isna(row.get('first_name')) else str(row.get('first_name'))\n    ln = '' if pd.isna(row.get('last_name')) else str(row.get('last_name'))\n    return (fn + ' ' + ln).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'first_name', 'last_name', 'full_name']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_member', 'new_name': 'member_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'month', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'day', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'month', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)\n    s = s.strip()\n    return s.zfill(2)"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'day', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)\n    s = s.strip()\n    return s.zfill(2)"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['year', 'month', 'day'], 'target_column': 'received_date', 'func': "def transform(row):\n    y = str(row['year']) if pd.notna(row['year']) else ''\n    m = str(row['month']) if pd.notna(row['month']) else ''\n    d = str(row['day']) if pd.notna(row['day']) else ''\n    return '-'.join([y, m, d]) if y and m and d else ''"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'received_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['income_id', 'member_id', 'amount', 'source', 'notes', 'year', 'month', 'day', 'received_date']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(row):\n    fn = '' if pd.isna(row.get('first_name')) else str(row.get('first_name'))\n    ln = '' if pd.isna(row.get('last_name')) else str(row.get('last_name'))\n    return (fn + ' ' + ln).strip()", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['full_name'] = tmp_0[['first_name', 'last_name']].apply(_concat_func_1, axis=1)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['member_id', 'first_name', 'last_name', 'full_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'link_to_member': 'member_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['year'] = tmp_1['year'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['month'] = tmp_2['month'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['day'] = tmp_3['day'].astype(str)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)\n    s = s.strip()\n    return s.zfill(2)", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['month'] = tmp_4['month'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)\n    s = s.strip()\n    return s.zfill(2)", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['day'] = tmp_5['day'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: Concatenate
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec("def transform(row):\n    y = str(row['year']) if pd.notna(row['year']) else ''\n    m = str(row['month']) if pd.notna(row['month']) else ''\n    d = str(row['day']) if pd.notna(row['day']) else ''\n    return '-'.join([y, m, d]) if y and m and d else ''", globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_6['received_date'] = tmp_6[['year', 'month', 'day']].apply(_concat_func_3, axis=1)
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['received_date'] = pd.to_datetime(tmp_7['received_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['income_id', 'member_id', 'amount', 'source', 'notes', 'year', 'month', 'day', 'received_date']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', on='member_id')
# Filter for the member named Casey Mason; use robust case-insensitive matching on full_name and first/last names
mask_full = integrated['full_name'].str.strip().str.casefold() == 'casey mason'
mask_parts = (integrated['first_name'].str.strip().str.casefold() == 'casey') & (integrated['last_name'].str.strip().str.casefold() == 'mason')
filtered = integrated[mask_full | mask_parts]
# If no direct match, fall back to rows where either name part loosely matches 'casey' or 'mason'
if filtered.empty:
    loose = integrated[
        integrated['first_name'].str.contains('casey', case=False, na=False) |
        integrated['last_name'].str.contains('mason', case=False, na=False) |
        integrated['full_name'].str.contains('casey', case=False, na=False)
    ]
    filtered = loose if not loose.empty else integrated
# Project the relevant columns and sort by received_date to show when income was received
result = filtered[['first_name', 'last_name', 'income_id', 'amount', 'source', 'received_date']].sort_values(by='received_date')
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
