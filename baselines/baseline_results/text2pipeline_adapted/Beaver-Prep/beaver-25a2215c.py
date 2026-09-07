import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'PERSON_ROLE', 'func': 'def transform(s):\n    s = str(s)\n    s = s.strip().lower()\n    # title-case while preserving original characters beyond casing\n    return s.title()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'iap_subject_person_key', 'new_name': 'IAP_SUBJECT_PERSON_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_PERSON_KEY', 'PERSON_ROLE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_CANCELLED', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_MULTIPLE_SESSION', 'func': 'def transform(s):\n    return str(s).strip().upper() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_PERSON_KEY', 'IAP_SUBJECT_CATEGORY_KEY', 'FEE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'IAP_SUBJECT_CATEGORY_KEY', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s)).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = str(s)\n    s = s.strip().lower()\n    # title-case while preserving original characters beyond casing\n    return s.title()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['PERSON_ROLE'] = tmp_0['PERSON_ROLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: Rename
    tmp_1 = tmp_0.rename(columns={'iap_subject_person_key': 'IAP_SUBJECT_PERSON_KEY'})
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IAP_SUBJECT_PERSON_KEY', 'PERSON_ROLE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['FEE'] = pd.to_numeric(tmp_0['FEE'], errors='coerce').astype(float)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['IS_CANCELLED'] = tmp_1['IS_CANCELLED'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['IS_MULTIPLE_SESSION'] = tmp_2['IS_MULTIPLE_SESSION'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['IAP_SUBJECT_PERSON_KEY', 'IAP_SUBJECT_CATEGORY_KEY', 'FEE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s)).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['IAP_SUBJECT_CATEGORY_KEY'] = tmp_0['IAP_SUBJECT_CATEGORY_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['IAP_SUBJECT_CATEGORY_KEY', 'IAP_CATEGORY_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', on='IAP_SUBJECT_PERSON_KEY').merge(prepared_table_3, how='inner', on='IAP_SUBJECT_CATEGORY_KEY')
# Group by role and category name to compute count of people (distinct persons per role-category) and average fee
# Use person key to count people; if the same person appears multiple times within the same role-category, count distinct
grp = integrated.groupby(['PERSON_ROLE', 'IAP_CATEGORY_NAME'], as_index=False).agg(role_count=('IAP_SUBJECT_PERSON_KEY', 'nunique'), average_fee=('FEE', 'mean'))
# Sort by role_count descending
result = grp.sort_values(['role_count', 'PERSON_ROLE', 'IAP_CATEGORY_NAME'], ascending=[False, True, True])
# Final projection and column order
target = result[['PERSON_ROLE', 'IAP_CATEGORY_NAME', 'role_count', 'average_fee']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
