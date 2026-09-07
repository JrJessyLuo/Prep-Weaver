import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['ID'] = df['ID'].astype(str).str.strip().str.strip('"')
    df['First Date'] = df['First Date'].replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA})
    df['Admission'] = df['Admission'].replace({'-': pd.NA, 'nan': pd.NA, 'NaN': pd.NA, '': pd.NA})
    target = df[['ID','First Date','Admission']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    target = df[['ID','Date','SSA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
