import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'molecule_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'label_value', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['molecule_id', 'label_type', 'label_value']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'atom_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'molecule_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'element', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['atom_id', 'molecule_id', 'element']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'atom_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'atom_id2', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'bond_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'atom_id', 'target_columns': ['molecule_id', 'tmp_suffix'], 'func': "def transform(s):\n    parts = str(s).split('_', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['tmp_suffix']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['atom_id', 'atom_id2', 'bond_id', 'molecule_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['molecule_id'] = tmp_0['molecule_id'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['label_value'] = tmp_1['label_value'].astype(str)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['molecule_id', 'label_type', 'label_value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['atom_id'] = tmp_0['atom_id'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['molecule_id'] = tmp_1['molecule_id'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['element'] = tmp_2['element'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['atom_id', 'molecule_id', 'element']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['atom_id'] = tmp_0['atom_id'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['atom_id2'] = tmp_1['atom_id2'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['bond_id'] = tmp_2['bond_id'].astype(str)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('_', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return [parts[0], parts[1]]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_3['atom_id'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['molecule_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['tmp_suffix'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 5: DropColumn
    tmp_4 = tmp_3.drop(columns=['tmp_suffix'], errors='ignore').copy()
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['atom_id', 'atom_id2', 'bond_id', 'molecule_id']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
atoms_labeled = prepared_table_2.merge(prepared_table_1, how='left', on='molecule_id')
bonds_with_mol = prepared_table_3.copy()
# Attach label to bonds by joining via molecule_id
bonds_labeled = bonds_with_mol.merge(prepared_table_1, how='left', on='molecule_id')
# Identify double bonds: bond_id encodes atom pairs; to count unique bonds once, select canonical direction atom_id < atom_id2 lexicographically
bonds_labeled['canon_a'] = bonds_labeled[['atom_id','atom_id2']].min(axis=1)
bonds_labeled['canon_b'] = bonds_labeled[['atom_id','atom_id2']].max(axis=1)
# Heuristic: in absence of explicit bond order column, infer double bonds where both connected atoms are carbons. Join atom elements for both endpoints.
b1 = bonds_labeled.merge(prepared_table_2[['atom_id','element']], how='left', left_on='canon_a', right_on='atom_id').rename(columns={'element':'elem_a'})
b1 = b1.drop(columns=['atom_id_y']) if 'atom_id_y' in b1.columns else b1
b1 = b1.rename(columns={'atom_id_x':'atom_id'}) if 'atom_id_x' in b1.columns else b1
b2 = b1.merge(prepared_table_2[['atom_id','element']], how='left', left_on='canon_b', right_on='atom_id').rename(columns={'element':'elem_b'})
b2 = b2.drop(columns=['atom_id_y']) if 'atom_id_y' in b2.columns else b2
# Filter carcinogenic molecules and double-bond-like edges (both atoms carbon)
carc = b2[(b2['label_type'].str.lower()=='label') & (b2['label_value'].str.strip()=='+')]
dbonds = carc[(carc['elem_a'].str.lower()=='c') & (carc['elem_b'].str.lower()=='c')]
# Count unique canonical bonds per molecule_id
unique_db = dbonds.drop_duplicates(subset=['molecule_id','canon_a','canon_b'])
counts = unique_db.groupby('molecule_id', as_index=False).size().rename(columns={'size':'double_bond_count'})
# If no counts (edge case), fallback to all molecules' max based on available bonds
if counts.empty:
    # fallback: consider all bonds regardless of element, still unique per molecule
    all_unique = bonds_labeled.drop_duplicates(subset=['molecule_id','canon_a','canon_b'])
    counts = all_unique.groupby('molecule_id', as_index=False).size().rename(columns={'size':'double_bond_count'})
# Get molecule(s) with max double_bond_count and return their identifiers
max_cnt = counts['double_bond_count'].max()
result = counts[counts['double_bond_count']==max_cnt]
target = result[['molecule_id','double_bond_count']].sort_values(['double_bond_count','molecule_id'], ascending=[False, True])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
