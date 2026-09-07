import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row):
    #     v = row.get('atom_id', None)
    #     return v is not None and str(v).strip() != ''
    # """)
    # Filter
    def filter_func(row):
        v = row.get('atom_id', None)
        return v is not None and str(v).strip() != ''
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 2 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="molecule_id", func="""
    # def compute(row):
    #     v = row.get('atom_id', None)
    #     if v is None:
    #         return None
    #     s = str(v).strip().strip('"').strip("'")
    #     # molecule_id is prefix before first underscore
    #     return s.split('_', 1)[0] if '_' in s else s
    # """)
    # AddNewColumn
    def compute(row):
        v = row.get('atom_id', None)
        if v is None:
            return None
        s = str(v).strip().strip('"').strip("'")
        # molecule_id is prefix before first underscore
        return s.split('_', 1)[0] if '_' in s else s
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["molecule_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['molecule_id', 'atom_id', 'n'])
    # SelectCol
    _cols = [c for c in ['molecule_id', 'atom_id', 'n'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
