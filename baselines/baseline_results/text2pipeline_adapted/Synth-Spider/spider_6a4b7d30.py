import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'affiliation_id', 'target_columns': ['affiliation_id'], 'func': 'def transform(s):\n    import re\n    def strip_quotes(x):\n        x = \'\' if x is None else str(x)\n        if len(x) >= 2 and ((x[0] == \'"\' and x[-1] == \'"\') or (x[0] == "\'" and x[-1] == "\'")):\n            return x[1:-1]\n        return x\n    return [strip_quotes(s)]'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'affiliation_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'address', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['affiliation_id', 'name', 'address']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'affiliation_id', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'paper_author_combined', 'target_columns': ['paper_id_raw', 'author_id_raw'], 'func': "def transform(s):\n    parts = str(s).split('||', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'paper_id_raw', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s, float) and s!=s) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'author_id_raw', 'func': 'def transform(s):\n    return None if s is None or (isinstance(s, float) and s!=s) else str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'paper_id_raw', 'new_name': 'paper_id'}, {'old_name': 'author_id_raw', 'new_name': 'author_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['affiliation_id', 'paper_id', 'author_id']}, 'table_indices': [0]}], [{'op': 'SplitColumn', 'params': {'source_column': 'paper_info', 'target_columns': ['paper_id', 'venue', 'year'], 'func': "def transform(s):\n    parts = str(s).split('|')\n    parts = (parts + [None, None, None])[:3]\n    return parts"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'paper_id', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'venue', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'year', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else None'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'year', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paper_id', 'title', 'venue', 'year']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    def strip_quotes(x):\n        x = \'\' if x is None else str(x)\n        if len(x) >= 2 and ((x[0] == \'"\' and x[-1] == \'"\') or (x[0] == "\'" and x[-1] == "\'")):\n            return x[1:-1]\n        return x\n    return [strip_quotes(s)]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['affiliation_id'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['affiliation_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['affiliation_id'] = tmp_1['affiliation_id'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['name'] = tmp_2['name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['address'] = tmp_3['address'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['affiliation_id', 'name', 'address']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['affiliation_id'] = tmp_0['affiliation_id'].astype(str)
    # Step 2: SplitColumn
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('||', 1)\n    if len(parts) == 1:\n        return [parts[0], None]\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_1['paper_author_combined'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_1['paper_id_raw'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_1['author_id_raw'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s, float) and s!=s) else str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['paper_id_raw'] = tmp_2['paper_id_raw'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return None if s is None or (isinstance(s, float) and s!=s) else str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['author_id_raw'] = tmp_3['author_id_raw'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'paper_id_raw': 'paper_id', 'author_id_raw': 'author_id'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['affiliation_id', 'paper_id', 'author_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    parts = str(s).split('|')\n    parts = (parts + [None, None, None])[:3]\n    return parts", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['paper_info'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['paper_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['venue'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    tmp_0['year'] = _split_values_1.apply(lambda x: x[2] if len(x) > 2 else pd.NA)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['paper_id'] = tmp_1['paper_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['venue'] = tmp_2['venue'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else None', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['year'] = tmp_3['year'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['year'] = pd.to_numeric(tmp_4['year'], errors='coerce').fillna(0).astype(int)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['paper_id', 'title', 'venue', 'year']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge author/affiliation-paper links with paper metadata
integrated = prepared_table_2.merge(prepared_table_3, on='paper_id', how='inner')

# Relax filtering: ensure year comparison works even if typed as int/str inconsistently
# prepared_table_3['year'] is int64 per schema; still guard by casting
integrated['year'] = integrated['year'].astype('int64')
integrated_2009 = integrated[integrated['year'] == 2009]

# Bring in affiliation names (may be missing for some rows; keep left to retain possible matches)
integrated_2009 = integrated_2009.merge(prepared_table_1, on='affiliation_id', how='left')

# If affiliation_id is missing but name may still be present (unlikely), keep those with a plausible name; otherwise, fall back later
# Count distinct papers per affiliation-name; if name missing, temporarily fill with 'Unknown Affiliation' to avoid dropping all
integrated_2009['name'] = integrated_2009['name'].fillna('Unknown Affiliation')

paper_counts = (
    integrated_2009
      .drop_duplicates(subset=['affiliation_id', 'name', 'paper_id'])
      .groupby(['affiliation_id', 'name'], as_index=False)['paper_id']
      .count()
      .rename(columns={'paper_id':'paper_count_2009'})
)

# If everything collapsed to Unknown only and there are no meaningful affiliations, broaden by allowing aggregation purely by name fallback
if paper_counts.empty:
    # Fall back to counting distinct papers by any available affiliation name within 2009
    fallback = (
        integrated_2009
          .drop_duplicates(subset=['name', 'paper_id'])
          .groupby(['name'], as_index=False)['paper_id']
          .count()
          .rename(columns={'paper_id':'paper_count_2009'})
    )
    target = fallback.sort_values(['paper_count_2009','name'], ascending=[False, True]).head(3)
else:
    target = paper_counts.sort_values(['paper_count_2009','name'], ascending=[False, True]).head(3)[['name','paper_count_2009']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
