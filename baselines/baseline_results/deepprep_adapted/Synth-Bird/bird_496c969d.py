import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="First Date", mode="mode")
    # MissingValueImputation
    table_1["First Date"] = table_1["First Date"].fillna(table_1["First Date"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ID", func="""
    # import re
    # def transform_func(s: str):
    #     if s is None:
    #         return None
    #     s = str(s).strip()
    #     # remove repeated double-quotes like ""4526214""
    #     s = s.replace('""', '').replace('"', '')
    #     return s.strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return None
        s = str(s).strip()
        # remove repeated double-quotes like ""4526214""
        s = s.replace('""', '').replace('"', '')
        return s.strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ID"] = table_1["ID"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="First Date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['First Date'] = table_1['First Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['First Date'] = table_1['First Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'First Date', 'Admission'])
    # SelectCol
    _cols = [c for c in ['ID', 'First Date', 'Admission'] if c in table_1.columns]
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
    # Sort(table_name="table_1", by=['ID', 'Date'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['ID', 'Date'], ascending=[True, True])

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ID']
    if _dtype == "datetime64":
        table_1['ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ID'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="Date", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['Date'] = table_1['Date'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['Date'] = table_1['Date'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 4 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['ID', 'Date', 'SSA'])
    # SelectCol
    _cols = [c for c in ['ID', 'Date', 'SSA'] if c in table_1.columns]
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
patients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs = prepared_table_2

# Assume patients and labs are the prepared tables from table_1 and table_2 respectively
p = patients.copy()
l = labs.copy()

# Normalize ID types (table_1 ID looks like quoted strings; table_2 ID is int64)
p['ID_clean'] = p['ID'].astype(str).str.replace('^"|"$', '', regex=True).str.strip()
l['ID_clean'] = l['ID'].astype(str).str.strip()

# Parse dates
for col in ['First Date', 'Admission']:
    if col in p.columns:
        p[col] = pd.to_datetime(p[col], errors='coerce')
if 'Date' in l.columns:
    l['Date'] = pd.to_datetime(l['Date'], errors='coerce')

# Determine first arrival date per patient (prefer First Date, fallback to Admission)
p['first_arrival'] = p['First Date']
mask_na = p['first_arrival'].isna()
p.loc[mask_na, 'first_arrival'] = p.loc[mask_na, 'Admission']

# Merge labs to patients
merged = pd.merge(l, p[['ID_clean','first_arrival']], left_on='ID_clean', right_on='ID_clean', how='inner')

# Define normal anti-SSA. Treat values like '-', '0', 'neg', 'negative', 'normal', '<=cutoff', or numeric below cutoff as normal; treat '+', 'pos', 'positive', '>cutoff' as abnormal. Missing SSA is excluded.
def ssa_is_normal(val):
    if pd.isna(val):
        return None
    s = str(val).strip().lower()
    if s in {'', 'nan'}:
        return None
    # categorical encodings
    if s in {'-', 'neg', 'negative', 'normal', 'n'}:
        return True
    if s in {'+', 'pos', 'positive', 'p'}:
        return False
    # relational encodings
    if s.startswith('<') or s.startswith('<='):
        return True
    if s.startswith('>') or s.startswith('>='):
        return False
    # try numeric
    try:
        x = float(s)
        # assume titer/units where 0 is negative; without reference, treat 0 as normal, >0 as abnormal
        return x == 0.0
    except Exception:
        return None

merged['ssa_normal'] = merged['SSA'].apply(ssa_is_normal)

# Keep lab records with a determinate SSA status
merged_det = merged[merged['ssa_normal'].isin([True, False])].copy()

# Find patients who have any normal SSA result
normal_ids = merged_det.loc[merged_det['ssa_normal'] == True, 'ID_clean'].dropna().unique()

# Count unique patients with normal SSA whose hospital arrival was before 2000-01-01
cutoff = pd.Timestamp('2000-01-01')
eligible = p[p['ID_clean'].isin(normal_ids) & (p['first_arrival'].notna()) & (p['first_arrival'] < cutoff)]
answer = int(eligible['ID_clean'].nunique())

answer

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
