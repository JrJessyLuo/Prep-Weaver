import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['bond_id','attribute_value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['bond_id','atom_id','atom_id2']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_bond_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_bond_mapping = prepared_table_2

# prepared_bond_attributes: columns [bond_id, attribute_value]
# prepared_bond_mapping: columns [bond_id, atom_id, atom_id2]

merged = prepared_bond_attributes.merge(prepared_bond_mapping, on='bond_id', how='inner')

# Derive molecule_id from atom_id prefix before the last underscore (e.g., TR123 from TR123_4)
# Assumes atom_id uses the pattern MoleculeID_index (matches samples like TR000_1)
merged['molecule_id'] = merged['atom_id'].str.rsplit('_', n=1).str[0]

# Identify bonds of type 'single' (case-insensitive, trim)
merged['attr_norm'] = merged['attribute_value'].astype(str).str.strip().str.lower()
single_bonds = merged[merged['attr_norm'] == 'single']

# Determine non-carcinogenic molecules: here we infer that molecules considered are those with no bond labeled 'carcinogenic'.
# If 'attribute_value' contains such a tag per bond, flag molecules that have any 'carcinogenic' bond label.
carc_bonds = merged[merged['attr_norm'] == 'carcinogenic']
carc_molecules = set(carc_bonds['molecule_id'].unique())

# Molecules having at least one single bond and not in carcinogenic set
single_molecules = set(single_bonds['molecule_id'].unique())
non_carc_single_molecules = [m for m in single_molecules if m not in carc_molecules]

result = len(non_carc_single_molecules)

answer = result

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
