import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'attribute', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'value', 'func': "def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'value', 'target_columns': ['value'], 'func': "def transform(s):\n    # For language rows: split on commas and trim tokens; for others keep as single-element list\n    import re\n    def clean_token(tok):\n        # trim and collapse internal spaces; preserve case\n        tok = tok.strip()\n        tok = re.sub(r'\\s+', ' ', tok)\n        return tok\n    return [clean_token(x) for x in str(s).split(',')]"}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'value', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'id', 'new_name': 'song_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['song_id', 'attribute', 'value']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'songs_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'participant_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'vsq', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rt', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'sp', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['participant_id', 'songs_id', 'vsq', 'rt', 'sp']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['attribute'] = tmp_1['attribute'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    s = '' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r'\\s+', ' ', s)\n    return s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['value'] = tmp_2['value'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SplitColumn
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    # For language rows: split on commas and trim tokens; for others keep as single-element list\n    import re\n    def clean_token(tok):\n        # trim and collapse internal spaces; preserve case\n        tok = tok.strip()\n        tok = re.sub(r'\\s+', ' ', tok)\n        return tok\n    return [clean_token(x) for x in str(s).split(',')]", globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_3['value'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_3['value'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 5: Explode
    tmp_4 = tmp_3.explode('value')
    # Step 6: Rename
    tmp_5 = tmp_4.rename(columns={'id': 'song_id'})
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['song_id', 'attribute', 'value']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['songs_id'] = pd.to_numeric(tmp_0['songs_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['participant_id'] = pd.to_numeric(tmp_1['participant_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['vsq'] = pd.to_numeric(tmp_2['vsq'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['rt'] = pd.to_numeric(tmp_3['rt'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['sp'] = pd.to_numeric(tmp_4['sp'], errors='coerce').astype(float)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['participant_id', 'songs_id', 'vsq', 'rt', 'sp']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
songs_meta = prepared_table_1
ratings = prepared_table_2
# Join all song attributes to ratings by song_id
joined = ratings.merge(songs_meta, left_on='songs_id', right_on='song_id', how='left')
# Identify rows corresponding to the target song name and English language
# Build a pivot-like filter by aggregating attributes per (songs_id, participant_id)
# First, create flags for name and language matches
jn = joined.copy()
jn['attr_lc'] = jn['attribute'].str.lower()
jn['val_clean'] = jn['value']
# Name match: case-insensitive, trim spaces around the provided title
target_name = 'The Balkan Girls'.strip().lower()
name_match = (jn['attr_lc'] == 'name') & (jn['val_clean'].str.strip().str.lower() == target_name)
# Language match: language attribute containing 'english' (case-insensitive)
language_match = (jn['attr_lc'] == 'language') & (jn['val_clean'].str.strip().str.lower() == 'english')
jn['name_ok'] = name_match
jn['lang_ok'] = language_match
# Aggregate flags per (songs_id, participant_id)
agg_flags = jn.groupby(['songs_id','participant_id'], as_index=False).agg(name_ok=('name_ok','max'), lang_ok=('lang_ok','max'))
full = ratings.merge(agg_flags, on=['songs_id','participant_id'], how='left')
# Filter to rows that match the song name; if that yields none, relax progressively
res = full[full['name_ok'] == True]
if res.empty:
    # try looser name match: substring contains
    tmp = joined[(joined['attribute'].str.lower() == 'name') & (joined['value'].str.contains('balkan girls', case=True, regex=False, na=False))]
    cand_ids = tmp['songs_id'].unique()
    res = full[full['songs_id'].isin(cand_ids)]
# Now, if there are language flags, prefer English; otherwise keep what we have
if 'lang_ok' in res.columns and res['lang_ok'].notna().any():
    en = res[res['lang_ok'] == True]
    if not en.empty:
        res = en
# Project voice sound quality scores
target = res[['participant_id','songs_id','vsq']].rename(columns={'vsq':'voice_sound_quality_score'})
# If duplicates exist, keep all participant scores for the song

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
