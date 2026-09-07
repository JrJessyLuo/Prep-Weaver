import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.rename(columns={'-': 'molecule_id'})
    parts = df['bond_id'].astype(str).str.split('_', expand=True)
    df['bond_type'] = 'single'
    df['atom1_id'] = df['molecule_id'].astype(str) + '_' + parts[1].astype(str)
    df['atom2_id'] = df['molecule_id'].astype(str) + '_' + parts[2].astype(str)
    target = df[['bond_id', 'molecule_id', 'bond_type', 'atom1_id', 'atom2_id']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    parts = df['jd'].astype(str).str.split('_', n=2, expand=True)
    df['molecule_id'] = parts[0]
    df['atom1_id'] = parts[0].astype(str) + '_' + parts[1].astype(str)
    df['atom2_id'] = parts[0].astype(str) + '_' + parts[2].astype(str)
    df['bond_id'] = df['jd']
    df['bond_type'] = 'single'
    target = df[['bond_id','molecule_id','bond_type','atom1_id','atom2_id']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['atom_id','molecule_id','element']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_bonds = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_bonds_from_jd = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_atoms = prepared_table_3

# prepared_bonds from table_1
b1 = prepared_bonds.copy()
# prepared_bonds_from_jd from table_2
b2 = prepared_bonds_from_jd.copy()
# prepared_atoms from table_3
atoms = prepared_atoms.copy()

# Combine single bonds from both sources (if both exist)
all_bonds = pd.concat([b1, b2], ignore_index=True, sort=False).drop_duplicates(subset=['bond_id'])

# Annotate atom elements
all_bonds = all_bonds.merge(atoms[['atom_id','element']].rename(columns={'atom_id':'atom1_id','element':'atom1_element'}), on='atom1_id', how='left')
all_bonds = all_bonds.merge(atoms[['atom_id','element']].rename(columns={'atom_id':'atom2_id','element':'atom2_element'}), on='atom2_id', how='left')

# The question: "What atoms are connected in single type bonds?"
# Return the pair of atom_ids and their elements for single bonds
answer = all_bonds[['bond_id','molecule_id','atom1_id','atom1_element','atom2_id','atom2_element']]

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
