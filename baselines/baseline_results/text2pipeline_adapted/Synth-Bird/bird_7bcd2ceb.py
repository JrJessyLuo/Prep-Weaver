import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'atom_id', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'br', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'c', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'lv', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'f', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'h', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'i', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'n', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'na', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'o', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'p', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'liu', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'lv', 'new_name': 'molecule_id'}]}, 'table_indices': [0]}, {'op': 'Stack', 'params': {'id_vars': ['atom_id', 'molecule_id'], 'value_vars': ['br', 'c', 'f', 'h', 'i', 'n', 'na', 'o', 'p', 'liu'], 'var_name': 'element', 'value_name': 'indicator'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'indicator', 'func': 'def transform(s):\n    return str(s).strip().lower()\n'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['atom_id', 'molecule_id', 'element', 'indicator']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'mid', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'lb', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'mid', 'new_name': 'molecule_id'}, {'old_name': 'lb', 'new_name': 'carcinogenic_label'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['molecule_id', 'carcinogenic_label']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['atom_id'] = tmp_0['atom_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['br'] = tmp_1['br'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['c'] = tmp_2['c'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['lv'] = tmp_3['lv'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['f'] = tmp_4['f'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['h'] = tmp_5['h'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['i'] = tmp_6['i'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_7['n'] = tmp_7['n'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_9 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_9)
    _std_func_9 = _ns_9.get('transform') or _ns_9.get('transform')
    tmp_8['na'] = tmp_8['na'].apply(lambda s: _std_func_9(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_10 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_10)
    _std_func_10 = _ns_10.get('transform') or _ns_10.get('transform')
    tmp_9['o'] = tmp_9['o'].apply(lambda s: _std_func_10(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_11 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_11)
    _std_func_11 = _ns_11.get('transform') or _ns_11.get('transform')
    tmp_10['p'] = tmp_10['p'].apply(lambda s: _std_func_11(s) if pd.notna(s) else s)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_12 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_12)
    _std_func_12 = _ns_12.get('transform') or _ns_12.get('transform')
    tmp_11['liu'] = tmp_11['liu'].apply(lambda s: _std_func_12(s) if pd.notna(s) else s)
    # Step 13: Rename
    tmp_12 = tmp_11.rename(columns={'lv': 'molecule_id'})
    # Step 14: Stack
    tmp_13 = tmp_12.melt(id_vars=['atom_id', 'molecule_id'], value_vars=['br', 'c', 'f', 'h', 'i', 'n', 'na', 'o', 'p', 'liu'], var_name='element', value_name='indicator')
    # Step 15: StandardizeString
    tmp_14 = tmp_13.copy()
    _ns_13 = {}
    exec('def transform(s):\n    return str(s).strip().lower()\n', globals(), _ns_13)
    _std_func_13 = _ns_13.get('transform') or _ns_13.get('transform')
    tmp_14['indicator'] = tmp_14['indicator'].apply(lambda s: _std_func_13(s) if pd.notna(s) else s)
    # Step 16: SelectCol
    result = tmp_14.loc[:, ['atom_id', 'molecule_id', 'element', 'indicator']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['mid'] = tmp_0['mid'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['lb'] = tmp_1['lb'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'mid': 'molecule_id', 'lb': 'carcinogenic_label'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['molecule_id', 'carcinogenic_label']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
long = prepared_table_1.copy()
# Keep only rows that actually indicate presence of the element for the molecule: indicator equals molecule_id or is a non-empty, non-'nan' marker
mask_present = (long['indicator'].notna()) & (long['indicator'].str.lower() != 'nan') & (long['indicator'].str.len() > 0)
long_present = long[mask_present]
# Join carcinogenic labels
integrated = long_present.merge(prepared_table_2, on='molecule_id', how='inner')
# Filter to Nitrogen element and carcinogenic molecules (label '+')
nitro = integrated[integrated['element'].str.lower() == 'n']
carc = nitro[nitro['carcinogenic_label'] == '+']
# Count distinct molecules that have Nitrogen and are carcinogenic
count_df = carc[['molecule_id']].drop_duplicates()
count = len(count_df)
# Return as a one-row DataFrame with the count
target = pd.DataFrame({'carcinogenic_molecules_with_nitrogen': [count]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
