import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['atom_id','n']].copy()
    prepared['molecule_id'] = prepared['atom_id'].astype(str).str.split('_').str[0]
    target = prepared[['molecule_id','atom_id','n']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['mid', 'lb']].astype({'mid': 'string', 'lb': 'string'})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_atoms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_labels = prepared_table_2

# prepared_atoms creation from table_1
prepared_atoms = table_1.copy()
# derive molecule_id from atom_id like 'TR001_12' -> 'TR001'
prepared_atoms['molecule_id'] = prepared_atoms['atom_id'].str.split('_').str[0]
# keep only necessary columns
prepared_atoms = prepared_atoms[['molecule_id', 'atom_id', 'n']]

# prepared_labels is a simple rename/selection from table_2
prepared_labels = table_2[['mid', 'lb']].copy()

# integrate atom-level nitrogen info with molecule-level labels
merged = prepared_atoms.merge(prepared_labels, left_on='molecule_id', right_on='mid', how='inner')

# Normalize values: treat strings 'nan'/'NaN' as missing
for col in ['n', 'lb']:
    merged[col] = merged[col].replace({"nan": pd.NA, "NaN": pd.NA})

# Identify molecules that have at least one nitrogen-containing atom
# Assume 'n' is non-missing/non-empty when nitrogen is present. Adjust condition if 'n' encodes differently.
merged['has_n'] = merged['n'].notna() & (merged['n'].astype(str).str.strip() != '')

# Carcinogenic label '+' indicates carcinogenic molecules
is_carcinogenic = merged['lb'] == '+'

# Aggregate to molecule level: molecules that are carcinogenic and have nitrogen
molecule_flags = merged.groupby('molecule_id').agg({
    'has_n': 'max',  # any N atom
    'lb': 'first'    # label consistent per molecule
}).reset_index()

result_count = molecule_flags[(molecule_flags['lb'] == '+') & (molecule_flags['has_n'])]['molecule_id'].nunique()

answer = int(result_count)

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
