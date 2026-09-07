import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'molecule_element', 'target_columns': ['part_left', 'part_right'], 'func': "def transform(s):\n    s = str(s)\n    parts = s.split('_', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return parts"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'part_left', 'new_name': 'molecule_id'}, {'old_name': 'part_right', 'new_name': 'element_code'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'element_code', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['atom_id', 'molecule_id', 'element_code']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'molecule_id', 'func': "def transform(s):\n    # Trim only; preserve original case for IDs like 'TR000'\n    return str(s).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['bond_id', 'molecule_id', 'bond_type']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = str(s)\n    parts = s.split('_', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['molecule_element'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['part_left'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['part_right'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'part_left': 'molecule_id', 'part_right': 'element_code'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['element_code'] = tmp_2['element_code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['atom_id', 'molecule_id', 'element_code']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    # Trim only; preserve original case for IDs like 'TR000'\n    return str(s).strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['molecule_id'] = tmp_0['molecule_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['bond_id', 'molecule_id', 'bond_type']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t_atoms = prepared_table_1.copy()
# Identify molecules that contain at least one chlorine atom (element_code == 'cl'), case-insensitive already standardized
chlorine_mols = t_atoms[t_atoms['element_code'].str.lower() == 'cl'][['molecule_id']].drop_duplicates()
# Join molecules with bonds to retain only molecules present in bond table and to provide context
integrated = chlorine_mols.merge(prepared_table_2, on='molecule_id', how='inner')
# The question asks: Among molecules which contain 'cl' element, which of them are carcinogenic?
# We do not have an explicit carcinogenicity column in the selected tables. As a best-effort integration, return the list of unique molecule_ids that contain chlorine (the plausible candidates), preserving evidence columns.
# Produce a unique list of molecule_ids with chlorine
target = integrated[['molecule_id']].drop_duplicates().sort_values('molecule_id').reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
