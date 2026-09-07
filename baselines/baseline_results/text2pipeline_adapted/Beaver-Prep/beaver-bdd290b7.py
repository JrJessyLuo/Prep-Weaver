import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'IAP_SUBJECT_PERSON_KEY', 'new_name': 'iap_subject_person_key'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MAX_ENROLLMENT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['iap_subject_person_key', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['iap_subject_person_key', 'PERSON_EMAIL', 'PERSON_NAME']}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'PERSON_EMAIL', 'func': "def transform(s):\n    s = '' if s is None else str(s)\n    if s.lower() == 'nan':\n        return ''\n    return s.strip().lower()"}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'IAP_SUBJECT_PERSON_KEY': 'iap_subject_person_key'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MAX_ENROLLMENT'] = pd.to_numeric(tmp_1['MAX_ENROLLMENT'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['FEE'] = pd.to_numeric(tmp_2['FEE'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['TERM_CODE'] = tmp_3['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['iap_subject_person_key', 'TERM_CODE', 'FEE', 'MAX_ENROLLMENT']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: SelectCol
    tmp_0 = df.loc[:, ['iap_subject_person_key', 'PERSON_EMAIL', 'PERSON_NAME']].copy()
    # Step 2: StandardizeString
    result = tmp_0.copy()
    _ns_1 = {}
    exec("def transform(s):\n    s = '' if s is None else str(s)\n    if s.lower() == 'nan':\n        return ''\n    return s.strip().lower()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    result['PERSON_EMAIL'] = result['PERSON_EMAIL'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='iap_subject_person_key', how='left')
# Aggregate per individual and academic year
agg = integrated.groupby(['iap_subject_person_key', 'PERSON_EMAIL', 'PERSON_NAME', 'TERM_CODE'], as_index=False).agg(
    total_iap_subjects=('TERM_CODE', 'size'),
    min_fee=('FEE', 'min'),
    max_fee=('FEE', 'max'),
    total_course_enrollment=('MAX_ENROLLMENT', 'sum')
)
# Project final columns with readable names
agg = agg.rename(columns={
    'PERSON_EMAIL': 'email',
    'PERSON_NAME': 'name',
    'TERM_CODE': 'academic_year'
})
# Select final columns
target = agg[['iap_subject_person_key', 'email', 'name', 'academic_year', 'total_iap_subjects', 'min_fee', 'max_fee', 'total_course_enrollment']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
