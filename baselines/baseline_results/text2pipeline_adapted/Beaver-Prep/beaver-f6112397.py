import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'MAX_ENROLLMENT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'TERM_CODE', 'MAX_ENROLLMENT', 'FEE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'ACADEMIC_YEAR']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['MAX_ENROLLMENT'] = pd.to_numeric(tmp_0['MAX_ENROLLMENT'], errors='coerce').astype(float)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['FEE'] = pd.to_numeric(tmp_1['FEE'], errors='coerce').astype(float)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['IAP_SUBJECT_CATEGORY_KEY'] = tmp_3['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'TERM_CODE', 'MAX_ENROLLMENT', 'FEE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['ACADEMIC_YEAR'] = pd.to_numeric(tmp_1['ACADEMIC_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['TERM_CODE', 'ACADEMIC_YEAR']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
tmp = prepared_table_1.merge(prepared_table_3, how='left', on='TERM_CODE').merge(prepared_table_2, how='left', on='IAP_SUBJECT_CATEGORY_KEY')
# Aggregate per category and academic year
agg = tmp.groupby(['IAP_CATEGORY_NAME', 'ACADEMIC_YEAR'], dropna=False).agg(
    total_fee_collected=('FEE', 'sum'),
    total_number_of_IAP_subjects=('TERM_CODE', 'count'),
    minimum_enrollment=('MAX_ENROLLMENT', 'min'),
    maximum_enrollment=('MAX_ENROLLMENT', 'max')
).reset_index()
# Final projection and ordering
cols = ['IAP_CATEGORY_NAME', 'ACADEMIC_YEAR', 'total_fee_collected', 'total_number_of_IAP_subjects', 'minimum_enrollment', 'maximum_enrollment']
target = agg[cols].sort_values(['IAP_CATEGORY_NAME', 'ACADEMIC_YEAR'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
