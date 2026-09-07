import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="molecule_id", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['molecule_id'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['molecule_id']
    if _dtype == "datetime64":
        table_1['molecule_id'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['molecule_id'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['molecule_id'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['molecule_id'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""
    # def filter_func(row: pd.Series) -> bool:
    #     return str(row['label_type']).strip().lower() == 'label'
    # """)
    # Filter
    def filter_func(row: pd.Series) -> bool:
        return str(row['label_type']).strip().lower() == 'label'
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="is_carcinogenic", func="""
    # def compute(row: pd.Series):
    #     v = str(row['label_value']).strip()
    #     if v == '+':
    #         return True
    #     if v == '-':
    #         return False
    #     return None
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        v = str(row['label_value']).strip()
        if v == '+':
            return True
        if v == '-':
            return False
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["is_carcinogenic"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['molecule_id', 'is_carcinogenic'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['molecule_id', 'is_carcinogenic'], how='any').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['molecule_id'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['molecule_id'], keep='last').reset_index(drop=True)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['molecule_id', 'is_carcinogenic'])
    # SelectCol
    _cols = [c for c in ['molecule_id', 'is_carcinogenic'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 7 ----------------
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
    # StandardizeString(table_name="table_1", column_name="atom_id", func="""
    # import re
    # def transform_func(s):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # Normalize repeated underscores/spaces
    #     s = re.sub(r'\s+', '', s)
    #     s = re.sub(r'_+', '_', s)
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return None
        s = str(s).strip()
        # Normalize repeated underscores/spaces
        s = re.sub(r'\s+', '', s)
        s = re.sub(r'_+', '_', s)
        return s
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
    # AddNewColumn(table_name="table_1", new_column_name="molecule_id", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     val = row.get('atom_id', None)
    #     if val is None:
    #         return None
    #     s = str(val)
    #     return s.split('_', 1)[0] if '_' in s else s
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        val = row.get('atom_id', None)
        if val is None:
            return None
        s = str(val)
        return s.split('_', 1)[0] if '_' in s else s
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["molecule_id"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 3 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="bond_order", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     # bond order not present in the source table; leave null for downstream filtering
    #     return None
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        # bond order not present in the source table; leave null for downstream filtering
        return None
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["bond_order"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['bond_id'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['bond_id'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['molecule_id', 'bond_id', 'bond_order'])
    # SelectCol
    _cols = [c for c in ['molecule_id', 'bond_id', 'bond_order'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
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
prepared_labels = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_bonds = prepared_table_2

# prepared_labels has columns: molecule_id, is_carcinogenic
# prepared_bonds has columns: molecule_id, bond_id, bond_order

# Join bonds to labels to focus on carcinogenic molecules
carc_bonds = prepared_bonds.merge(prepared_labels, on='molecule_id', how='inner')
carc_bonds = carc_bonds[carc_bonds['is_carcinogenic'] == True]

# Identify double bonds. If bond_order encodes order numerically or as 'double', normalize:
order_col = carc_bonds['bond_order']
# Convert common encodings to numeric where possible
map_vals = {
    'single': 1, 'double': 2, 'triple': 3,
    '1': 1, '2': 2, '3': 3
}
order_num = order_col.map(lambda v: map_vals.get(str(v).strip().lower(), pd.to_numeric(v, errors='coerce')))
carc_bonds['bond_order_num'] = order_num

# Keep only double bonds (bond_order_num == 2)
double_bonds = carc_bonds[carc_bonds['bond_order_num'] == 2]

# Count double bonds per molecule
counts = double_bonds.groupby('molecule_id', as_index=False).agg(double_bond_count=('bond_id', 'nunique'))

# Find molecule(s) with the maximum number of double bonds
if counts.empty:
    result = pd.DataFrame([], columns=['molecule_id', 'double_bond_count'])
else:
    max_cnt = counts['double_bond_count'].max()
    result = counts[counts['double_bond_count'] == max_cnt].sort_values(['molecule_id']).reset_index(drop=True)

# 'result' contains the carcinogenic molecule(s) with the most double bonds and their counts.
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
