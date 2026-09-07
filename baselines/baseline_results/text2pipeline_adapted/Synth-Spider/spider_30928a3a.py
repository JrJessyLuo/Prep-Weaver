import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Stack', 'params': {'id_vars': ['artistID'], 'value_vars': [111, 222, 333, 444, 555], 'var_name': 'artist_id', 'value_name': 'value'}, 'table_indices': [0]}, {'op': 'Pivot', 'params': {'index': 'artist_id', 'columns': 'artistID', 'values': 'value', 'aggfunc': 'first'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'artist_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fname', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'artist_id', 'new_name': 'painterID'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['painterID', 'fname', 'birthYear', 'deathYear']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'painterID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'medium', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'mediumOn', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'title', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paintingID', 'title', 'year', 'medium', 'mediumOn', 'painterID']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=['artistID'], value_vars=[111, 222, 333, 444, 555], var_name='artist_id', value_name='value')
    # Step 2: Pivot
    tmp_1 = pd.pivot_table(tmp_0, index='artist_id', columns='artistID', values='value', aggfunc='first').reset_index()
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['artist_id'] = pd.to_numeric(tmp_2['artist_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['fname'] = tmp_3['fname'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'artist_id': 'painterID'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['painterID', 'fname', 'birthYear', 'deathYear']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['painterID'] = pd.to_numeric(tmp_0['painterID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['medium'] = tmp_1['medium'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['mediumOn'] = tmp_2['mediumOn'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['title'] = tmp_3['title'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['paintingID', 'title', 'year', 'medium', 'mediumOn', 'painterID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, on='painterID', how='inner')
# Identify painters who have at least one oil work and at least one lithographic work
mediums_by_painter = integrated.groupby('painterID')['medium'].apply(lambda s: set(s.dropna().str.lower().str.strip()))
eligible_ids = [pid for pid, meds in mediums_by_painter.items() if ('oil' in meds) and ('lithograph' in meds or 'lithographic' in meds or any(m.startswith('lithograph') for m in meds))]
result = integrated[integrated['painterID'].isin(eligible_ids)]
# Deduplicate by painter and return first and last names (only first names available; use fname as first name and leave last name blank if unavailable)
# Attempt to split fname on whitespace into first and last if present, else treat entire fname as first name
names = result[['painterID','fname']].drop_duplicates().copy()
split = names['fname'].str.strip().str.split('\s+', n=1, expand=True)
names['first_name'] = split[0]
names['last_name'] = split[1] if split.shape[1] > 1 else ''
# Final projection
target = names[['first_name','last_name']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
