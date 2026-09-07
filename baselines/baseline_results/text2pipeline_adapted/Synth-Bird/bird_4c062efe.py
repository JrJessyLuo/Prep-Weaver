import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['first_name', 'last_name'], 'target_column': 'full_name', 'func': "def transform(row):\n    a = str(row['first_name']).strip() if row['first_name'] is not None else ''\n    b = str(row['last_name']).strip() if row['last_name'] is not None else ''\n    return (a + ' ' + b).strip()"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'link_to_major', 'new_name': 'major_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['member_id', 'major_id', 'full_name']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'major_info', 'target_columns': ['major_name', 'department', 'college'], 'func': "def transform(s):\n    parts = str(s).split('::') if s is not None else []\n    parts = (parts + [None, None, None])[:3]\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'department', 'func': 'def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return None if s is None else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['major_id', 'department', 'major_name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['first_name'] = tmp_0['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['last_name'] = tmp_1['last_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Concatenate
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(row):\n    a = str(row['first_name']).strip() if row['first_name'] is not None else ''\n    b = str(row['last_name']).strip() if row['last_name'] is not None else ''\n    return (a + ' ' + b).strip()", globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_2['full_name'] = tmp_2[['first_name', 'last_name']].apply(_concat_func_3, axis=1)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'link_to_major': 'major_id'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['member_id', 'major_id', 'full_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('::') if s is not None else []\n    parts = (parts + [None, None, None])[:3]\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['major_info'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['major_name'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['department'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_0['college'] = _split_values_1.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return None if s is None else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['department'] = tmp_1['department'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['major_id', 'department', 'major_name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='major_id')
# Filter for Art and Design Department using broad, case-insensitive match on department
mask = integrated['department'].astype(str).str.contains('art and design', case=False, na=False)
filtered = integrated[mask]
# If no rows after strict contains, relax by matching 'art' and 'design' separately as a fallback
if filtered.empty:
    mask_relaxed = integrated['department'].astype(str).str.contains('art', case=False, na=False) & integrated['department'].astype(str).str.contains('design', case=False, na=False)
    filtered = integrated[mask_relaxed]
# Final projection of student full names
target = filtered[['full_name']].drop_duplicates().sort_values('full_name')

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
