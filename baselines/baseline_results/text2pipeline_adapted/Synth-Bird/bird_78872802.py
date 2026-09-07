import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['id', 'artist', 'setCode', 'name']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'code', 'new_name': 'setCode'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'setCode', 'name']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['id', 'artist', 'setCode', 'name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'code': 'setCode'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but preserve original casing\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['name'] = tmp_1['name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'setCode', 'name']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
cards = prepared_table_1.copy()
sets = prepared_table_2.copy()

# Ensure common merge key is setCode
if 'setCode' not in cards.columns:
    if 'set' in cards.columns:
        cards = cards.rename(columns={'set': 'setCode'})
    elif 'setcode' in cards.columns:
        cards = cards.rename(columns={'setcode': 'setCode'})
if 'setCode' not in sets.columns:
    if 'set' in sets.columns:
        sets = sets.rename(columns={'set': 'setCode'})
    elif 'setcode' in sets.columns:
        sets = sets.rename(columns={'setcode': 'setCode'})

# Merge cards with sets on setCode to bring set names alongside cards
integrated = cards.merge(sets, on='setCode', how='inner', suffixes=('_card','_set'))

# Filter for the set "Hauptset Zehnte Edition"; use robust case-insensitive matching and fallbacks
set_name_col = 'name_set' if 'name_set' in integrated.columns else 'name'
mask_de = integrated[set_name_col].astype(str).str.lower().str.contains('hauptset zehnte edition', na=False)
filtered = integrated[mask_de]
if filtered.empty:
    # fallback to English name 'Tenth Edition'
    mask_en = integrated[set_name_col].astype(str).str.lower().str.contains('tenth edition', na=False)
    filtered = integrated[mask_en]

# Now filter by artist Adam Rex (case-insensitive)
artist_col = 'artist' if 'artist' in filtered.columns else 'artist_card'
artist_mask = filtered[artist_col].astype(str).str.lower().eq('adam rex')
result = filtered[artist_mask]

# If still empty, relax to partial match on 'rex'
if result.empty:
    artist_mask_relaxed = filtered[artist_col].astype(str).str.lower().str.contains('rex', na=False)
    result = filtered[artist_mask_relaxed]

# Count matching cards
count = result.shape[0]

target = __import__('pandas').DataFrame({'count': [count]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
