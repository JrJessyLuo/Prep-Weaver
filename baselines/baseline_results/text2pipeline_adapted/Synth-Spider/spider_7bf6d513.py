import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'pn', 'new_name': 'pilot_name'}, {'old_name': 'pln', 'new_name': 'plane_name'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'age', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'pilot_name', 'func': 'def transform(s):\n    # Trim surrounding whitespace but keep original capitalization\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'plane_name', 'func': 'def transform(s):\n    # Trim surrounding whitespace but keep original capitalization\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['pilot_name', 'plane_name', 'age']}, 'table_indices': [0]}], [{'op': 'Stack', 'params': {'id_vars': [], 'value_vars': ['B-1 Bomber', 'B-52 Bomber', 'F-14 Fighter', 'Piper Cub'], 'var_name': 'plane_name', 'value_name': 'location'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'plane_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'location', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['plane_name', 'location']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'pn': 'pilot_name', 'pln': 'plane_name'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['age'] = pd.to_numeric(tmp_1['age'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but keep original capitalization\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['pilot_name'] = tmp_2['pilot_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but keep original capitalization\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['plane_name'] = tmp_3['plane_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['pilot_name', 'plane_name', 'age']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Stack
    tmp_0 = df.melt(id_vars=[], value_vars=['B-1 Bomber', 'B-52 Bomber', 'F-14 Fighter', 'Piper Cub'], var_name='plane_name', value_name='location')
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['plane_name'] = tmp_1['plane_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['location'] = tmp_2['location'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['plane_name', 'location']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1
t2 = prepared_table_2
integrated = t1.merge(t2, on='plane_name', how='inner')
# Find pilots who have planes in both Austin and Boston
has_austin = integrated[integrated['location'].str.casefold() == 'austin']
has_boston = integrated[integrated['location'].str.casefold() == 'boston']
pilots_austin = set(has_austin['pilot_name'])
pilots_boston = set(has_boston['pilot_name'])
common_pilots = pilots_austin.intersection(pilots_boston)
result = integrated[integrated['pilot_name'].isin(list(common_pilots))]
# Project unique pilot names
target = result[['pilot_name']].drop_duplicates().sort_values('pilot_name').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
