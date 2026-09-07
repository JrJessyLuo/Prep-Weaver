import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'artistID', 'new_name': 'artist_id'}, {'old_name': 'fname', 'new_name': 'first_name'}, {'old_name': 'lname', 'new_name': 'last_name'}, {'old_name': 'deathYear', 'new_name': 'death_year'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'artist_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'birth_year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'death_year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'first_name', 'func': "def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = s.replace('\\u00A0',' ')\n    s = re.sub(r'\\s+', ' ', s).strip()\n    return s"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'last_name', 'func': "def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = s.replace('\\u00A0',' ')\n    s = re.sub(r'\\s+', ' ', s).strip()\n    return s"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['quote_start', 'quote_end']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['artist_id', 'first_name', 'last_name', 'birth_year', 'death_year']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'sculptureID', 'new_name': 'sculpture_id'}, {'old_name': 'sculptorID', 'new_name': 'sculptor_id'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'sculpture_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'sculptor_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'title', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'medium', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'location', 'func': 'def transform(s):\n    import re\n    if s is None or str(s).lower() == \'nan\':\n        return \'\'\n    s = str(s).strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['sculpture_id', 'title', 'year', 'medium', 'location', 'sculptor_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'artistID': 'artist_id', 'fname': 'first_name', 'lname': 'last_name', 'deathYear': 'death_year'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['artist_id'] = pd.to_numeric(tmp_1['artist_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['birth_year'] = pd.to_numeric(tmp_2['birth_year'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['death_year'] = pd.to_numeric(tmp_3['death_year'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec("def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = s.replace('\\u00A0',' ')\n    s = re.sub(r'\\s+', ' ', s).strip()\n    return s", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['first_name'] = tmp_4['first_name'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec("def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = s.replace('\\u00A0',' ')\n    s = re.sub(r'\\s+', ' ', s).strip()\n    return s", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['last_name'] = tmp_5['last_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: DropColumn
    tmp_6 = tmp_5.drop(columns=['quote_start', 'quote_end'], errors='ignore').copy()
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['artist_id', 'first_name', 'last_name', 'birth_year', 'death_year']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'sculptureID': 'sculpture_id', 'sculptorID': 'sculptor_id'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['sculpture_id'] = pd.to_numeric(tmp_1['sculpture_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['year'] = pd.to_numeric(tmp_2['year'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['sculptor_id'] = pd.to_numeric(tmp_3['sculptor_id'], errors='coerce').fillna(0).astype(int)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['title'] = tmp_4['title'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['medium'] = tmp_5['medium'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    if s is None or str(s).lower() == \'nan\':\n        return \'\'\n    s = str(s).strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['location'] = tmp_6['location'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['sculpture_id', 'title', 'year', 'medium', 'location', 'sculptor_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', left_on='sculptor_id', right_on='artist_id')
# Treat all rows in table_2 as sculptures by definition; filter by year < 1900
filtered = integrated[integrated['year'] < 1900]
# Distinct artists with first and last names
result = filtered[['first_name', 'last_name']].drop_duplicates()
target = result.reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
