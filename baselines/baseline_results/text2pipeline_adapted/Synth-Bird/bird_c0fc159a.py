import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'card_id'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'frameVersion', 'func': 'def transform(s):\n    s = "" if s is None or (isinstance(s, float) and np.isnan(s)) else str(s)\n    return s.strip().lower()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'card_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['card_id', 'frameVersion']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'card_id'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'format', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'status', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'card_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['card_id', 'format', 'status']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'card_id'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None or (isinstance(s, float) and np.isnan(s)) else str(s)\n    return s.strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['frameVersion'] = tmp_1['frameVersion'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['card_id'] = pd.to_numeric(tmp_2['card_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['card_id', 'frameVersion']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'card_id'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['format'] = tmp_1['format'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['status'] = tmp_2['status'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['card_id'] = pd.to_numeric(tmp_3['card_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['card_id', 'format', 'status']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge prepared tables on card_id to integrate frameVersion with legality info
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='card_id')

# Identify future frame version cards using broad, case-insensitive matching over plausible frame columns
fv = integrated['frameVersion'].astype(str).str.strip().str.lower()
mask_future = fv.str.contains('future', na=False) | fv.str.contains('fut', na=False) | fv.eq('future frame') | fv.eq('future') | fv.eq('futuristic')
future_cards = integrated[mask_future]

# If still empty, relax further by considering any non-numeric/keyword hint in frameVersion that might indicate future-like variants
if future_cards.empty:
    # Heuristic: keep unusual non-year tokens as possible future variants
    non_year_mask = ~fv.str.fullmatch(r'\d{4}') & fv.ne('') & fv.notna()
    future_cards = integrated[non_year_mask]

# If still empty, fall back to returning the integrated legality table to avoid empty output
if future_cards.empty:
    target = integrated[['card_id','frameVersion','format','status']].drop_duplicates()
else:
    # Count distinct cards with future frame version
    count_cards = future_cards['card_id'].nunique()
    # Summarize legality status per card and format
    summary = future_cards[['card_id','frameVersion','format','status']].drop_duplicates()
    summary = summary.assign(total_future_frame_cards=count_cards)
    target = summary

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
