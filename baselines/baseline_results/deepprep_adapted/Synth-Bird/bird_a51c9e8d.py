import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="molecule_code", func="""
    # def compute(row):
    #     v = row.get('atom_id', None)
    #     if v is None:
    #         return None
    #     s = str(v)
    #     return s.split('_', 1)[0] if '_' in s else s
    # """)
    # AddNewColumn
    def compute(row):
        v = row.get('atom_id', None)
        if v is None:
            return None
        s = str(v)
        return s.split('_', 1)[0] if '_' in s else s
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["molecule_code"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 2 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="element_symbol", func="""
    # def compute(row):
    #     v = row.get('molecule_element', None)
    #     if v is None:
    #         return None
    #     s = str(v).strip()
    #     # expected pattern: <molecule_code>_<element_symbol>
    #     if '_' in s:
    #         return s.split('_', 1)[1].strip()
    #     return None
    # """)
    # AddNewColumn
    def compute(row):
        v = row.get('molecule_element', None)
        if v is None:
            return None
        s = str(v).strip()
        # expected pattern: <molecule_code>_<element_symbol>
        if '_' in s:
            return s.split('_', 1)[1].strip()
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["element_symbol"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['molecule_code', 'element_symbol'])
    # SelectCol
    _cols = [c for c in ['molecule_code', 'element_symbol'] if c in table_1.columns]
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
    # SelectCol(table_name="table_1", columns=['molecule_code', 'is_carcinogenic'])
    # SelectCol
    _cols = [c for c in ['molecule_code', 'is_carcinogenic'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
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
