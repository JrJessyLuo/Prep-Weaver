import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'atom_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'atom_id2', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'bond_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'bond_id', 'target_columns': ['molecule_id', '_rest'], 'func': "def transform(s):\n    parts = str(s).split('_', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_rest']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['molecule_id', 'atom_id', 'atom_id2', 'bond_id']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'atom_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'molecule_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'element', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['molecule_id', 'atom_id', 'element']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'molecule_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'label_type', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'label_value', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'molecule_id', 'target_columns': ['mol_list_str'], 'func': 'def transform(s):\n    return [str(s)]'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'label_value', 'target_columns': ['label_list_str'], 'func': 'def transform(s):\n    return [str(s)]'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'mol_list_str', 'func': "def transform(s):\n    return ','.join([p.strip() for p in str(s).split(',')])"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'label_list_str', 'func': "def transform(s):\n    return ','.join([p.strip() for p in str(s).split(',')])"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'mol_list_str', 'target_columns': ['mol_list'], 'func': "def transform(s):\n    return [[p for p in str(s).split(',') if p!='']]"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'label_list_str', 'target_columns': ['label_list'], 'func': "def transform(s):\n    return [[p for p in str(s).split(',') if p!='']]"}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'mol_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'label_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'mol_list', 'new_name': 'molecule_id'}, {'old_name': 'label_list', 'new_name': 'raw_label'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'raw_label', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'raw_label', 'new_name': 'carcinogenic_label'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['molecule_id', 'carcinogenic_label']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['atom_id'] = tmp_0['atom_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['atom_id2'] = tmp_1['atom_id2'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['bond_id'] = tmp_2['bond_id'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    parts = str(s).split('_', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]", globals(), _ns_4)
    _split_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('split')
    _split_values_4 = tmp_3['bond_id'].apply(_split_func_4)
    _split_values_4 = _split_values_4.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['molecule_id'] = _split_values_4.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['_rest'] = _split_values_4.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: DropColumn
    tmp_4 = tmp_3.drop(columns=['_rest'], errors='ignore').copy()
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['molecule_id', 'atom_id', 'atom_id2', 'bond_id']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_4', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['atom_id'] = tmp_0['atom_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['molecule_id'] = tmp_1['molecule_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['element'] = tmp_2['element'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['molecule_id', 'atom_id', 'element']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['molecule_id'] = tmp_0['molecule_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['label_type'] = tmp_1['label_type'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['label_value'] = tmp_2['label_value'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return [str(s)]', globals(), _ns_4)
    _split_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('split')
    _split_values_4 = tmp_3['molecule_id'].apply(_split_func_4)
    _split_values_4 = _split_values_4.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['mol_list_str'] = _split_values_4.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: SplitColumn
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return [str(s)]', globals(), _ns_5)
    _split_func_5 = _ns_5.get('transform') or _ns_5.get('transform') or _ns_5.get('split')
    _split_values_5 = tmp_4['label_value'].apply(_split_func_5)
    _split_values_5 = _split_values_5.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_4['label_list_str'] = _split_values_5.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec("def transform(s):\n    return ','.join([p.strip() for p in str(s).split(',')])", globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['mol_list_str'] = tmp_5['mol_list_str'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec("def transform(s):\n    return ','.join([p.strip() for p in str(s).split(',')])", globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['label_list_str'] = tmp_6['label_list_str'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: SplitColumn
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec("def transform(s):\n    return [[p for p in str(s).split(',') if p!='']]", globals(), _ns_8)
    _split_func_8 = _ns_8.get('transform') or _ns_8.get('transform') or _ns_8.get('split')
    _split_values_8 = tmp_7['mol_list_str'].apply(_split_func_8)
    _split_values_8 = _split_values_8.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_7['mol_list'] = _split_values_8.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 9: SplitColumn
    tmp_8 = tmp_7.copy()
    _ns_9 = {}
    exec("def transform(s):\n    return [[p for p in str(s).split(',') if p!='']]", globals(), _ns_9)
    _split_func_9 = _ns_9.get('transform') or _ns_9.get('transform') or _ns_9.get('split')
    _split_values_9 = tmp_8['label_list_str'].apply(_split_func_9)
    _split_values_9 = _split_values_9.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_8['label_list'] = _split_values_9.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 10: Explode
    tmp_9 = tmp_8.explode('mol_list')
    # Step 11: Explode
    tmp_10 = tmp_9.explode('label_list')
    # Step 12: Rename
    tmp_11 = tmp_10.rename(columns={'mol_list': 'molecule_id', 'label_list': 'raw_label'})
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_10 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_10)
    _std_func_10 = _ns_10.get('transform') or _ns_10.get('transform')
    tmp_12['raw_label'] = tmp_12['raw_label'].apply(lambda s: _std_func_10(s) if pd.notna(s) else s)
    # Step 14: Rename
    tmp_13 = tmp_12.rename(columns={'raw_label': 'carcinogenic_label'})
    # Step 15: SelectCol
    result = tmp_13.loc[:, ['molecule_id', 'carcinogenic_label']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Extract unique molecule_ids from bonds (interpreted as single bonds present)
mol_from_bonds = prepared_table_1[['molecule_id']].drop_duplicates()

# prepared_table_3 has duplicate column labels; select by position and rename for a clean merge
labels_raw = prepared_table_3.iloc[:, [1, 2]].copy()
labels_raw.columns = ['molecule_id', 'carcinogenic_label']

# Merge molecules from bonds with labels
mol_with_labels = mol_from_bonds.merge(labels_raw, how='left', on='molecule_id')

# Normalize label text for robust filtering
mol_with_labels['carcinogenic_label_norm'] = mol_with_labels['carcinogenic_label'].astype(str).str.strip().str.lower()

# Primary filter: explicitly non-carcinogenic marked as '-'
non_carc = mol_with_labels[mol_with_labels['carcinogenic_label_norm'] == '-']

# If no explicit '-' found, relax: include molecules without a '+' label (unknown or missing)
if non_carc.empty:
    non_carc = mol_with_labels[mol_with_labels['carcinogenic_label_norm'] != '+']

# Final projection
target = non_carc[['molecule_id']].drop_duplicates().sort_values('molecule_id').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
