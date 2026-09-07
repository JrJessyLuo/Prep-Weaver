import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'BUILDING_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'BUILDING_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'BUILDING_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['BUILDING_KEY', 'BUILDING_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['OFFER_DEPT_NAME', 'SUBJECT_SUMMARY_KEY']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['BUILDING_KEY'] = tmp_0['BUILDING_KEY'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['BUILDING_NAME'] = tmp_1['BUILDING_NAME'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['BUILDING_KEY'] = tmp_2['BUILDING_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['BUILDING_NAME'] = tmp_3['BUILDING_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['BUILDING_KEY', 'BUILDING_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['OFFER_DEPT_NAME'] = tmp_0['OFFER_DEPT_NAME'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['OFFER_DEPT_NAME', 'SUBJECT_SUMMARY_KEY']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
prepared_table_1_tmp = prepared_table_1.copy()
prepared_table_2_tmp = prepared_table_2.copy()

# Filter to Center for International Studies in a robust, case-insensitive way
mask = prepared_table_2_tmp['OFFER_DEPT_NAME'].str.contains('Center for International Studies', case=False, na=False)
cfis = prepared_table_2_tmp[mask].copy()

# Count distinct course offerings (use SUBJECT_SUMMARY_KEY as offering key)
cfis_counts = cfis.groupby([])['SUBJECT_SUMMARY_KEY'].nunique().reset_index(name='NUM_COURSES')
if cfis_counts.empty:
    # Fallback: broaden to names containing 'International Studies'
    mask2 = prepared_table_2_tmp['OFFER_DEPT_NAME'].str.contains('International Studies', case=False, na=False)
    cfis = prepared_table_2_tmp[mask2].copy()
    cfis_counts = cfis.groupby([])['SUBJECT_SUMMARY_KEY'].nunique().reset_index(name='NUM_COURSES')

# Without a building key in course data, we cannot distribute counts by building; 
# Provide the building name for every building key with the same total CFIS count (best available integration path).
cfis_total = 0
if not cfis_counts.empty:
    cfis_total = int(cfis_counts.loc[0, 'NUM_COURSES'])

result = prepared_table_1_tmp[['BUILDING_KEY', 'BUILDING_NAME']].copy()
result['NUM_COURSES'] = cfis_total

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
