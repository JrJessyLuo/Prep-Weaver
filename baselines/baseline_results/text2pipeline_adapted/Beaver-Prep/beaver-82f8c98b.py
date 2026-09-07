import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY', 'ISBN', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': "def transform(s):\n    return ('' if s is None else str(s)).strip()"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': "def transform(s):\n    return ('' if s is None or str(s).lower()=='nan' else str(s)).strip()"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NEW_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'USED_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RENTAL_NEW_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RENTAL_USED_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER', 'YEAR', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'RENTAL_NEW_PRICE', 'RENTAL_USED_PRICE', 'MATERIAL_INFO_SOURCE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_2['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['subject_id'] = tmp_2['subject_id'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['ISBN'] = tmp_3['ISBN'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['TIP_MATERIAL_KEY'] = tmp_4['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['RECORD_COUNT'] = pd.to_numeric(tmp_5['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'subject_id', 'TIP_MATERIAL_KEY', 'ISBN', 'TIP_MATERIAL_STATUS_KEY', 'RECORD_COUNT']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return ('' if s is None else str(s)).strip()", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_MATERIAL_KEY'] = tmp_0['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return ('' if s is None or str(s).lower()=='nan' else str(s)).strip()", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['ISBN'] = tmp_1['ISBN'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['YEAR'] = pd.to_numeric(tmp_2['YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['NEW_SHELF_PRICE'] = pd.to_numeric(tmp_3['NEW_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['USED_SHELF_PRICE'] = pd.to_numeric(tmp_4['USED_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['RENTAL_NEW_PRICE'] = pd.to_numeric(tmp_5['RENTAL_NEW_PRICE'], errors='coerce').astype(float)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['RENTAL_USED_PRICE'] = pd.to_numeric(tmp_6['RENTAL_USED_PRICE'], errors='coerce').astype(float)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER', 'YEAR', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'RENTAL_NEW_PRICE', 'RENTAL_USED_PRICE', 'MATERIAL_INFO_SOURCE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1.copy()
t2 = prepared_table_2.copy()
t3 = prepared_table_3.copy()

# Primary join on TIP_SUBJECT_OFFERED_KEY
j1 = t2.merge(t1, how='left', on='TIP_SUBJECT_OFFERED_KEY', suffixes=('_t2', '_t1'))

# Identify rows from t2 that did not match t1 on primary key
unmatched = j1[j1['OFFER_DEPT_NAME'].isna()]
matched = j1[~j1['OFFER_DEPT_NAME'].isna()]

# Fallback join for unmatched using subject_id to SUBJECT_ID
if not unmatched.empty:
    # keep only the columns from unmatched needed to merge without colliding with t1 columns, then merge by subject id
    cols_to_keep = [c for c in unmatched.columns if c not in t1.columns or c in ['subject_id','TIP_MATERIAL_KEY','ISBN','TIP_MATERIAL_STATUS_KEY','RECORD_COUNT','TERM_CODE_t2','TIP_SUBJECT_OFFERED_KEY']]
    fb_src = unmatched[cols_to_keep].copy()
    fb = fb_src.merge(t1, how='left', left_on='subject_id', right_on='SUBJECT_ID', suffixes=('', '_t1fb'))
    combined = pd.concat([matched, fb], ignore_index=True, sort=False)
else:
    combined = matched.copy()

# Join materials/prices
combined_prices = combined.merge(t3[['TIP_MATERIAL_KEY','RENTAL_NEW_PRICE']], how='left', on='TIP_MATERIAL_KEY')

# Ensure proper types
if combined_prices['NUM_ENROLLED_STUDENTS'].dtype != 'int64':
    combined_prices['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(combined_prices['NUM_ENROLLED_STUDENTS'], errors='coerce')

# Baseline from table_1
dept_baseline = t1[['OFFER_DEPT_NAME','SUBJECT_ID','NUM_ENROLLED_STUDENTS']].copy()
if dept_baseline['NUM_ENROLLED_STUDENTS'].dtype != 'int64':
    dept_baseline['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(dept_baseline['NUM_ENROLLED_STUDENTS'], errors='coerce')

# Aggregate from combined_prices (has prices and subject linkage from t2/t3)
agg_from_prices = combined_prices.groupby('OFFER_DEPT_NAME', dropna=False).agg(
    types_of_tip_subjects=('SUBJECT_ID', lambda x: x.nunique()),
    total_enrolled_students=('NUM_ENROLLED_STUDENTS', 'sum'),
    min_rental_new_price=('RENTAL_NEW_PRICE', 'min'),
    max_rental_new_price=('RENTAL_NEW_PRICE', 'max')
).reset_index()

# Aggregate baseline directly from table_1 to ensure departments without any t2 linkage are not lost
agg_baseline = dept_baseline.groupby('OFFER_DEPT_NAME', dropna=False).agg(
    types_of_tip_subjects=('SUBJECT_ID', lambda x: x.nunique()),
    total_enrolled_students=('NUM_ENROLLED_STUDENTS', 'sum')
).reset_index()

# Merge the two aggregations, preferring price stats from agg_from_prices
target = agg_baseline.merge(
    agg_from_prices[['OFFER_DEPT_NAME','min_rental_new_price','max_rental_new_price']],
    how='left', on='OFFER_DEPT_NAME'
)

# Final column names per question
target = target.rename(columns={
    'OFFER_DEPT_NAME': 'department_name',
    'types_of_tip_subjects': 'total_types_of_tip_subjects',
    'total_enrolled_students': 'total_enrolled_students',
    'min_rental_new_price': 'min_rental_new_price',
    'max_rental_new_price': 'max_rental_new_price'
})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
