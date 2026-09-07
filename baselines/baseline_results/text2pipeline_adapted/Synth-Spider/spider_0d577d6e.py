import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Code', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Movie', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['Name_Part1', 'Name_Part2'], 'target_column': 'theater_name', 'func': "def transform(row):\n    a = '' if pd.isna(row['Name_Part1']) else str(row['Name_Part1'])\n    b = '' if pd.isna(row['Name_Part2']) else str(row['Name_Part2'])\n    return a + b"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'theater_name', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Code', 'new_name': 'movie_code'}, {'old_name': 'Movie', 'new_name': 'theater_movie_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['movie_code', 'theater_name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Code', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'Code', 'new_name': 'movie_code'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'movie_title', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['movie_code', 'movie_title']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Code'] = pd.to_numeric(tmp_0['Code'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Movie'] = pd.to_numeric(tmp_1['Movie'], errors='coerce').fillna(0).astype(int)
    # Step 3: Concatenate
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec("def transform(row):\n    a = '' if pd.isna(row['Name_Part1']) else str(row['Name_Part1'])\n    b = '' if pd.isna(row['Name_Part2']) else str(row['Name_Part2'])\n    return a + b", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_2['theater_name'] = tmp_2[['Name_Part1', 'Name_Part2']].apply(_concat_func_1, axis=1)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['theater_name'] = tmp_3['theater_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'Code': 'movie_code', 'Movie': 'theater_movie_id'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['movie_code', 'theater_name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Code'] = pd.to_numeric(tmp_0['Code'], errors='coerce').fillna(0).astype(int)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'Code': 'movie_code'})
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['movie_title'] = tmp_2['movie_title'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['movie_code', 'movie_title']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='movie_code')
# Filter theaters Odeon or Imperial with robust case-insensitive matching on the concatenated theater_name
mask_odeon = integrated['theater_name'].str.contains('odeon', case=False, na=False)
mask_imperial = integrated['theater_name'].str.contains('imperial', case=False, na=False)
filtered = integrated[mask_odeon | mask_imperial]
# Project unique movie titles
target = filtered[['movie_title']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
