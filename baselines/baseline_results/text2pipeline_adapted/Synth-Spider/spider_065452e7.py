import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Book_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Pages', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Book_ID', 'Pages', 'Title']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Book_ID', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'rk', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'rk', 'new_name': 'Rank'}]}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['Review_ID', 'rim', 'Rating']}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Book_ID', 'Rank']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Book_ID'] = pd.to_numeric(tmp_0['Book_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Pages'] = pd.to_numeric(tmp_1['Pages'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Book_ID', 'Pages', 'Title']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Book_ID'] = pd.to_numeric(tmp_0['Book_ID'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['rk'] = pd.to_numeric(tmp_1['rk'], errors='coerce').fillna(0).astype(int)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'rk': 'Rank'})
    # Step 4: DropColumn
    tmp_3 = tmp_2.drop(columns=['Review_ID', 'rim', 'Rating'], errors='ignore').copy()
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Book_ID', 'Rank']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
merged = prepared_table_1.merge(prepared_table_2, how='inner', on='Book_ID')
# Identify the book(s) with the minimum number of pages, then report their rank(s)
min_pages = merged['Pages'].min()
result = merged[merged['Pages'] == min_pages][['Title', 'Pages', 'Rank']]
# If multiple, return all; final target is the rank of the smallest-page book(s)
target = result[['Rank']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
