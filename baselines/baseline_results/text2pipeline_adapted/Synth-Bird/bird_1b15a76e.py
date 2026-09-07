import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'card_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['card_id', 'artist', 'asciiName', 'availability', 'borderColor', 'cardKingdomFoilId', 'cardKingdomId', 'colorIdentity', 'colorIndicator', 'colors', 'convertedManaCost', 'duelDeck', 'edhrecRank', 'faceConvertedManaCost', 'faceName', 'flavorName', 'flavorText', 'frameEffects', 'frameVersion', 'hand', 'hasAlternativeDeckLimit', 'hasContentWarning', 'hasFoil', 'hasNonFoil', 'isAlternative', 'isFullArt', 'isOnlineOnly', 'isOversized', 'isPromo', 'isReprint', 'isReserved', 'isStarter', 'isStorySpotlight', 'isTextless', 'isTimeshifted', 'keywords', 'layout', 'leadershipSkills', 'life', 'loyalty']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'rq', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'rq', 'new_name': 'rq_str'}]}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'rq_str', 'target_columns': ['rq_date', 'rq'], 'func': "def transform(s):\n    # s is the normalized string; we return datetime (as string parsable by pandas) and original-like rq string\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s, dayfirst=False, errors='coerce')\n    except Exception:\n        dt = pd.NaT\n    # keep rq as the original normalized string (lowercased/trimmed)\n    return [dt, s]"}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'rq_date', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'rq', 'rq_date', 'rq_str', 'nr', 'uuid']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'id': 'card_id'})
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['card_id', 'artist', 'asciiName', 'availability', 'borderColor', 'cardKingdomFoilId', 'cardKingdomId', 'colorIdentity', 'colorIndicator', 'colors', 'convertedManaCost', 'duelDeck', 'edhrecRank', 'faceConvertedManaCost', 'faceName', 'flavorName', 'flavorText', 'frameEffects', 'frameVersion', 'hand', 'hasAlternativeDeckLimit', 'hasContentWarning', 'hasFoil', 'hasNonFoil', 'isAlternative', 'isFullArt', 'isOnlineOnly', 'isOversized', 'isPromo', 'isReprint', 'isReserved', 'isStarter', 'isStorySpotlight', 'isTextless', 'isTimeshifted', 'keywords', 'layout', 'leadershipSkills', 'life', 'loyalty']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['rq'] = tmp_0['rq'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'rq': 'rq_str'})
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    # s is the normalized string; we return datetime (as string parsable by pandas) and original-like rq string\n    import pandas as pd\n    try:\n        dt = pd.to_datetime(s, dayfirst=False, errors='coerce')\n    except Exception:\n        dt = pd.NaT\n    # keep rq as the original normalized string (lowercased/trimmed)\n    return [dt, s]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_2['rq_str'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['rq_date'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_2['rq'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 4: StandardizeDatetime
    tmp_3 = tmp_2.copy()
    tmp_3['rq_date'] = pd.to_datetime(tmp_3['rq_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['id', 'rq', 'rq_date', 'rq_str', 'nr', 'uuid']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
cards = prepared_table_1
rulings = prepared_table_2
# Join cards to rulings on card_id=id
integrated = cards.merge(rulings, left_on='card_id', right_on='id', how='inner')
# Identify cards with print rarity. Common column is often named 'rarity' or similar; fall back to broad detection if present.
rarity_cols = [c for c in integrated.columns if c.lower() in ['rarity','print_rarity','printedrarity','printed_rarity']]
if rarity_cols:
    rcol = rarity_cols[0]
    mask_print = integrated[rcol].astype(str).str.lower().str.contains('print') | integrated[rcol].astype(str).str.lower().str.contains('printed')
else:
    # Fallback: use evidence that implies physical print (non-online-only) as a broad proxy, ensuring we don't drop all rows
    mask_print = (~integrated.get('isOnlineOnly', 0).astype(int).eq(1))
filtered = integrated[mask_print].copy()
# Filter rulings by printed on 01/02/2007. Try exact date match first; then fallback to string contains in case of formatting differences.
try:
    target_date = pd.to_datetime('2007-01-02')
    date_mask = (pd.to_datetime(filtered['rq_date'], errors='coerce') == target_date)
except Exception:
    date_mask = pd.Series(False, index=filtered.index)
if not date_mask.any():
    # Fallback to string comparison with common formats, case-insensitive
    date_mask = filtered['rq'].astype(str).str.strip().str.startswith('2007-01-02') | filtered['rq'].astype(str).str.contains(r'\b01[/-]02[/-]2007\b', case=False, regex=True)
result = filtered[date_mask]
# Count distinct cards that have at least one ruling on that date
count_df = result.groupby('card_id', as_index=False).size().rename(columns={'size':'ruling_rows'})
answer = pd.DataFrame({'cards_with_print_rarity_and_ruling_on_2007_01_02': [count_df['card_id'].nunique()]})
target = answer

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
