import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['bond_type'] = df['bond_id_type'].astype(str).str.split('|', n=1).str[1]
    target = df[['molecule_id', 'bond_id_type', 'bond_type']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['molecule_id', 'label']].copy()
    target['label'] = target['label'].astype(str).str.replace("^b'", "", regex=True).str.replace("'$", "", regex=True)
    target = target.drop_duplicates(subset=['molecule_id'], keep='first').reset_index(drop=True)
    target = target.loc[:, ['molecule_id', 'label']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.assign(molecule_id=table_1['atom_id'].astype(str).str.split('_').str[0])[['atom_id','molecule_id','ys']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_bonds = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_molecule_labels = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_atoms = prepared_table_3

single_bonds = prepared_bonds[prepared_bonds['bond_type'] == '-']
# Join atoms to know available elements per molecule, if needed for evidence
sb_with_atoms = single_bonds.merge(prepared_atoms, on='molecule_id', how='left')
# Count distinct elements (ys) per molecule that has at least one single bond
elements_per_mol = sb_with_atoms.groupby('molecule_id')['ys'].nunique().reset_index(name='n_elements')
# If the question asks 'How many elements are there for single bond molecules?', interpret as the number of distinct element symbols present across all molecules that have at least one single bond
answer = elements_per_mol['n_elements'].sum()
# Alternatively, if it means distinct element types across all such molecules:
# answer = sb_with_atoms['ys'].dropna().unique().size

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
