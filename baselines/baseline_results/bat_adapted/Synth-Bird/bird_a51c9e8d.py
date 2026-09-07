import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['molecule_code'] = df['atom_id'].astype(str).str.split('_').str[0]
    df['element_symbol'] = df['molecule_element'].astype(str).str.split('_').str[-1]
    target = df[['molecule_code', 'element_symbol']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    melted = table_1.melt(id_vars=['molecule_id'], var_name='molecule_code', value_name='is_carcinogenic')
    melted['is_carcinogenic'] = melted['is_carcinogenic'].map({'+': True, '-': False})
    target = melted[['molecule_code', 'is_carcinogenic']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
atoms_with_elements = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
molecule_labels = prepared_table_2

# Prepared tables are assumed to be provided as dataframes: atoms_with_elements, molecule_labels
# 1) Filter atoms that are chlorine ('cl') and get distinct molecule codes containing Cl
cl_molecules = (
    atoms_with_elements[atoms_with_elements['element_symbol'].str.lower() == 'cl']
    ['molecule_code']
    .drop_duplicates()
)

# 2) Join with molecule labels to get carcinogenicity for those molecules
result = (
    pd.DataFrame({'molecule_code': cl_molecules})
    .merge(molecule_labels, on='molecule_code', how='left')
)

# 3) Select only carcinogenic molecules
carcinogenic_with_cl = result[result['is_carcinogenic'] == True]['molecule_code'].sort_values().unique().tolist()

# Final answer object
answer = {
    'carcinogenic_molecules_with_cl': carcinogenic_with_cl
}

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
