import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    parts = df['combined_bond'].astype(str).str.split('_', expand=True)
    df['molecule_id'] = parts[0]
    df['bond_type'] = parts[3].map({'+': 'double', '-': 'single'})
    target = df[['molecule_id', 'bond_type', 'combined_bond']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    mols = df.loc[0, 'molecule_id'].split(',')
    vals = df.loc[0, 'label_value'].split(',')
    ltype = df.loc[0, 'label_type']
    target = pd.DataFrame({'molecule_id': mols, 'label_type': [ltype] * len(mols), 'label_value': vals})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_bonds = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_labels = prepared_table_2

# prepared_bonds has columns: molecule_id, bond_type, combined_bond
# prepared_labels has columns: molecule_id, label_type, label_value

# 1) Select molecules that have at least one single bond
single_bond_mols = prepared_bonds.query("bond_type == '-' ")[['molecule_id']].drop_duplicates()

# 2) Join with labels to get carcinogenicity
merged = single_bond_mols.merge(prepared_labels[['molecule_id','label_value']], on='molecule_id', how='left')

# 3) Filter to non-carcinogenic (label_value == '-') among single-bond molecules
answer = merged.query("label_value == '-' ")

# 4) Produce list of molecule_ids (unique)
result = answer[['molecule_id']].drop_duplicates().sort_values('molecule_id')

# result is the final table of molecule_ids with single bonds that are not carcinogenic

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
