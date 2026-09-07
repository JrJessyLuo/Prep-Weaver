import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'Id', 'func': 'def transform(s):\n    s = str(s)\n    if s.startswith(\'"\') and s.endswith(\'"\') and len(s) >= 2:\n        s = s[1:-1]\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'Id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ViewCount', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CommentCount', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['Id', 'ViewCount', 'CommentCount']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    if s.startswith(\'"\') and s.endswith(\'"\') and len(s) >= 2:\n        s = s[1:-1]\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['Id'] = tmp_0['Id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['Id'] = tmp_1['Id'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ViewCount'] = pd.to_numeric(tmp_2['ViewCount'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['CommentCount'] = pd.to_numeric(tmp_3['CommentCount'], errors='coerce').fillna(0).astype(int)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['Id', 'ViewCount', 'CommentCount']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()
# Find the post with ViewCount == 1910 (exact match on float after casting)
match = df[df['ViewCount'] == 1910]
if match.empty:
    # Fallback: try close integer match if stored as int-like float
    match = df[(df['ViewCount'].round(0) == 1910)]
# If still empty, fallback to nearest by absolute difference
if match.empty:
    df_nonnull = df[df['ViewCount'].notna()].copy()
    if not df_nonnull.empty:
        df_nonnull['abs_diff'] = (df_nonnull['ViewCount'] - 1910).abs()
        match = df_nonnull.sort_values('abs_diff').head(1)
    else:
        match = df.head(0)
# Project the answer: Id and CommentCount
target = match[['Id','CommentCount']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
