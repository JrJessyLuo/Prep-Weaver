import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SEX', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Diagnosis', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'combined_dates', 'target_columns': ['birth_date', 'admit_date', 'discharge_date'], 'func': "def transform(s):\n    parts = (str(s) if s is not None else '').split('|')\n    out = []\n    for i in range(3):\n        val = parts[i] if i < len(parts) else ''\n        if val in ['NA', 'NaN', 'nan', 'None', '']:\n            out.append(None)\n        else:\n            out.append(val)\n    return out"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'birth_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'admit_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'discharge_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'SEX', 'Diagnosis', 'birth_date', 'admit_date', 'discharge_date', 'Admission']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'HGB', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'HGB']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SEX'] = tmp_1['SEX'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Diagnosis'] = tmp_2['Diagnosis'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    parts = (str(s) if s is not None else '').split('|')\n    out = []\n    for i in range(3):\n        val = parts[i] if i < len(parts) else ''\n        if val in ['NA', 'NaN', 'nan', 'None', '']:\n            out.append(None)\n        else:\n            out.append(val)\n    return out", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['combined_dates'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['birth_date'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_3['admit_date'] = _split_values_3.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_3['discharge_date'] = _split_values_3.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 5: StandardizeDatetime
    tmp_4 = tmp_3.copy()
    tmp_4['birth_date'] = pd.to_datetime(tmp_4['birth_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['admit_date'] = pd.to_datetime(tmp_5['admit_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['discharge_date'] = pd.to_datetime(tmp_6['discharge_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['ID', 'SEX', 'Diagnosis', 'birth_date', 'admit_date', 'discharge_date', 'Admission']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ID'] = pd.to_numeric(tmp_0['ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['Date'] = pd.to_datetime(tmp_1['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['HGB'] = pd.to_numeric(tmp_2['HGB'], errors='coerce').astype(float)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ID', 'Date', 'HGB']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='ID', how='inner')

# Identify SLE patients with robust case-insensitive matching
sle_mask = integrated['Diagnosis'].astype(str).str.contains('SLE', case=False, na=False)
sle = integrated[sle_mask].copy()

# Normalize sex and ensure HGB numeric
sle['SEX_norm'] = sle['SEX'].astype(str).str.strip().str.upper()
sle['HGB_num'] = pd.to_numeric(sle['HGB'], errors='coerce')

# Normal hemoglobin ranges (typical adult reference)
is_normal_m = (sle['SEX_norm'] == 'M') & sle['HGB_num'].between(13.5, 17.5, inclusive='both')
is_normal_f = (sle['SEX_norm'] == 'F') & sle['HGB_num'].between(12.0, 15.5, inclusive='both')
sle_norm = sle[is_normal_m | is_normal_f].copy()

# Parse dates safely for age computation
sle_norm['Date_dt'] = pd.to_datetime(sle_norm['Date'], errors='coerce')
sle_norm['birth_dt'] = pd.to_datetime(sle_norm['birth_date'], errors='coerce')
sle_norm['admit_dt'] = pd.to_datetime(sle_norm['admit_date'], errors='coerce')

# Compute age at lab when possible; fallback to proxy using admit_date if birth_date missing
sle_norm['age_at_lab'] = ((sle_norm['Date_dt'] - sle_norm['birth_dt']).dt.days) / 365.25
fallback_mask = sle_norm['age_at_lab'].isna()
# If birth_date missing but admit_date exists, approximate by adding (Date - admit_date) to 0; still gives ordering signal
sle_norm.loc[fallback_mask, 'age_at_lab'] = ((sle_norm.loc[fallback_mask, 'Date_dt'] - sle_norm.loc[fallback_mask, 'admit_dt']).dt.days) / 365.25

# Final sort key: use very small value if still NaN so they rank last
sle_norm['age_sort'] = sle_norm['age_at_lab']
sle_norm.loc[sle_norm['age_sort'].isna(), 'age_sort'] = -1e9

# For each patient, pick their maximum observed age among normal-HGB labs
per_patient = sle_norm.sort_values(['ID','age_sort']).groupby('ID', as_index=False).agg({'age_sort':'max', 'SEX':'first'})

# Select the single oldest patient overall
if not per_patient.empty:
    oldest_idx = per_patient['age_sort'].idxmax()
    oldest = per_patient.loc[[oldest_idx], ['ID','SEX']]
else:
    # Fallback: if no normal-HGB SLE rows, relax to any SLE with available HGB and pick the oldest by birth_date
    sle_any = sle.copy()
    sle_any['birth_dt'] = pd.to_datetime(sle_any['birth_date'], errors='coerce')
    sle_any = sle_any.dropna(subset=['birth_dt'])
    if sle_any.empty:
        oldest = sle.head(1)[['ID','SEX']]
    else:
        oldest = sle_any.sort_values('birth_dt', ascending=True).head(1)[['ID','SEX']]

target = oldest.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
