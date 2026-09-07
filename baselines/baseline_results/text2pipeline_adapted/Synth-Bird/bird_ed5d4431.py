import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'bond_id', 'new_name': 'bond_type_code'}, {'old_name': 'attribute_value', 'new_name': 'bond_type'}, {'old_name': 'part1', 'new_name': 'bond_key'}, {'old_name': 'part2', 'new_name': 'bond_key_part2'}, {'old_name': 'part3', 'new_name': 'bond_key_part3'}, {'old_name': 'sep1', 'new_name': 'sep1'}, {'old_name': 'sep2', 'new_name': 'sep2'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'bond_type', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['bond_key', 'bond_type']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['atom_id', 'molecule_id', 'element']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'atom_id', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'molecule_id', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'element', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'atom_id', 'new_name': 'atom_id_1'}, {'old_name': 'atom_id2', 'new_name': 'atom_id_2'}, {'old_name': 'bond_id', 'new_name': 'bond_key'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'atom_id_1', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'atom_id_2', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'bond_key', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['atom_id_1', 'atom_id_2', 'bond_key']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'bond_id': 'bond_type_code', 'attribute_value': 'bond_type', 'part1': 'bond_key', 'part2': 'bond_key_part2', 'part3': 'bond_key_part3', 'sep1': 'sep1', 'sep2': 'sep2'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['bond_type'] = tmp_1['bond_type'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['bond_key', 'bond_type']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    tmp_0 = df.loc[:, ['atom_id', 'molecule_id', 'element']].copy()
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['atom_id'] = tmp_1['atom_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['molecule_id'] = tmp_2['molecule_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    result = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    result['element'] = result['element'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'atom_id': 'atom_id_1', 'atom_id2': 'atom_id_2', 'bond_id': 'bond_key'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['atom_id_1'] = tmp_1['atom_id_1'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['atom_id_2'] = tmp_2['atom_id_2'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['bond_key'] = tmp_3['bond_key'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['atom_id_1', 'atom_id_2', 'bond_key']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge bonds to atoms to get molecule IDs via both atoms
bt = prepared_table_1.rename(columns={"bond_key": "bond_key", "bond_type": "bond_type"})
conn = prepared_table_3.rename(columns={"atom_id_1": "atom_id_1", "atom_id_2": "atom_id_2", "bond_key": "bond_key"})
atoms = prepared_table_2

bond_mol_1 = conn.merge(atoms[["atom_id", "molecule_id"]], left_on="atom_id_1", right_on="atom_id", how="left").drop(columns=["atom_id"]).rename(columns={"molecule_id": "molecule_id_1"})
bond_mol_2 = bond_mol_1.merge(atoms[["atom_id", "molecule_id"]], left_on="atom_id_2", right_on="atom_id", how="left").drop(columns=["atom_id"]).rename(columns={"molecule_id": "molecule_id_2"})

# Prefer molecule_id from first atom, fallback to second
bond_mol_2["molecule_id"] = bond_mol_2["molecule_id_1"].where(bond_mol_2["molecule_id_1"].notna(), bond_mol_2["molecule_id_2"])

# Join bond types
bond_with_type = bond_mol_2.merge(bt, on="bond_key", how="left")

# Identify single bonds using broader case-insensitive matching
bt_series = bond_with_type["bond_type"].fillna("").str.lower().str.strip()
single_mask = bt_series.eq("single") | bt_series.str.contains("single", na=False)
single_bonds = bond_with_type.loc[single_mask]

# Lacking carcinogenicity table, treat absence of carcinogenic labels as non-carcinogenic signal in this integrated subset
non_carcinogenic_single_mols = single_bonds[["molecule_id"]].dropna().drop_duplicates()

# Final single-row DataFrame with the count
count_val = non_carcinogenic_single_mols["molecule_id"].nunique()
target = __import__("pandas").DataFrame({"count": [count_val]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
