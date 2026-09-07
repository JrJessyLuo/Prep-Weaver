import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': '-', 'new_name': 'molecule_id'}, {'old_name': '=', 'new_name': 'bond_type_flag'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'bond_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'molecule_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'bond_id', 'target_columns': ['molecule_id_from_id', 'atom_idx_1', 'atom_idx_2'], 'func': "def transform(s):\n    parts = str(s).strip().split('_')\n    if len(parts) >= 3:\n        return [parts[0], parts[-2], parts[-1]]\n    return [None, None, None]"}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['molecule_id_from_id', 'atom_idx_1'], 'target_column': 'atom_id_1', 'func': 'def transform(row):\n    a = row.get(\'molecule_id_from_id\')\n    b = row.get(\'atom_idx_1\')\n    if a is None or b is None:\n        return None\n    return f"{a}_{b}"'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['molecule_id_from_id', 'atom_idx_2'], 'target_column': 'atom_id_2', 'func': 'def transform(row):\n    a = row.get(\'molecule_id_from_id\')\n    b = row.get(\'atom_idx_2\')\n    if a is None or b is None:\n        return None\n    return f"{a}_{b}"'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['molecule_id_from_id', 'atom_idx_1', 'atom_idx_2', 'bond_type_flag']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['bond_id', 'molecule_id', 'atom_id_1', 'atom_id_2']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'atom_id', 'new_name': 'atom_id_1'}, {'old_name': 'yzid2', 'new_name': 'atom_id_2'}, {'old_name': 'jd', 'new_name': 'bond_id'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'bond_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'atom_id_1', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'atom_id_2', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['bond_id', 'atom_id_1', 'atom_id_2']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'element', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['atom_id', 'molecule_id', 'element']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'-': 'molecule_id', '=': 'bond_type_flag'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['bond_id'] = tmp_1['bond_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['molecule_id'] = tmp_2['molecule_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    parts = str(s).strip().split('_')\n    if len(parts) >= 3:\n        return [parts[0], parts[-2], parts[-1]]\n    return [None, None, None]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['bond_id'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['molecule_id_from_id'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['atom_idx_1'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_3['atom_idx_2'] = _split_values_3.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(row):\n    a = row.get(\'molecule_id_from_id\')\n    b = row.get(\'atom_idx_1\')\n    if a is None or b is None:\n        return None\n    return f"{a}_{b}"', globals(), _ns_4)
    _concat_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('concat')
    tmp_4['atom_id_1'] = tmp_4[['molecule_id_from_id', 'atom_idx_1']].apply(_concat_func_4, axis=1)
    # Step 6: Concatenate
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(row):\n    a = row.get(\'molecule_id_from_id\')\n    b = row.get(\'atom_idx_2\')\n    if a is None or b is None:\n        return None\n    return f"{a}_{b}"', globals(), _ns_5)
    _concat_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('concat')
    tmp_5['atom_id_2'] = tmp_5[['molecule_id_from_id', 'atom_idx_2']].apply(_concat_func_5, axis=1)
    # Step 7: DropColumn
    tmp_6 = tmp_5.drop(columns=['molecule_id_from_id', 'atom_idx_1', 'atom_idx_2', 'bond_type_flag'], errors='ignore').copy()
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['bond_id', 'molecule_id', 'atom_id_1', 'atom_id_2']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'atom_id': 'atom_id_1', 'yzid2': 'atom_id_2', 'jd': 'bond_id'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['bond_id'] = tmp_1['bond_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['atom_id_1'] = tmp_2['atom_id_1'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['atom_id_2'] = tmp_3['atom_id_2'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['bond_id', 'atom_id_1', 'atom_id_2']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['element'] = tmp_0['element'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['atom_id', 'molecule_id', 'element']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
b1 = prepared_table_1[['bond_id','atom_id_1','atom_id_2']]
b2 = prepared_table_2[['bond_id','atom_id_1','atom_id_2']]
# Harmonize bonds by coalescing endpoints from both sources when available
b = b1.merge(b2, on='bond_id', how='outer', suffixes=('_x','_y'))
b['a1'] = b['atom_id_1_x'].where(b['atom_id_1_x'].notna(), b['atom_id_1_y'])
b['a2'] = b['atom_id_2_x'].where(b['atom_id_2_x'].notna(), b['atom_id_2_y'])
b = b[['bond_id','a1','a2']].rename(columns={'a1':'atom_id_1','a2':'atom_id_2'})
# Attach element info for both endpoints
atoms = prepared_table_3
b = b.merge(atoms[['atom_id','element']].rename(columns={'atom_id':'atom_id_1','element':'element_1'}), on='atom_id_1', how='left')
b = b.merge(atoms[['atom_id','element']].rename(columns={'atom_id':'atom_id_2','element':'element_2'}), on='atom_id_2', how='left')
# The question asks which atoms are connected in single type bonds.
# Interpret as listing endpoint atom_ids (and their elements) for the bonds enumerated.
# Since table_1 appears to represent single bonds, include all bonds present after the union.
# Produce a concise listing of the connected atom pairs with their elements.
target = b[['bond_id','atom_id_1','element_1','atom_id_2','element_2']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
