import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Code', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Title_Part1', 'Title_Part2'], 'target_column': 'Title', 'func': "def transform(row):\n    p1 = str(row['Title_Part1']).strip() if row['Title_Part1'] is not None else ''\n    p2 = str(row['Title_Part2']).strip() if row['Title_Part2'] is not None else ''\n    return (p1 + ' ' + p2).strip() if p1 or p2 else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Title', 'func': 'def transform(s):\n    # Trim extraneous whitespace but preserve original case\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Code', 'Title', 'Rating']}, 'table_indices': [0]}], [{'op': 'PassThroughFallback', 'params': {'reason': 'fallback_passthrough_after_pipeline_generation_failure: KeyError: "The following id_vars or value_vars are not present in the DataFrame: [\'Position\', \'Name\', \'Movie\']"', 'source_table': 'table_2'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Code'] = pd.to_numeric(tmp_0['Code'], errors='coerce').fillna(0).astype(int)
    # Step 2: Concatenate
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(row):\n    p1 = str(row['Title_Part1']).strip() if row['Title_Part1'] is not None else ''\n    p2 = str(row['Title_Part2']).strip() if row['Title_Part2'] is not None else ''\n    return (p1 + ' ' + p2).strip() if p1 or p2 else ''", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_1['Title'] = tmp_1[['Title_Part1', 'Title_Part2']].apply(_concat_func_1, axis=1)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # Trim extraneous whitespace but preserve original case\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['Title'] = tmp_2['Title'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['Code', 'Title', 'Rating']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1
sched = prepared_table_2

# Reshape sched from wide to long, then pivot Code rows into columns
long = sched.melt(id_vars=['Code'], var_name='Theater_ID', value_name='Val')
# Separate the two rows by Code value into wide columns
names = long[long['Code'].astype(str).str.casefold().eq('name')][['Theater_ID','Val']].rename(columns={'Val':'Theater_Name'})
movies = long[long['Code'].astype(str).str.casefold().eq('movie')][['Theater_ID','Val']].rename(columns={'Val':'Movie_Code'})
# Merge theater names with movie codes
sched_norm = names.merge(movies, on='Theater_ID', how='inner')

# Clean types: movie codes may be string numbers like '5.0', convert to int safely
mc = sched_norm['Movie_Code'].astype(str).str.strip().str.replace('.0','', regex=False)
sched_norm['Movie_Code_int'] = mc.where(mc.str.fullmatch(r"\d+"), None)
sched_norm = sched_norm.dropna(subset=['Movie_Code_int']).copy()
sched_norm['Movie_Code_int'] = sched_norm['Movie_Code_int'].astype(int)

# Merge with movie titles
integrated = sched_norm.merge(t1, left_on='Movie_Code_int', right_on='Code', how='left')

# Filter for Odeon theater (case-insensitive); relax to contains if strict match yields none
mask_strict = integrated['Theater_Name'].astype(str).str.strip().str.casefold().eq('odeon')
filtered = integrated[mask_strict]
if filtered.empty:
    mask_relax = integrated['Theater_Name'].astype(str).str.casefold().str.contains('odeon')
    filtered = integrated[mask_relax]

# Select unique movie titles
target = filtered[['Title']].dropna().drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
