import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'molecule_id', 'new_name': 'molecule_id'}, {'old_name': 'bond_id_type', 'new_name': 'bond_id_type'}])
    # Rename
    table_1 = table_1.rename(columns={'molecule_id': 'molecule_id', 'bond_id_type': 'bond_id_type'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['molecule_id', 'bond_id_type'])
    # SelectCol
    _cols = [c for c in ['molecule_id', 'bond_id_type'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # MissingValueImputation(table_name="table_1", column_name="label", mode="mode")
    # MissingValueImputation
    table_1["label"] = table_1["label"].fillna(table_1["label"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['molecule_id', 'label'])
    # SelectCol
    _cols = [c for c in ['molecule_id', 'label'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="atom_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["atom_id"] = table_1["atom_id"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="fz_id", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["fz_id"] = table_1["fz_id"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ys", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     if s == "":
    #         return s
    #     s = s.lower()
    #     # Canonical element symbol casing: first letter uppercase, rest lowercase
    #     return s[0].upper() + s[1:]
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        if s == "":
            return s
        s = s.lower()
        # Canonical element symbol casing: first letter uppercase, rest lowercase
        return s[0].upper() + s[1:]
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ys"] = table_1["ys"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['atom_id', 'fz_id', 'ys'])
    # SelectCol
    _cols = [c for c in ['atom_id', 'fz_id', 'ys'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 5 ----------------
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

prepared_table_1 = _prep_1(tables['table_2'])
bonds_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
molecules_prepared = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
atoms_prepared = prepared_table_3

# Start from prepared tables: bonds_prepared, atoms_prepared, molecules_prepared
# Identify single-bond molecules: rows in bonds where bond_id_type indicates a single bond (suffix '|-')
single_bonds = bonds_prepared[bonds_prepared['bond_id_type'].astype(str).str.endswith('|-')]

# Get unique molecule_ids that have at least one single bond
single_bond_molecules = single_bonds[['molecule_id']].drop_duplicates()

# Join to atoms to count elements (ys) per those molecules
atoms_in_single = single_bond_molecules.merge(
    atoms_prepared, left_on='molecule_id', right_on='fz_id', how='left'
)

# Count total number of atoms (elements) for the single-bond molecules
# If the question intends unique element types, switch to nunique on ys
result_count = atoms_in_single['atom_id'].notna().sum()

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
