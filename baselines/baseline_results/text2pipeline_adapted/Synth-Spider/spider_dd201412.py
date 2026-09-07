import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'name_email_combined', 'target_columns': ['name', 'email'], 'func': "def transform(s):\n    try:\n        if s is None or (isinstance(s, float) and np.isnan(s)):\n            return [None, None]\n        s = str(s)\n        if '|' not in s:\n            return [s if s != '' else None, None]\n        left, right = s.split('|', 1)\n        left = left if left != '' and left.lower() != 'nan' else None\n        right = right if right != '' and right.lower() != 'nan' else None\n        return [left, right]\n    except Exception:\n        return [None, None]"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    import html\n    if s is None or (isinstance(s, float) and np.isnan(s)):\n        return None\n    s = str(s)\n    s = html.unescape(s)\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'author_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['author_id', 'name', 'email']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'aid', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['paper_id', 'aid', 'afid']}, 'table_indices': [0]}], [{'op': 'PassThroughFallback', 'params': {'reason': 'fallback_passthrough_after_pipeline_generation_failure: KeyError: "The following id_vars or value_vars are not present in the DataFrame: [\'paper_id\']"', 'source_table': 'table_3'}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    try:\n        if s is None or (isinstance(s, float) and np.isnan(s)):\n            return [None, None]\n        s = str(s)\n        if '|' not in s:\n            return [s if s != '' else None, None]\n        left, right = s.split('|', 1)\n        left = left if left != '' and left.lower() != 'nan' else None\n        right = right if right != '' and right.lower() != 'nan' else None\n        return [left, right]\n    except Exception:\n        return [None, None]", globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['name_email_combined'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['name'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_0['email'] = _split_values_1.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import html\n    if s is None or (isinstance(s, float) and np.isnan(s)):\n        return None\n    s = str(s)\n    s = html.unescape(s)\n    return s.strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['name'] = tmp_1['name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['author_id'] = pd.to_numeric(tmp_2['author_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['author_id', 'name', 'email']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['aid'] = pd.to_numeric(tmp_0['aid'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['paper_id', 'aid', 'afid']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    result = df.copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
auth = prepared_table_1.copy()
auth_papers = prepared_table_2.copy()
papers_wide = prepared_table_3.copy()

# Reshape papers_wide (wide format with paper IDs as columns and a 'paper_id' row key) to long format
# so we have columns: paper_id, title, venue, year
paper_rows = ['title', 'venue', 'year']
# Ensure only expected keys exist
papers_long_list = []
for row_key in paper_rows:
    if not papers_wide.empty and (papers_wide['paper_id'] == row_key).any():
        row_df = papers_wide[papers_wide['paper_id'] == row_key].drop(columns=['paper_id']).T.reset_index()
        row_df.columns = ['paper_id', row_key]
        papers_long_list.append(row_df)

if papers_long_list:
    # Merge the stacked rows on paper_id to get a tidy papers table
    papers = papers_long_list[0]
    for dfpart in papers_long_list[1:]:
        papers = papers.merge(dfpart, on='paper_id', how='outer')
else:
    # Fallback: create minimal papers table from columns if special rows not found
    # Take all columns except the first identifier column and create empty metadata
    cols = [c for c in papers_wide.columns if c != 'paper_id']
    papers = (
        pd.DataFrame({'paper_id': cols})
        if cols else pd.DataFrame(columns=['paper_id'])
    )
    papers['venue'] = None
    papers['title'] = None
    papers['year'] = None

# Join authors to their papers
ap = auth.merge(auth_papers, left_on='author_id', right_on='aid', how='left')
# Attach paper metadata (including venue)
apv = ap.merge(papers[['paper_id', 'venue', 'title']], on='paper_id', how='left')

# Determine which authors have at least one ACL paper (case-insensitive, look in venue first, then title as fallback)
venue_ci = apv['venue'].astype(str).str.lower()
title_ci = apv['title'].astype(str).str.lower()
apv['is_acl'] = venue_ci.str.contains('acl', na=False) | title_ci.str.contains(' acl', na=False) | title_ci.str.contains('association for computational linguistics', na=False)

# Aggregate to author level
any_acl_by_author = apv.groupby(['author_id', 'name'], dropna=False)['is_acl'].any().reset_index()
any_acl_by_author.rename(columns={'is_acl': 'has_acl'}, inplace=True)

# Include authors without any papers (has_acl will be NaN -> fill as False)
merged = auth.merge(any_acl_by_author, on=['author_id', 'name'], how='left')
merged['has_acl'] = merged['has_acl'].fillna(False)

# Authors who have never published in ACL
never_acl = merged[~merged['has_acl']]

# Final projection: distinct author names
target = never_acl[['name']].drop_duplicates().reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
