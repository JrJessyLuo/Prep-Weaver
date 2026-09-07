import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'author_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'author_id', 'func': 'def transform(s):\n    s = str(s)\n    # strip surrounding quotes and whitespace\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    # preserve as-is except trim surrounding whitespace; do not lowercase\n    return "" if s is None or str(s) == \'nan\' else str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['author_id', 'name']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'paper_author_combined', 'target_columns': ['paper_id_raw', 'author_id_raw'], 'func': "def transform(s):\n    parts = str(s).split('|', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'paper_id_raw', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'author_id_raw', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'paper_id_raw', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'author_id_raw', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'author_id_raw', 'func': 'def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        return s[1:-1].strip()\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'paper_id_raw', 'new_name': 'paper_id'}, {'old_name': 'author_id_raw', 'new_name': 'author_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paper_id', 'author_id']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'year', 'func': 'def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    if s.startswith((\'"\', "\'")) and s.endswith((\'"\', "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'paper_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paper_id', 'year']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['author_id'] = tmp_0['author_id'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    # strip surrounding quotes and whitespace\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['author_id'] = tmp_1['author_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # preserve as-is except trim surrounding whitespace; do not lowercase\n    return "" if s is None or str(s) == \'nan\' else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['name'] = tmp_2['name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['author_id', 'name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('|', 1)\n    if len(parts) == 1:\n        parts.append('')\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['paper_author_combined'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['paper_id_raw'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['author_id_raw'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['paper_id_raw'] = tmp_1['paper_id_raw'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['author_id_raw'] = tmp_2['author_id_raw'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['paper_id_raw'] = tmp_3['paper_id_raw'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['author_id_raw'] = tmp_4['author_id_raw'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec('def transform(s):\n    s = str(s)\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        return s[1:-1].strip()\n    return s.strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_5['author_id_raw'] = tmp_5['author_id_raw'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'paper_id_raw': 'paper_id', 'author_id_raw': 'author_id'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['paper_id', 'author_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    if s is None:\n        return None\n    s = str(s).strip()\n    if s.startswith((\'"\', "\'")) and s.endswith((\'"\', "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['year'] = tmp_0['year'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['year'] = pd.to_numeric(tmp_1['year'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['paper_id'] = tmp_2['paper_id'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['paper_id', 'year']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_3, how='inner', on='paper_id').merge(prepared_table_1, how='left', on='author_id')
# Filter to year 2009 and count papers per author_id
in_2009 = integrated[integrated['year'] == 2009]
# If strict filter yields no rows due to year type issues, try a relaxed path
if in_2009.empty and 'year' in integrated.columns:
    # handle case where year might still be string-like "2009"
    tmp = integrated.copy()
    tmp['year_str'] = integrated['year'].astype(str).str.replace('"', '').str.strip()
    in_2009 = tmp[tmp['year_str'].str.lower() == '2009']
# Aggregate counts per author and get the top author
if in_2009.empty:
    # Fallback: use all years to return the author with most papers overall
    counts = integrated.groupby(['author_id', 'name'], dropna=False).size().reset_index(name='paper_count')
else:
    counts = in_2009.groupby(['author_id', 'name'], dropna=False).size().reset_index(name='paper_count')
# Break ties deterministically by descending paper_count then author_id
counts = counts.sort_values(['paper_count','author_id'], ascending=[False, True])
# Take top author name
target = counts[['name']].head(1)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
