import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'Id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ViewCount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OwnerDisplayName', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'CreaionDate', 'new_name': 'CreationDate'}, {'old_name': 'LasActivityDate', 'new_name': 'LastActivityDate'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Id', 'PostTypeId', 'ViewCount', 'OwnerDisplayName']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'Id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DisplayName', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Id', 'DisplayName']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Id'] = pd.to_numeric(tmp_0['Id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ViewCount'] = pd.to_numeric(tmp_1['ViewCount'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['OwnerDisplayName'] = tmp_2['OwnerDisplayName'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'CreaionDate': 'CreationDate', 'LasActivityDate': 'LastActivityDate'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Id', 'PostTypeId', 'ViewCount', 'OwnerDisplayName']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['Id'] = pd.to_numeric(tmp_0['Id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['DisplayName'] = tmp_1['DisplayName'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['Id', 'DisplayName']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
posts = prepared_table_1.copy()
users = prepared_table_2.copy()
# Merge posts with users to standardize/validate author names before any filtering
integrated = posts.merge(users, how='left', left_on='OwnerDisplayName', right_on='DisplayName')

# Prepare case-insensitive author matching with relaxed handling (strip and casefold)
authors = integrated['OwnerDisplayName'].astype(str).fillna('').str.strip().str.casefold()
views = integrated['ViewCount'].fillna(0)

# Compute total views for Mornington and Amos with broader matching on owner display name
mask_mornington = authors.eq('mornington') | authors.str.contains('^mornington\b', na=False)
mask_amos = authors.eq('amos') | authors.str.contains('^amos\b', na=False)

views_mornington = views[mask_mornington].sum()
views_amos = views[mask_amos].sum()

result = [{'author_pair': 'Mornington - Amos', 'view_count_difference': float(views_mornington - views_amos)}]

target = integrated.iloc[0:0].copy()
for k in result[0:1]:
    pass
# Construct a simple one-row DataFrame without importing pandas by using existing structure
# Create columns and append the single result row
for col in ['author_pair', 'view_count_difference']:
    if col not in target.columns:
        target[col] = []
# Append the result row
row_df = integrated.iloc[0:0].copy()
row_df['author_pair'] = [result[0]['author_pair']]
row_df['view_count_difference'] = [result[0]['view_count_difference']]
# Keep only the result columns
target = row_df[['author_pair', 'view_count_difference']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
