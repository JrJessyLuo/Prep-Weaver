import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'document_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'category_prefix', 'func': 'def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'connector', 'func': 'def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'topic', 'func': 'def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['category_prefix', 'connector', 'topic'], 'target_column': 'document_title', 'func': 'def transform(row):\n    parts = []\n    for c in ["category_prefix", "connector", "topic"]:\n        v = row.get(c)\n        parts.append("" if v is None or (isinstance(v, float) and v != v) else str(v))\n    return (parts[0] + " " + parts[1] + " " + parts[2]).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['document_id', 'document_title']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'document_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'process_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'process_status_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'process_outcome_part1', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'process_outcome_part2', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['process_outcome_part1', 'process_outcome_part2'], 'target_column': 'process_outcome', 'func': "def transform(row):\n    a = '' if row.get('process_outcome_part1') is None else str(row.get('process_outcome_part1'))\n    b = '' if row.get('process_outcome_part2') is None else str(row.get('process_outcome_part2'))\n    return a + b"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['document_id', 'process_id', 'process_status_code', 'process_outcome']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'process_id', 'func': 'def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'process_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'next_process_id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'process_name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'process_description', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['process_id', 'process_name', 'process_description']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['document_id'] = pd.to_numeric(tmp_0['document_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['category_prefix'] = tmp_1['category_prefix'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['connector'] = tmp_2['connector'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    try:\n        return str(s).strip()\n    except Exception:\n        return s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['topic'] = tmp_3['topic'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_4 = {}
    exec('def transform(row):\n    parts = []\n    for c in ["category_prefix", "connector", "topic"]:\n        v = row.get(c)\n        parts.append("" if v is None or (isinstance(v, float) and v != v) else str(v))\n    return (parts[0] + " " + parts[1] + " " + parts[2]).strip()', globals(), _ns_4)
    _concat_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('concat')
    tmp_4['document_title'] = tmp_4[['category_prefix', 'connector', 'topic']].apply(_concat_func_4, axis=1)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['document_id', 'document_title']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['document_id'] = pd.to_numeric(tmp_0['document_id'], errors='coerce').fillna(0).astype(int)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['process_id'] = pd.to_numeric(tmp_1['process_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['process_status_code'] = tmp_2['process_status_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['process_outcome_part1'] = tmp_3['process_outcome_part1'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['process_outcome_part2'] = tmp_4['process_outcome_part2'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: Concatenate
    tmp_5 = tmp_4.copy()
    _ns_4 = {}
    exec("def transform(row):\n    a = '' if row.get('process_outcome_part1') is None else str(row.get('process_outcome_part1'))\n    b = '' if row.get('process_outcome_part2') is None else str(row.get('process_outcome_part2'))\n    return a + b", globals(), _ns_4)
    _concat_func_4 = _ns_4.get('transform') or _ns_4.get('transform') or _ns_4.get('concat')
    tmp_5['process_outcome'] = tmp_5[['process_outcome_part1', 'process_outcome_part2']].apply(_concat_func_4, axis=1)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['document_id', 'process_id', 'process_status_code', 'process_outcome']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    if len(s) >= 2 and ((s[0] == \'"\' and s[-1] == \'"\') or (s[0] == "\'" and s[-1] == "\'")):\n        s = s[1:-1]\n    return s.strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['process_id'] = tmp_0['process_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['process_id'] = pd.to_numeric(tmp_1['process_id'], errors='coerce').fillna(0).astype(int)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['next_process_id'] = pd.to_numeric(tmp_2['next_process_id'], errors='coerce').fillna(0).astype(int)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['process_name'] = tmp_3['process_name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_4['process_description'] = tmp_4['process_description'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['process_id', 'process_name', 'process_description']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='document_id').merge(prepared_table_3, how='left', on='process_id')
mask_exact = integrated['document_title'].astype(str) == 'Travel to Brazil'
result = integrated[mask_exact]
if result.empty:
    # fallback: case-insensitive match allowing variable whitespace
    ci = integrated['document_title'].astype(str).str.replace('\s+', ' ', regex=True).str.strip().str.lower()
    result = integrated[ci == 'travel to brazil']
# Project the process name for the matched document title; keep unique rows
cols = ['document_title', 'process_name']
result = result[cols].drop_duplicates()
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
