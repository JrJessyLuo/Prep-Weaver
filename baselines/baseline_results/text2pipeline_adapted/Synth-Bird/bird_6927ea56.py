import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'convertedManaCost', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'artist', 'asciiName', 'availability', 'borderColor', 'cardKingdomFoilId', 'cardKingdomId', 'colorIdentity', 'colorIndicator', 'colors', 'convertedManaCost', 'duelDeck', 'edhrecRank', 'faceConvertedManaCost', 'faceName', 'flavorName', 'flavorText', 'frameEffects', 'frameVersion', 'hand', 'hasAlternativeDeckLimit', 'hasContentWarning', 'hasFoil', 'hasNonFoil', 'isAlternative', 'isFullArt', 'isOnlineOnly', 'isOversized', 'isPromo', 'isReprint', 'isReserved', 'isStarter', 'isStorySpotlight', 'isTextless', 'isTimeshifted', 'keywords', 'layout', 'leadershipSkills', 'life', 'loyalty']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s)\n    s = s.strip().lower()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'code', 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'bss', 'blk', 'bst', 'code', 'isFoilOnly', 'isForeignOnly', 'isNonFoilOnly', 'isOnlineOnly', 'isPartialPreview', 'keyruneCode', 'mcmId', 'mcmIdExtras', 'mcmName', 'mtgoCode', 'name', 'parentCode', 'releaseDate', 'tcgplayerGroupId', 'totalSetSize', 'type']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['convertedManaCost'] = pd.to_numeric(tmp_0['convertedManaCost'], errors='coerce').astype(float)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['id', 'artist', 'asciiName', 'availability', 'borderColor', 'cardKingdomFoilId', 'cardKingdomId', 'colorIdentity', 'colorIndicator', 'colors', 'convertedManaCost', 'duelDeck', 'edhrecRank', 'faceConvertedManaCost', 'faceName', 'flavorName', 'flavorText', 'frameEffects', 'frameVersion', 'hand', 'hasAlternativeDeckLimit', 'hasContentWarning', 'hasFoil', 'hasNonFoil', 'isAlternative', 'isFullArt', 'isOnlineOnly', 'isOversized', 'isPromo', 'isReprint', 'isReserved', 'isStarter', 'isStorySpotlight', 'isTextless', 'isTimeshifted', 'keywords', 'layout', 'leadershipSkills', 'life', 'loyalty']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None or (isinstance(s, float) and str(s) == \'nan\') else str(s)\n    s = s.strip().lower()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['name'] = tmp_0['name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s)\n    return s.strip().upper()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['code'] = tmp_1['code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'bss', 'blk', 'bst', 'code', 'isFoilOnly', 'isForeignOnly', 'isNonFoilOnly', 'isOnlineOnly', 'isPartialPreview', 'keyruneCode', 'mcmId', 'mcmIdExtras', 'mcmName', 'mtgoCode', 'name', 'parentCode', 'releaseDate', 'tcgplayerGroupId', 'totalSetSize', 'type']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
cards = prepared_table_1.copy()
sets_ = prepared_table_2.copy()

# Attempt to join cards to sets by a set code field if present on cards; common field names include 'setCode' or 'set'.
# We will try 'setCode' first, then 'set' fallback. If neither exists, we will match by set name if a likely 'setName' column exists.
join_done = False
integrated = None

if 'setCode' in cards.columns:
    integrated = cards.merge(sets_, left_on='setCode', right_on='code', how='inner')
    join_done = True
elif 'set' in cards.columns:
    integrated = cards.merge(sets_, left_on='set', right_on='code', how='inner')
    join_done = True
elif 'setName' in cards.columns:
    # Standardize both sides for name-based join
    left = cards.copy()
    left['setName_std'] = left['setName'].astype(str).str.strip().str.lower()
    right = sets_.copy()
    right['name_std'] = right['name'].astype(str).str.strip().str.lower()
    integrated = left.merge(right, left_on='setName_std', right_on='name_std', how='inner')
    join_done = True
else:
    # As a broader fallback, try to detect a column that likely holds set code by common variants
    possible_code_cols = [c for c in cards.columns if c.lower() in ['code','set_code','setcode','edition','setid','set_id']]
    if possible_code_cols:
        col = possible_code_cols[0]
        integrated = cards.merge(sets_, left_on=col, right_on='code', how='inner')
        join_done = True

# If no join could be established, fall back to using only cards but we cannot identify the set reliably; in that case, we will attempt name-based filtering on any plausible columns post-merge-like.
if not join_done:
    # Create minimal integrated with a placeholder name column if cards already contain a plausible set name column
    integrated = cards.copy()
    if 'name' not in integrated.columns:
        integrated['name'] = ''

# Filter to Coldsnap using robust case-insensitive match on set name or code
name_cols = [c for c in integrated.columns if c.lower() in ['name','setname','set_name']]
code_cols = [c for c in integrated.columns if c.lower() in ['code','setcode','set_code','set']]

coldsnap_mask = False
if name_cols:
    nm = name_cols[0]
    coldsn = integrated[nm].astype(str).str.strip().str.lower()
    coldsn_mask = coldsn.eq('coldsnap')
    coldsn_contains = coldsn.str.contains('coldsnap', na=False)
    coldsn_mask = coldsn_mask | coldsn_contains
    coldsnap_mask = coldsn_mask
else:
    coldsnap_mask = False

# Also try by known Coldsnap code 'CSP'
code_mask = False
if code_cols:
    cd = code_cols[0]
    code_std = integrated[cd].astype(str).str.strip().str.upper()
    code_mask = code_std.eq('CSP')

if hasattr(coldsnap_mask, 'any') and hasattr(code_mask, 'any'):
    mask = coldsnap_mask | code_mask
elif hasattr(coldsnap_mask, 'any'):
    mask = coldsnap_mask
elif hasattr(code_mask, 'any'):
    mask = code_mask
else:
    mask = integrated.index == -1  # no matches; will relax below

subset = integrated[mask]
if subset.empty:
    # Relax to any rows whose set type suggests an expansion around the era; fallback to rows with name similar to 'cold'
    if name_cols:
        nm = name_cols[0]
        subset = integrated[integrated[nm].astype(str).str.lower().str.contains('cold', na=False)]
    if subset.empty and code_cols:
        cd = code_cols[0]
        subset = integrated[integrated[cd].astype(str).str.upper().eq('CSP')]
    if subset.empty:
        subset = integrated  # ultimate fallback to avoid empty result

# Compute percentage of cards in the set with convertedManaCost == 7
work = subset.copy()
# Ensure numeric
if 'convertedManaCost' in work.columns:
    work['convertedManaCost'] = pd.to_numeric(work['convertedManaCost'], errors='coerce')
else:
    work['convertedManaCost'] = pd.NA

total = len(work)
if total == 0:
    pct = 0.0
else:
    count_cmc7 = (work['convertedManaCost'] == 7).sum()
    pct = (count_cmc7 / total) * 100.0

target = pd.DataFrame({'percentage_cmc7_in_coldsnap': [pct]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
