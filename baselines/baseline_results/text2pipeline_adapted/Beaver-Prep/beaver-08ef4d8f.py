import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    return str(s).strip()\n'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'subject_id', 'new_name': 'SUBJECT_ID'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'OFFER_SCHOOL_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NEW_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'USED_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_MATERIAL_KEY', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'tip_material_status_key', 'new_name': 'TIP_MATERIAL_STATUS_KEY'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_STATUS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TIP_MATERIAL_KEY'] = tmp_1['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['TIP_MATERIAL_STATUS_KEY'] = tmp_2['TIP_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['TERM_CODE'] = tmp_3['TERM_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['subject_id'] = tmp_4['subject_id'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()\n', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['ISBN'] = tmp_5['ISBN'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'subject_id': 'SUBJECT_ID'})
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

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
    tmp_2['COURSE_NUMBER'] = tmp_2['COURSE_NUMBER'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['SUBJECT_ID'] = tmp_3['SUBJECT_ID'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['SUBJECT_TITLE'] = tmp_4['SUBJECT_TITLE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['OFFER_SCHOOL_NAME'] = tmp_5['OFFER_SCHOOL_NAME'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'COURSE_NUMBER', 'SUBJECT_TITLE', 'OFFER_SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_MATERIAL_KEY'] = tmp_0['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['ISBN'] = tmp_1['ISBN'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['NEW_SHELF_PRICE'] = pd.to_numeric(tmp_2['NEW_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['USED_SHELF_PRICE'] = pd.to_numeric(tmp_3['USED_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['TIP_MATERIAL_KEY', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_1', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['tip_material_status_key'] = tmp_0['tip_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TIP_MATERIAL_STATUS'] = tmp_1['TIP_MATERIAL_STATUS'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'tip_material_status_key': 'TIP_MATERIAL_STATUS_KEY'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['TIP_MATERIAL_STATUS_KEY', 'TIP_MATERIAL_STATUS']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='left', on='TIP_SUBJECT_OFFERED_KEY').merge(prepared_table_3, how='left', on='TIP_MATERIAL_KEY').merge(prepared_table_4, how='left', on='TIP_MATERIAL_STATUS_KEY')
# Build grouping keys: TIP subject is represented by SUBJECT_TITLE here; keep COURSE_NUMBER and material status
# Compute totals and min/max for new and used shelf prices, plus counts of schools and materials
# For school count: count distinct OFFER_SCHOOL_NAME within each group
integrated['NEW_SHELF_PRICE'] = integrated['NEW_SHELF_PRICE']
integrated['USED_SHELF_PRICE'] = integrated['USED_SHELF_PRICE']
# Aggregate
agg = integrated.groupby(['COURSE_NUMBER', 'SUBJECT_TITLE', 'TIP_MATERIAL_STATUS'], dropna=False).agg(
    total_new_shelf_price = ('NEW_SHELF_PRICE', 'sum'),
    min_new_shelf_price = ('NEW_SHELF_PRICE', 'min'),
    max_new_shelf_price = ('NEW_SHELF_PRICE', 'max'),
    total_used_shelf_price = ('USED_SHELF_PRICE', 'sum'),
    min_used_shelf_price = ('USED_SHELF_PRICE', 'min'),
    max_used_shelf_price = ('USED_SHELF_PRICE', 'max'),
    total_materials = ('TIP_MATERIAL_KEY', 'count')
).reset_index()
# distinct school count per group
school_counts = integrated.groupby(['COURSE_NUMBER', 'SUBJECT_TITLE', 'TIP_MATERIAL_STATUS'], dropna=False)['OFFER_SCHOOL_NAME'].nunique(dropna=True).reset_index(name='total_schools')
result = agg.merge(school_counts, how='left', on=['COURSE_NUMBER', 'SUBJECT_TITLE', 'TIP_MATERIAL_STATUS'])
# Final projection and ordering
cols = ['COURSE_NUMBER', 'SUBJECT_TITLE', 'TIP_MATERIAL_STATUS', 'total_new_shelf_price', 'min_new_shelf_price', 'max_new_shelf_price', 'total_used_shelf_price', 'min_used_shelf_price', 'max_used_shelf_price', 'total_schools', 'total_materials']
missing = [c for c in cols if c not in result.columns]
for c in missing:
    if c not in result.columns:
        result[c] = None
target = result[cols]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
