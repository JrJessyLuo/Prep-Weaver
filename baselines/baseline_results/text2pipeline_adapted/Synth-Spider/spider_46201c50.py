import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['paper_id', 'author_id']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'author_id', 'func': 'def transform(s):\n    # Cast to string and strip surrounding whitespace/quotes; keep characters/digits as-is\n    if s is None:\n        return \'\'\n    s = str(s)\n    s = s.strip()\n    # remove surrounding quotes if present\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1].strip()\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'paper_id', 'dtype': 'str'}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'author_id', 'func': 'def transform(s):\n    s = str(s)\n    s = s.strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'name_email_combined', 'target_columns': ['name_raw', 'email_raw'], 'func': "def transform(s):\n    s = '' if s is None or str(s).lower() == 'nan' else str(s)\n    parts = s.split('|||', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name_raw', 'func': "def transform(s):\n    return '' if s is None or str(s).lower() == 'nan' else str(s).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'email_raw', 'func': "def transform(s):\n    return '' if s is None or str(s).lower() == 'nan' else str(s).strip()"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'name_raw', 'new_name': 'author_name'}, {'old_name': 'email_raw', 'new_name': 'author_email'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['author_id', 'author_name', 'author_email']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    tmp_0 = df.loc[:, ['paper_id', 'author_id']].copy()
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    # Cast to string and strip surrounding whitespace/quotes; keep characters/digits as-is\n    if s is None:\n        return \'\'\n    s = str(s)\n    s = s.strip()\n    # remove surrounding quotes if present\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1].strip()\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['author_id'] = tmp_1['author_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: CastType
    result = tmp_1.copy()
    result['paper_id'] = result['paper_id'].astype(str)
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    s = s.strip()\n    if len(s) >= 2 and s[0] == \'"\' and s[-1] == \'"\':\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['author_id'] = tmp_0['author_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    s = '' if s is None or str(s).lower() == 'nan' else str(s)\n    parts = s.split('|||', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts", globals(), _ns_2)
    _split_func_2 = _ns_2.get('transform') or _ns_2.get('transform') or _ns_2.get('split')
    _split_values_2 = tmp_1['name_email_combined'].apply(_split_func_2)
    _split_values_2 = _split_values_2.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['name_raw'] = _split_values_2.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['email_raw'] = _split_values_2.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return '' if s is None or str(s).lower() == 'nan' else str(s).strip()", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['name_raw'] = tmp_2['name_raw'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return '' if s is None or str(s).lower() == 'nan' else str(s).strip()", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['email_raw'] = tmp_3['email_raw'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'name_raw': 'author_name', 'email_raw': 'author_email'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['author_id', 'author_name', 'author_email']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
tmp_counts = prepared_table_1.groupby('author_id', as_index=False).agg(paper_count=('paper_id', 'nunique'))
integrated = tmp_counts.merge(prepared_table_2, on='author_id', how='left')
result = integrated[integrated['paper_count'] > 50]
# Prefer author_name when available; fall back to author_id
result['author_display'] = result['author_name'].where(result['author_name'].notna() & (result['author_name'].astype(str).str.strip() != ''), result['author_id'])
target = result[['author_display']].drop_duplicates().rename(columns={'author_display': 'author_name'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
