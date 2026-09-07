import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'availability', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'layout', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'isStarter', 'availability', 'layout']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'id', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'code', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'name', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'type', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['id', 'code', 'name', 'type']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['availability'] = tmp_1['availability'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['layout'] = tmp_2['layout'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['id', 'isStarter', 'availability', 'layout']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['id'] = pd.to_numeric(tmp_0['id'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['code'] = tmp_1['code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['name'] = tmp_2['name'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_3['type'] = tmp_3['type'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['id', 'code', 'name', 'type']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
prepared_cols = [c for c in prepared_table_1.columns if c.lower() in ['id','isstarter','availability','layout'] or 'legal' in c.lower()]
pt1 = prepared_table_1[prepared_cols].copy()
# Identify the legality-status column: prefer a structured 'legalities' dict-like/text column; else fall back to any column containing 'legal'.
legal_cols = [c for c in pt1.columns if 'legal' in c.lower()]
# Build a single text column to search for 'restricted'
if legal_cols:
    legal_text = pt1[legal_cols].astype(str).agg(' '.join, axis=1)
else:
    legal_text = pt1.apply(lambda r: '', axis=1)
# Starter deck indicator: use isStarter == 1. Some datasets may encode as 1/0 ints.
starter_mask = pt1['isStarter'] == 1 if 'isStarter' in pt1.columns else False
restricted_mask = legal_text.str.contains('restricted', case=False, na=False)
result = pt1[starter_mask & restricted_mask].copy()
# Count distinct cards by id
count_df = result[['id']].drop_duplicates()
count_df['count'] = 1
agg = count_df['count'].sum()
target = count_df.iloc[:0].copy()
target['restricted_starter_count'] = [agg]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
