import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'author_id', 'target_columns': ['author_id_clean', 'author_id_int'], 'func': 'def transform(s):\n    try:\n        raw = str(s)\n        # strip surrounding quotes and whitespace\n        stripped = raw.strip().strip(\'"\\\'\')\n        # handle empty or nan-like strings\n        if stripped.lower() in (\'\', \'nan\', \'none\'): \n            return [s, None]\n        # attempt integer parse\n        try:\n            val = int(float(stripped)) if any(ch in stripped for ch in \'.eE\') else int(stripped)\n            return [stripped, val]\n        except Exception:\n            return [stripped, None]\n    except Exception:\n        return [s, None]'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'author_id_int', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': "def transform(s):\n    return None if s is None or str(s).lower() in ('nan','none') else str(s).strip()"}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'author_id_int', 'new_name': 'author_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['author_id', 'name']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'author_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'paper_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': []}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paper_id', 'author_id']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'cited_paper_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'paper_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'paper_id', 'target_columns': ['paper_id_list'], 'func': 'def transform(s):\n    # s is a string like "C08-3004, D09-1141, ..."\n    txt = "" if s is None else str(s)\n    if txt == "" or txt.lower() == "nan":\n        return [[]]\n    parts = [p.strip() for p in txt.split(\',\') if p.strip() != ""]\n    return [parts]'}, 'table_indices': [0]}, {'op': 'Explode', 'params': {'column': 'paper_id_list', 'split_comma': False}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'cited_paper_id', 'new_name': 'paper_id'}, {'old_name': 'paper_id_list', 'new_name': 'citing_paper_id'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paper_id', 'citing_paper_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    try:\n        raw = str(s)\n        # strip surrounding quotes and whitespace\n        stripped = raw.strip().strip(\'"\\\'\')\n        # handle empty or nan-like strings\n        if stripped.lower() in (\'\', \'nan\', \'none\'): \n            return [s, None]\n        # attempt integer parse\n        try:\n            val = int(float(stripped)) if any(ch in stripped for ch in \'.eE\') else int(stripped)\n            return [stripped, val]\n        except Exception:\n            return [stripped, None]\n    except Exception:\n        return [s, None]', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['author_id'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['author_id_clean'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['author_id_int'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['author_id_int'] = pd.to_numeric(tmp_1['author_id_int'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return None if s is None or str(s).lower() in ('nan','none') else str(s).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['name'] = tmp_2['name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: Rename
    tmp_3 = tmp_2.rename(columns={'author_id_int': 'author_id'})
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['author_id', 'name']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['author_id'] = pd.to_numeric(tmp_0['author_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['paper_id'] = tmp_1['paper_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['paper_id', 'author_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['cited_paper_id'] = tmp_0['cited_paper_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['paper_id'] = tmp_1['paper_id'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SplitColumn
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    # s is a string like "C08-3004, D09-1141, ..."\n    txt = "" if s is None else str(s)\n    if txt == "" or txt.lower() == "nan":\n        return [[]]\n    parts = [p.strip() for p in txt.split(\',\') if p.strip() != ""]\n    return [parts]', globals(), _ns_3)
    _split_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('split')
    _split_values_3 = tmp_2['paper_id'].apply(_split_func_3)
    _split_values_3 = _split_values_3.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_2['paper_id_list'] = _split_values_3.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 4: Explode
    tmp_3 = tmp_2.explode('paper_id_list')
    # Step 5: Rename
    tmp_4 = tmp_3.rename(columns={'cited_paper_id': 'paper_id', 'paper_id_list': 'citing_paper_id'})
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['paper_id', 'citing_paper_id']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Start from prepared tables
authors_raw = prepared_table_1.copy()
paper_author = prepared_table_2.copy()
citations_raw = prepared_table_3.copy()

# Disambiguate duplicate column names in authors and citations for reliable merges
# Authors: two 'author_id' columns; keep string one explicitly
au_cols = authors_raw.columns.tolist()
new_au_cols = []
author_id_seen = 0
for c in au_cols:
    if c == 'author_id':
        author_id_seen += 1
        new_au_cols.append('author_id_str' if author_id_seen == 1 else 'author_id_num')
    else:
        new_au_cols.append(c)
authors = authors_raw.copy()
authors.columns = new_au_cols
# Normalize author_id to string key for joining
authors['author_id'] = authors['author_id_str'].astype(str).str.replace('"','', regex=False)

# Citations: two 'paper_id' columns; keep the atomic paper_id as 'paper_id' and the list-like as 'paper_id_list'
ci_cols = citations_raw.columns.tolist()
new_ci_cols = []
paper_id_seen = 0
for c in ci_cols:
    if c == 'paper_id':
        paper_id_seen += 1
        new_ci_cols.append('paper_id' if paper_id_seen == 1 else 'paper_id_list')
    else:
        new_ci_cols.append(c)
citations = citations_raw.copy()
citations.columns = new_ci_cols

# Merge paper-author with citations on paper_id to attribute each citation to all authors of the cited paper
pa_cite = paper_author.merge(citations[['paper_id', 'citing_paper_id']], how='left', on='paper_id')

# Count citations per author (number of citing_paper_id rows)
pa_cite['has_cite'] = pa_cite['citing_paper_id'].notna().astype(int)
author_cites = pa_cite.groupby('author_id', as_index=False)['has_cite'].sum().rename(columns={'has_cite': 'citations'})

# Join with author names
author_cites['author_id'] = author_cites['author_id'].astype(str)
author_stats = author_cites.merge(authors[['author_id', 'name']], how='left', on='author_id')

# If names missing, still proceed; select top by citations, break ties by author_id for determinism
author_stats_sorted = author_stats.sort_values(by=['citations', 'name', 'author_id'], ascending=[False, True, True])

# Fallback: if empty, relax by using author_cites only
if author_stats_sorted.empty:
    author_stats_sorted = author_cites.sort_values(by=['citations', 'author_id'], ascending=[False, True])
    author_stats_sorted = author_stats_sorted.merge(authors[['author_id', 'name']], how='left', on='author_id')

# Final target: top author name and citations
target = author_stats_sorted[['name', 'citations']].head(1)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
