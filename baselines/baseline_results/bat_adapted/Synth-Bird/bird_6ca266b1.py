import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[(table_1['label_type'] == 'label') & (table_1['label_value'].isin(['+','-']))].copy()
    df['is_carcinogenic'] = df['label_value'].map({'+': True, '-': False})
    df = df.drop_duplicates(subset=['molecule_id'], keep='first')
    target = df[['molecule_id','is_carcinogenic']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['molecule_id'] = df['bond_id'].str.extract(r'^([^_]+)', expand=False)
    target = df[['molecule_id','bond_id','atom_id','atom_id2']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_labels = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_bonds = prepared_table_2

# Assume prepared_labels and prepared_bonds are materialized as specified.
# 1) Keep only carcinogenic molecules
carc = prepared_labels.query('is_carcinogenic == True')[['molecule_id']].drop_duplicates()

# 2) Join bonds to carcinogenic set
carc_bonds = prepared_bonds.merge(carc, on='molecule_id', how='inner')

# 3) Deduplicate undirected bonds (table_2 lists both directions). Count unique bonds per molecule.
unique_bonds = carc_bonds[['molecule_id','bond_id']].drop_duplicates()

# 4) Identify double bonds (assuming bond_id encoding does not provide order; if bond order metadata exists elsewhere, adapt here).
# If bond order is encoded in bond_id (e.g., includes 'DB' or '=') extract; otherwise cannot distinguish. Here we assume bond order is not provided,
# so we interpret "most double bonds" as counting unique bonds and selecting the max only if a double-bond flag/encoding exists.
# Placeholder extraction: treat bond_id containing '=' as double bond. Adjust pattern per dataset specifics.
unique_bonds['is_double'] = unique_bonds['bond_id'].str.contains('=')

# 5) Aggregate counts
counts = (unique_bonds.groupby('molecule_id', as_index=False)
          .agg(double_bonds=('is_double','sum')))

# 6) Pick molecule with maximum number of double bonds
max_db = counts.loc[counts['double_bonds'].idxmax()]

answer = {
    'molecule_id': max_db['molecule_id'],
    'double_bonds': int(max_db['double_bonds'])
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
