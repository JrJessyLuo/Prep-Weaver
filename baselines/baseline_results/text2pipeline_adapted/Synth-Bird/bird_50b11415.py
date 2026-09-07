import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'convertedManaCost', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'availability', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'convertedManaCost', 'availability', 'faceName', 'asciiName']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fs', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'fs', 'target_columns': ['format', 'status'], 'func': "def transform(s):\n    parts = (s or '').split('|', 1)\n    left = parts[0] if len(parts) > 0 else ''\n    right = parts[1] if len(parts) > 1 else ''\n    return [left, right]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'uuid', 'fs', 'format', 'status']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['convertedManaCost'] = pd.to_numeric(tmp_1['convertedManaCost'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['availability'] = tmp_2['availability'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['id', 'convertedManaCost', 'availability', 'faceName', 'asciiName']].copy()
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
    tmp_1['fs'] = tmp_1['fs'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    parts = (s or '').split('|', 1)\n    left = parts[0] if len(parts) > 0 else ''\n    right = parts[1] if len(parts) > 1 else ''\n    return [left, right]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_2['fs'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['format'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['status'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['id', 'uuid', 'fs', 'format', 'status']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='id')
# Filter to Duel format; prefer explicit 'duel' in format column, fallback to substring match in fs
mask_duel = integrated['format'].str.lower() == 'duel'
if not mask_duel.any():
    mask_duel = integrated['fs'].str.lower().str.contains('duel', na=False)
sub = integrated[mask_duel]
# Prefer legal status; fallback to any status if none marked legal
mask_legal = sub['status'].str.lower() == 'legal'
if mask_legal.any():
    sub = sub[mask_legal]
# Keep rows with non-null numeric CMC
sub = sub.copy()
# Ensure convertedManaCost is numeric (should already be float from preparation)
# Choose a display name: faceName first, else asciiName, else fallback to empty string
name = sub['faceName']
name = name.where(name.notna() & (name.astype(str).str.len() > 0), sub['asciiName'])
sub['card_name'] = name.fillna('')
# If name is still empty, try to use uuid tail as a minimal identifier
empty_name = sub['card_name'].str.len() == 0
if empty_name.any():
    sub.loc[empty_name, 'card_name'] = sub.loc[empty_name, 'uuid'].fillna('').astype(str)
# Rank by highest convertedManaCost
sub = sub.sort_values(by='convertedManaCost', ascending=False)
# Deduplicate by card id to avoid multiple format rows per card
sub = sub.drop_duplicates(subset=['id'])
# Take top 10
target = sub.loc[:, ['card_name', 'convertedManaCost']].head(10)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
