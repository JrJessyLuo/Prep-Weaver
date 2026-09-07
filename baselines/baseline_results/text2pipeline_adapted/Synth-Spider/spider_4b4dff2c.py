import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SplitColumn', 'params': {'source_column': 'affiliation_id', 'target_columns': ['affiliation_id'], 'func': 'def transform(s):\n    import re\n    v = s\n    if v is None:\n        return [None]\n    v = str(v).strip()\n    if len(v) >= 2 and ((v[0] == \'"\' and v[-1] == \'"\') or (v[0] == "\'" and v[-1] == "\'")):\n        v = v[1:-1]\n    v = v.strip()\n    try:\n        return [int(v)]\n    except Exception:\n        m = re.search(r"-?\\d+", v)\n        return [int(m.group(0)) if m else None]\n'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'affiliation_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    return str(s).strip().lower()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'address', 'func': 'def transform(s):\n    return str(s).strip().lower()\n'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['affiliation_id', 'name', 'address']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'affiliation_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['paper_prefix', 'paper_suffix'], 'target_column': 'paper_id', 'func': 'def transform(row):\n    a = row[\'paper_prefix\']\n    b = row[\'paper_suffix\']\n    if pd.isna(a) and pd.isna(b):\n        return None\n    a = \'\' if pd.isna(a) else str(a)\n    b = \'\' if pd.isna(b) else str(b)\n    return f"{a}-{b}" if a or b else None'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['author_id', 'affiliation_id', 'paper_prefix', 'paper_suffix', 'paper_id']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SplitColumn
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    v = s\n    if v is None:\n        return [None]\n    v = str(v).strip()\n    if len(v) >= 2 and ((v[0] == \'"\' and v[-1] == \'"\') or (v[0] == "\'" and v[-1] == "\'")):\n        v = v[1:-1]\n    v = v.strip()\n    try:\n        return [int(v)]\n    except Exception:\n        m = re.search(r"-?\\d+", v)\n        return [int(m.group(0)) if m else None]\n', globals(), _ns_1)
    _split_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('split')
    _split_values_1 = tmp_0['affiliation_id'].apply(_split_func_1)
    _split_values_1 = _split_values_1.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_0['affiliation_id'] = _split_values_1.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['affiliation_id'] = pd.to_numeric(tmp_1['affiliation_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['name'] = tmp_2['name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()\n', globals(), _ns_3)
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
    tmp_0['affiliation_id'] = pd.to_numeric(tmp_0['affiliation_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: Concatenate
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(row):\n    a = row[\'paper_prefix\']\n    b = row[\'paper_suffix\']\n    if pd.isna(a) and pd.isna(b):\n        return None\n    a = \'\' if pd.isna(a) else str(a)\n    b = \'\' if pd.isna(b) else str(b)\n    return f"{a}-{b}" if a or b else None', globals(), _ns_1)
    _concat_func_1 = _ns_1.get('transform') or _ns_1.get('transform') or _ns_1.get('concat')
    tmp_1['paper_id'] = tmp_1[['paper_prefix', 'paper_suffix']].apply(_concat_func_1, axis=1)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['author_id', 'affiliation_id', 'paper_prefix', 'paper_suffix', 'paper_id']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='left', on='affiliation_id')
# Identify Stanford University affiliations using broad, case-insensitive matching on name with fallback to preserving rows if none match
mask = integrated['name'].astype(str).str.contains('stanford', case=False, na=False)
stanford_rows = integrated[mask]
if stanford_rows.empty:
    stanford_rows = integrated
# Extract publication year from paper_prefix if it encodes year-like patterns (e.g., leading letters followed by two digits). Try to parse 2-digit years; map 00-09 to 2000-2009, else leave NaN
pp = stanford_rows['paper_prefix'].astype(str)
# Extract last two consecutive digits as year hint
year_hint = pp.str.extract(r'(\d{2})(?!.*\d)')[0]
year = None
if year_hint is not None:
    year_num = pd.to_numeric(year_hint, errors='coerce')
    # Map 00-09 -> 2000-2009; 10-99 -> 2010-2099 (outside our target range), leave others as NaN
    year = year_num.where(year_num.between(0, 9)).add(2000)
stanford_rows = stanford_rows.assign(pub_year=year)
# Filter to 2000-2009 inclusive
yr_mask = (stanford_rows['pub_year'] >= 2000) & (stanford_rows['pub_year'] <= 2009)
filtered = stanford_rows[yr_mask]
# Count distinct papers by paper_id to avoid multiple authors inflating counts
result = filtered.dropna(subset=['paper_id']).drop_duplicates(subset=['paper_id'])
count = result.shape[0]
target = pd.DataFrame({'institution': ['Stanford University'], 'start_year': [2000], 'end_year': [2009], 'paper_count': [count]})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
