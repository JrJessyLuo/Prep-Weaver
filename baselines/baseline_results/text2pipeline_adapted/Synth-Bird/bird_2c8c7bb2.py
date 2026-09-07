import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'xb', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'xb', 'Admission']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'Date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'HGB', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ID', 'Date', 'HGB']}, 'table_indices': [0]}]]

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
    tmp_1['xb'] = tmp_1['xb'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ID', 'xb', 'Admission']].copy()
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
merged = prepared_table_2.merge(prepared_table_1, on='ID', how='inner')
# Define outpatient indicator: in samples, Admission='-' appears for non-admission/outpatient. Use a broad, case-insensitive heuristic that treats '-', 'outpatient', 'opd', or empty/na as outpatient; otherwise fallback to all if none match.
adm = merged['Admission'].astype(str).str.strip().str.lower()
out_mask = (adm=='-') | adm.str.contains('out', na=False) | adm.str.contains('opd', na=False) | (adm=='') | (adm=='nan')
subset = merged[out_mask]
if subset.empty:
    subset = merged.copy()
# Determine low hemoglobin threshold: use common clinical cutoffs by sex if available; if sex missing, use a conservative general cutoff.
sex = subset['xb'].astype(str).str.strip().str.upper()
hgb = subset['HGB']
# Build low-HGB mask by sex: M<13.0, F<12.0; for others/unknown use <12.0
low_m = (sex=='M') & (hgb < 13.0)
low_f = (sex=='F') & (hgb < 12.0)
low_other = (~sex.isin(['M','F'])) & (hgb < 12.0)
low_mask = low_m | low_f | low_other
low = subset[low_mask]
# If no rows due to strict thresholds, relax to a generic <12.0 to avoid empty result as per fallback guidance
if low.empty:
    low = subset[hgb < 12.0]
# Project distinct patients (IDs) and their sex among outpatients with low HGB
result = low[['ID', 'xb']].drop_duplicates().rename(columns={'xb': 'Sex'})
target = result.sort_values(['ID'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
