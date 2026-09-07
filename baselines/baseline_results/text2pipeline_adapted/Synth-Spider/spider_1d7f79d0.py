import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Concatenate', 'params': {'concatenate_columns': ['lname_part1', 'lname_part2'], 'target_column': 'lname', 'func': "def transform(row):\n    p1 = str(row.get('lname_part1', '') if row.get('lname_part1', '') is not None else '')\n    p2 = str(row.get('lname_part2', '') if row.get('lname_part2', '') is not None else '')\n    return (p1 + ' ' + p2).strip()"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'artistID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'fname', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'lname', 'func': "def transform(s):\n    return '' if s is None else str(s).strip()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['artistID', 'fname', 'lname']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'painterID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['painterID']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'sculptorID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['sculptureID', 'title', 'year', 'medium', 'location']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['sculptorID']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Concatenate
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(row):\n    p1 = str(row.get('lname_part1', '') if row.get('lname_part1', '') is not None else '')\n    p2 = str(row.get('lname_part2', '') if row.get('lname_part2', '') is not None else '')\n    return (p1 + ' ' + p2).strip()", globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_0['lname'] = tmp_0[['lname_part1', 'lname_part2']].apply(_concat_func_1, axis=1)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['artistID'] = pd.to_numeric(tmp_1['artistID'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['fname'] = tmp_2['fname'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return '' if s is None else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['lname'] = tmp_3['lname'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['artistID', 'fname', 'lname']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['painterID'] = pd.to_numeric(tmp_0['painterID'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['painterID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['sculptorID'] = pd.to_numeric(tmp_0['sculptorID'], errors='coerce').fillna(0).astype(int)
    # Step 2: DropColumn
    tmp_1 = tmp_0.drop(columns=['sculptureID', 'title', 'year', 'medium', 'location'], errors='ignore').copy()
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['sculptorID']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
artists = prepared_table_1.copy()
paintings = prepared_table_2.copy()
sculptures = prepared_table_3.copy()
# Identify artists with at least one painting
artists_with_painting = artists.merge(paintings, how='left', left_on='artistID', right_on='painterID')
artists_with_painting['has_painting'] = ~artists_with_painting['painterID'].isna()
artists_with_painting = artists_with_painting[['artistID','fname','lname','has_painting']].drop_duplicates()
# Identify artists with any sculpture by joining on artistID=sculptorID
artists_with_sculpture = artists.merge(sculptures, how='left', left_on='artistID', right_on='sculptorID')
artists_with_sculpture['has_sculpture'] = ~artists_with_sculpture['sculptorID'].isna()
artists_with_sculpture = artists_with_sculpture[['artistID','has_sculpture']].drop_duplicates()
# Combine painting and sculpture flags per artist
combined = artists_with_painting.merge(artists_with_sculpture, on='artistID', how='left')
combined['has_sculpture'] = combined['has_sculpture'].fillna(False)
# Select artists who have painting but no sculpture
result = combined[(combined['has_painting']) & (~combined['has_sculpture'])]
# Final projection: first and last names
target = result[['fname','lname']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
