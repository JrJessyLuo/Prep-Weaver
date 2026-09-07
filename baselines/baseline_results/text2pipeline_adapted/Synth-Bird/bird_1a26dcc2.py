import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'CreaionDate', 'new_name': 'CreationDate'}, {'old_name': 'LasActivityDate', 'new_name': 'LastActivityDate'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'PostTypeId', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AcceptedAnswerId', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ViewCount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'AnswerCount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FavoriteCount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'LastEditorUserId', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OwnerUserId', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ParentId', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'Tags', 'func': "def transform(s):\n    return '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)"}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'Tags', 'target_columns': ['tag_list'], 'func': "def transform(s):\n    s = '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)\n    if len(s) == 0:\n        return [[]]\n    if s.startswith('<'):\n        s = s[1:]\n    if s.endswith('>'):\n        s = s[:-1]\n    if len(s) == 0:\n        return [[]]\n    return [s.split('><')]"}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'tag_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'tag_list', 'new_name': 'tag_token'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'tag_token', 'func': "def transform(s):\n    return '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s).lower()"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Id', 'PostTypeId', 'CreationDate', 'Title', 'Tags', 'tag_token']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'CreaionDate': 'CreationDate', 'LasActivityDate': 'LastActivityDate'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Id'] = pd.to_numeric(tmp_1['Id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['PostTypeId'] = pd.to_numeric(tmp_2['PostTypeId'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['AcceptedAnswerId'] = pd.to_numeric(tmp_3['AcceptedAnswerId'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['ViewCount'] = pd.to_numeric(tmp_4['ViewCount'], errors='coerce').astype(float)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['AnswerCount'] = pd.to_numeric(tmp_5['AnswerCount'], errors='coerce').astype(float)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['FavoriteCount'] = pd.to_numeric(tmp_6['FavoriteCount'], errors='coerce').astype(float)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['LastEditorUserId'] = pd.to_numeric(tmp_7['LastEditorUserId'], errors='coerce').astype(float)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['OwnerUserId'] = pd.to_numeric(tmp_8['OwnerUserId'], errors='coerce').astype(float)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['ParentId'] = pd.to_numeric(tmp_9['ParentId'], errors='coerce').astype(float)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_10['Tags'] = tmp_10['Tags'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 12: SplitColumn
    tmp_11 = tmp_10.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s)\n    if len(s) == 0:\n        return [[]]\n    if s.startswith('<'):\n        s = s[1:]\n    if s.endswith('>'):\n        s = s[:-1]\n    if len(s) == 0:\n        return [[]]\n    return [s.split('><')]", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_11['Tags'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_11['tag_list'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 13: Explode
    tmp_12 = tmp_11.explode('tag_list')
    # Step 14: Rename
    tmp_13 = tmp_12.rename(columns={'tag_list': 'tag_token'})
    # Step 15: StandardizeString
    tmp_14 = tmp_13.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return '' if s is None or (isinstance(s, float) and pd.isna(s)) else str(s).lower()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_14['tag_token'] = tmp_14['tag_token'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 16: SelectCol
    result = tmp_14.loc[:, ['Id', 'PostTypeId', 'CreationDate', 'Title', 'Tags', 'tag_token']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
pt = prepared_table_1
# Denominator: number of distinct posts
total_posts = pt[['Id']].drop_duplicates().shape[0]
# Numerator: posts that have R tag (case-insensitive, matched via lowercase tag_token == 'r')
r_posts = pt.loc[pt['tag_token'].str.lower() == 'r', ['Id']].drop_duplicates().shape[0]
# Compute percentage
percentage = (r_posts / total_posts * 100.0) if total_posts > 0 else 0.0
target = pd.DataFrame({'percentage_r_posts': [percentage], 'r_posts': [r_posts], 'total_posts': [total_posts]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
