import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'bond_id_type', 'target_columns': ['bond_core', 'bond_symbol'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('|', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'bond_core', 'target_columns': ['molecule_id_chk', 'atom1_id', 'atom2_id'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('_')\n    # Expecting exactly 3 parts: mol, atom1, atom2\n    out = ['','','']\n    for i in range(min(3, len(parts))):\n        out[i] = parts[i]\n    return out"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'bond_symbol', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'bond_symbol', 'new_name': 'bond_type_symbol'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'molecule_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'atom1_id', 'target_columns': ['atom1_id'], 'func': 'def transform(s):\n    try:\n        v = str(s).strip()\n        return [int(v)] if v.isdigit() else [v]\n    except Exception:\n        return [s]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'atom2_id', 'target_columns': ['atom2_id'], 'func': 'def transform(s):\n    try:\n        v = str(s).strip()\n        return [int(v)] if v.isdigit() else [v]\n    except Exception:\n        return [s]'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['molecule_id', 'bond_type_symbol', 'atom1_id', 'atom2_id', 'molecule_id_chk']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'fz_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'atom_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ys', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'fz_id', 'new_name': 'molecule_id'}, {'old_name': 'ys', 'new_name': 'element_symbol'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['molecule_id', 'atom_id', 'element_symbol']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('|', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['bond_id_type'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['bond_core'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['bond_symbol'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('_')\n    # Expecting exactly 3 parts: mol, atom1, atom2\n    out = ['','','']\n    for i in range(min(3, len(parts))):\n        out[i] = parts[i]\n    return out", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['bond_core'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['molecule_id_chk'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['atom1_id'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_1['atom2_id'] = _split_values_2.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['bond_symbol'] = tmp_2['bond_symbol'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'bond_symbol': 'bond_type_symbol'})
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_4['molecule_id'] = tmp_4['molecule_id'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 6: SplitColumn
    tmp_5 = tmp_4.copy()
    _ns_5 = {}
    exec('def transform(s):\n    try:\n        v = str(s).strip()\n        return [int(v)] if v.isdigit() else [v]\n    except Exception:\n        return [s]', globals(), _ns_5)
    _split_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('split')
    _split_values_5 = tmp_5['atom1_id'].apply(_split_func_5)
    _split_values_5 = _split_values_5.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_5['atom1_id'] = _split_values_5.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 7: SplitColumn
    tmp_6 = tmp_5.copy()
    _ns_6 = {}
    exec('def transform(s):\n    try:\n        v = str(s).strip()\n        return [int(v)] if v.isdigit() else [v]\n    except Exception:\n        return [s]', globals(), _ns_6)
    _split_func_6 = _ns_6.get('transform') or _ns_6.get('transform') or _ns_6.get('split')
    _split_values_6 = tmp_6['atom2_id'].apply(_split_func_6)
    _split_values_6 = _split_values_6.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_6['atom2_id'] = _split_values_6.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['molecule_id', 'bond_type_symbol', 'atom1_id', 'atom2_id', 'molecule_id_chk']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['fz_id'] = tmp_0['fz_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['atom_id'] = tmp_1['atom_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['ys'] = tmp_2['ys'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'fz_id': 'molecule_id', 'ys': 'element_symbol'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['molecule_id', 'atom_id', 'element_symbol']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
single_bond = prepared_table_1[prepared_table_1['bond_type_symbol'].str.strip().str.lower() == '-']
integrated = single_bond.merge(prepared_table_2, on='molecule_id', how='inner')
# Count unique elements (by symbol) present in molecules that have at least one single bond
# Interpret the question as the number of distinct element types in those molecules
unique_elements = integrated['element_symbol'].dropna().str.strip().str.lower().unique()
count_df = pd.DataFrame({'elements_count': [len(unique_elements)]})
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
