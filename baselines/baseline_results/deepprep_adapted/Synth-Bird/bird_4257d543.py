import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="bond_id", target_columns=['atom1_id', 'atom2_id'], func="""
    # def split(val):
    #     if val is None:
    #         return {"atom1_id": None, "atom2_id": None}
    #     parts = str(val).split('_')
    #     if len(parts) < 3:
    #         return {"atom1_id": None, "atom2_id": None}
    #     mol = parts[0]
    #     i = parts[1]
    #     j = parts[2]
    #     return {"atom1_id": f"{mol}_{i}", "atom2_id": f"{mol}_{j}"}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"atom1_id": None, "atom2_id": None}
        parts = str(val).split('_')
        if len(parts) < 3:
            return {"atom1_id": None, "atom2_id": None}
        mol = parts[0]
        i = parts[1]
        j = parts[2]
        return {"atom1_id": f"{mol}_{i}", "atom2_id": f"{mol}_{j}"}
    for _c in ['atom1_id', 'atom2_id']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['bond_id']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['atom1_id', 'atom2_id']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['bond_id'])

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': '-', 'new_name': 'molecule_id'}])
    # Rename
    table_1 = table_1.rename(columns={'-': 'molecule_id'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="bond_type", func="""
    # def compute(row):
    #     return "single"
    # """)
    # AddNewColumn
    def compute(row):
        return "single"
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["bond_type"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['bond_id', 'molecule_id', 'bond_type', 'atom1_id', 'atom2_id'])
    # SelectCol
    _cols = [c for c in ['bond_id', 'molecule_id', 'bond_type', 'atom1_id', 'atom2_id'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="molecule_id", func="""
    # def compute(row):
    #     val = row.get('jd', None)
    #     if val is None:
    #         return None
    #     parts = str(val).split('_')
    #     return "_".join(parts[:-2]) if len(parts) >= 3 else None
    # """)
    # AddNewColumn
    def compute(row):
        val = row.get('jd', None)
        if val is None:
            return None
        parts = str(val).split('_')
        return "_".join(parts[:-2]) if len(parts) >= 3 else None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["molecule_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SplitColumn(table_name="table_1", source_column="jd", target_columns=['atom1_index', 'atom2_index'], func="""
    # def split(val):
    #     if val is None:
    #         return {"atom1_index": None, "atom2_index": None}
    #     parts = str(val).split('_')
    #     if len(parts) < 3:
    #         return {"atom1_index": None, "atom2_index": None}
    #     return {"atom1_index": parts[-2], "atom2_index": parts[-1]}
    # """)
    # SplitColumn
    def split(val):
        if val is None:
            return {"atom1_index": None, "atom2_index": None}
        parts = str(val).split('_')
        if len(parts) < 3:
            return {"atom1_index": None, "atom2_index": None}
        return {"atom1_index": parts[-2], "atom2_index": parts[-1]}
    for _c in ['atom1_index', 'atom2_index']:
        table_1[_c] = None
    for _i in range(len(table_1)):
        _val = table_1.iloc[_i]['jd']
        if pd.isna(_val):
            continue
        try:
            _res = split(_val)
            if isinstance(_res, dict):
                for _c in ['atom1_index', 'atom2_index']:
                    if _c in _res:
                        table_1[_c].iloc[_i] = _res[_c]
        except Exception:
            continue
    table_1 = table_1.drop(columns=['jd'])

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="atom1_id", func="""
    # def compute(row):
    #     mid = row.get('molecule_id', None)
    #     i = row.get('atom1_index', None)
    #     if mid is None or i is None:
    #         return None
    #     return f"{mid}_{i}"
    # """)
    # AddNewColumn
    def compute(row):
        mid = row.get('molecule_id', None)
        i = row.get('atom1_index', None)
        if mid is None or i is None:
            return None
        return f"{mid}_{i}"
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["atom1_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="atom2_id", func="""
    # def compute(row):
    #     mid = row.get('molecule_id', None)
    #     j = row.get('atom2_index', None)
    #     if mid is None or j is None:
    #         return None
    #     return f"{mid}_{j}"
    # """)
    # AddNewColumn
    def compute(row):
        mid = row.get('molecule_id', None)
        j = row.get('atom2_index', None)
        if mid is None or j is None:
            return None
        return f"{mid}_{j}"
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["atom2_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 5 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="bond_id", func="""
    # def compute(row):
    #     return row.get('jd', None)
    # """)
    # AddNewColumn
    def compute(row):
        return row.get('jd', None)
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["bond_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 6 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="bond_type", func="""
    # def compute(row):
    #     return "single"
    # """)
    # AddNewColumn
    def compute(row):
        return "single"
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["bond_type"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['bond_id', 'molecule_id', 'bond_type', 'atom1_id', 'atom2_id'])
    # SelectCol
    _cols = [c for c in ['bond_id', 'molecule_id', 'bond_type', 'atom1_id', 'atom2_id'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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
    # StandardizeString(table_name="table_1", column_name="element", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["element"] = table_1["element"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['atom_id', 'molecule_id', 'element'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['atom_id', 'molecule_id', 'element'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['atom_id', 'molecule_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['atom_id', 'molecule_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['atom_id', 'molecule_id', 'element'])
    # SelectCol
    _cols = [c for c in ['atom_id', 'molecule_id', 'element'] if c in table_1.columns]
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
