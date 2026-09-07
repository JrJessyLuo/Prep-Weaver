import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'hasContentWarning']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fmt', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'sts', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'fmt', 'sts']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['id', 'hasContentWarning']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['fmt'] = tmp_1['fmt'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['sts'] = tmp_2['sts'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['id', 'fmt', 'sts']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1.copy()
t2 = prepared_table_2.copy()
# Join cards to their format/status entries
merged = t2.merge(t1, on='id', how='inner')
# Filter for commander format (case-insensitive) and legal status (case-insensitive, matching 'legal')
mask_fmt = merged['fmt'].astype(str).str.strip().str.lower() == 'commander'
mask_legal = merged['sts'].astype(str).str.strip().str.lower() == 'legal'
flt = merged[mask_fmt & mask_legal]
# Compute percentage of records without a content warning (hasContentWarning == 0)
if len(flt) == 0:
    # Fallback: if strict match yields none, broaden to rows where fmt contains 'commander' and sts contains 'legal'
    mask_fmt_b = merged['fmt'].astype(str).str.strip().str.lower().str.contains('commander', na=False)
    mask_legal_b = merged['sts'].astype(str).str.strip().str.lower().str.contains('legal', na=False)
    flt = merged[mask_fmt_b & mask_legal_b]
# Calculate percentage
if len(flt) == 0:
    result = 0.0
else:
    no_warning = (flt['hasContentWarning'] == 0).sum()
    result = (no_warning / len(flt)) * 100.0
# Return as a one-row DataFrame with the percentage
target = __import__('pandas').DataFrame({'percentage_without_content_warning': [result]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
