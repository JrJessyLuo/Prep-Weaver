import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SPONSOR_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE', 'FEE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_CATEGORY_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_SPONSOR_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SPONSOR_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['IAP_SUBJECT_SPONSOR_KEY'] = tmp_1['IAP_SUBJECT_SPONSOR_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['FEE'] = pd.to_numeric(tmp_2['FEE'], errors='coerce').astype(float)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_SUBJECT_SPONSOR_KEY', 'ACTIVITY_TITLE', 'FEE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['IAP_CATEGORY_NAME'] = tmp_1['IAP_CATEGORY_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_SPONSOR_KEY'] = tmp_0['IAP_SUBJECT_SPONSOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SPONSOR_NAME'] = tmp_1['SPONSOR_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IAP_SUBJECT_SPONSOR_KEY', 'SPONSOR_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='IAP_SUBJECT_CATEGORY_KEY').merge(prepared_table_3, how='left', on='IAP_SUBJECT_SPONSOR_KEY')
# Compute per-category and sponsor aggregations: number of activities (count distinct titles) and average fee across activities
# Count distinct ACTIVITY_TITLE to represent number of activities; if duplicates exist, they will be de-duplicated by title within the group.
agg = (integrated
       .groupby(['IAP_CATEGORY_NAME', 'SPONSOR_NAME'], dropna=False)
       .agg(num_activities=('ACTIVITY_TITLE', lambda x: x.dropna().nunique()),
            avg_fee=('FEE', 'mean'))
       .reset_index())
# Sort by number of activities descending, then by category and sponsor for stability
agg = agg.sort_values(['num_activities', 'IAP_CATEGORY_NAME', 'SPONSOR_NAME'], ascending=[False, True, True])
# Final projection with requested columns
target = agg[['IAP_CATEGORY_NAME', 'SPONSOR_NAME', 'num_activities', 'avg_fee']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
