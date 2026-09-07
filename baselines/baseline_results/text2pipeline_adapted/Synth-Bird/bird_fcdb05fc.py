import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'gender_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'eye_colour_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'hair_colour_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'skin_colour_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'race_id', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'publisher_id', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'alignment_id', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'race_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'publisher_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'alignment_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'superhero_name', 'func': 'def transform(s):\n    # Trim surrounding whitespace but preserve original case\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'superhero_name', 'gender_id', 'eye_colour_id', 'hair_colour_id', 'skin_colour_id', 'race_id', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg', 'first_name', 'last_name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'hero_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'aid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'av', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['hero_id', 'aid', 'av']}, 'table_indices': [0]}], [{'op': 'PassThroughFallback', 'params': {'reason': 'fallback_passthrough_after_pipeline_generation_failure: ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()', 'source_table': 'table_3'}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'gender', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    t = str(s).strip()\n    t = re.sub(r"\\s+", " ", t)\n    return t'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'gender']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'colour', 'func': 'def transform(s):\n    import re\n    t = str(s)\n    # normalize whitespace\n    t = re.sub(r"\\s+", " ", t.strip())\n    # preserve display casing (no lowercasing)\n    return t'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'colour']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'race', 'func': "def transform(s):\n    import re\n    s = str(s)\n    # preserve exact '-' values\n    if s.strip() == '-':\n        return '-'\n    # normalize whitespace\n    s = re.sub(r'\\s+', ' ', s.strip())\n    # title case words while keeping internal hyphens/spaces\n    def tc(token):\n        return token[:1].upper() + token[1:].lower() if token else token\n    parts = [tc(p) for p in re.split(r'(\\-| )', s)]\n    return ''.join(parts)"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'race']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'publisher_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'publisher_name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'alignment', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()\n"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'alignment']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['gender_id'] = pd.to_numeric(tmp_1['gender_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['eye_colour_id'] = pd.to_numeric(tmp_2['eye_colour_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['hair_colour_id'] = pd.to_numeric(tmp_3['hair_colour_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['skin_colour_id'] = pd.to_numeric(tmp_4['skin_colour_id'], errors='coerce').fillna(0).astype(int)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['race_id'] = pd.to_numeric(tmp_5['race_id'], errors='coerce').astype(float)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['publisher_id'] = pd.to_numeric(tmp_6['publisher_id'], errors='coerce').astype(float)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['alignment_id'] = pd.to_numeric(tmp_7['alignment_id'], errors='coerce').astype(float)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['race_id'] = pd.to_numeric(tmp_8['race_id'], errors='coerce').fillna(0).astype(int)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['publisher_id'] = pd.to_numeric(tmp_9['publisher_id'], errors='coerce').fillna(0).astype(int)
    # Step 11: CastType
    tmp_10 = tmp_9.copy()
    tmp_10['alignment_id'] = pd.to_numeric(tmp_10['alignment_id'], errors='coerce').fillna(0).astype(int)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Trim surrounding whitespace but preserve original case\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_11['superhero_name'] = tmp_11['superhero_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_12['first_name'] = tmp_12['first_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 14: StandardizeString
    tmp_13 = tmp_12.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_13['last_name'] = tmp_13['last_name'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 15: SelectCol
    result = tmp_13.loc[:, ['id', 'superhero_name', 'gender_id', 'eye_colour_id', 'hair_colour_id', 'skin_colour_id', 'race_id', 'publisher_id', 'alignment_id', 'height_cm', 'weight_kg', 'first_name', 'last_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['hero_id'] = pd.to_numeric(tmp_0['hero_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['aid'] = pd.to_numeric(tmp_1['aid'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['av'] = pd.to_numeric(tmp_2['av'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['hero_id', 'aid', 'av']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    t = str(s).strip()\n    t = re.sub(r"\\s+", " ", t)\n    return t', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['gender'] = tmp_1['gender'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'gender']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_6', pd.DataFrame()))

def _prepare_table_5(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    t = str(s)\n    # normalize whitespace\n    t = re.sub(r"\\s+", " ", t.strip())\n    # preserve display casing (no lowercasing)\n    return t', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['colour'] = tmp_1['colour'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'colour']].copy()
    return result

prepared_table_5 = _prepare_table_5(tables.get('table_5', pd.DataFrame()))

def _prepare_table_6(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    s = str(s)\n    # preserve exact '-' values\n    if s.strip() == '-':\n        return '-'\n    # normalize whitespace\n    s = re.sub(r'\\s+', ' ', s.strip())\n    # title case words while keeping internal hyphens/spaces\n    def tc(token):\n        return token[:1].upper() + token[1:].lower() if token else token\n    parts = [tc(p) for p in re.split(r'(\\-| )', s)]\n    return ''.join(parts)", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['race'] = tmp_1['race'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'race']].copy()
    return result

prepared_table_6 = _prepare_table_6(tables.get('table_9', pd.DataFrame()))

def _prepare_table_7(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['publisher_name'] = tmp_1['publisher_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'publisher_name']].copy()
    return result

prepared_table_7 = _prepare_table_7(tables.get('table_8', pd.DataFrame()))

def _prepare_table_8(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    return s.strip()\n", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['alignment'] = tmp_1['alignment'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['id', 'alignment']].copy()
    return result

prepared_table_8 = _prepare_table_8(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
hero = prepared_table_1.copy()
# Join lookups for labels via proper merges
# gender
hero = hero.merge(prepared_table_4.rename(columns={'id':'gender_id'}), on='gender_id', how='left')
# eye colour
eye = prepared_table_5.rename(columns={'id':'eye_colour_id','colour':'eye_colour'})
hero = hero.merge(eye, on='eye_colour_id', how='left')
# hair colour
hair = prepared_table_5.rename(columns={'id':'hair_colour_id','colour':'hair_colour'})
hero = hero.merge(hair, on='hair_colour_id', how='left')
# skin colour
skin = prepared_table_5.rename(columns={'id':'skin_colour_id','colour':'skin_colour'})
hero = hero.merge(skin, on='skin_colour_id', how='left')
# race
race = prepared_table_6.rename(columns={'id':'race_id'})
hero = hero.merge(race, on='race_id', how='left')
# publisher
pub = prepared_table_7.rename(columns={'id':'publisher_id','publisher_name':'publisher'})
hero = hero.merge(pub, on='publisher_id', how='left')
# alignment
align = prepared_table_8.rename(columns={'id':'alignment_id'})
hero = hero.merge(align, on='alignment_id', how='left')

# Prepare attribute lookup from prepared_table_3 which is stored as list-like strings in a single row
attr_raw = prepared_table_3.iloc[0]
# Parse the list-like strings safely by simple cleanup
ids_str = str(attr_raw['id']).strip().strip('[]')
names_str = str(attr_raw['attribute_name']).strip().strip('[]')
ids = [int(x.strip()) for x in ids_str.split(',') if str(x).strip()!='']
# split names by comma, remove quotes and trim
names = [n.strip().strip("'").strip('"') for n in names_str.split(',') if n.strip()!='']
attr_lookup = pd.DataFrame({'aid': ids[:len(names)], 'attribute_name': names[:len(ids)]})

# Long attributes: merge values to names
attr_vals = prepared_table_2.copy()
attr_long = attr_vals.merge(attr_lookup, on='aid', how='left')

# Filter to 3-D Man (robust, case-insensitive)
mask_name = hero['superhero_name'].str.lower() == '3-d man'
if not mask_name.any():
    mask_name = hero['superhero_name'].str.lower().str.contains('3-d', na=False)
hero_3d = hero[mask_name]

# Merge attribute scores for that hero
hero_attr = hero_3d.merge(attr_long, left_on='id', right_on='hero_id', how='left')

# Build scalar attributes as name/value rows
scalar_cols = {
    'Gender':'gender',
    'Eye colour':'eye_colour',
    'Hair colour':'hair_colour',
    'Skin colour':'skin_colour',
    'Race':'race',
    'Publisher':'publisher',
    'Alignment':'alignment',
    'Height (cm)':'height_cm',
    'Weight (kg)':'weight_kg',
    'First name':'first_name',
    'Last name':'last_name'
}
rows = []
for _, r in hero_3d.iterrows():
    for aname, col in scalar_cols.items():
        rows.append({'superhero_name': r['superhero_name'], 'attribute_name': aname, 'value': r[col]})
scalar_df = pd.DataFrame(rows)

# Attribute scores
score_df = hero_attr[['superhero_name','attribute_name','av']].dropna(subset=['attribute_name'])
score_df = score_df.rename(columns={'av':'value'})

# Concatenate scalar and score attributes
all_attrs = pd.concat([scalar_df, score_df], ignore_index=True)

# Final target sorted by attribute name
target = all_attrs.sort_values(['superhero_name','attribute_name']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
