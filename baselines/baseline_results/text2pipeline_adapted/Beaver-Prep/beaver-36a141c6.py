import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    # preserve case, trim ends, collapse internal whitespace\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'AUTHOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'EDITION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'PUBLISHER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MATERIAL_INFO_SOURCE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NEW_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'USED_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RENTAL_NEW_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RENTAL_USED_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER', 'YEAR', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'RENTAL_NEW_PRICE', 'RENTAL_USED_PRICE', 'MATERIAL_INFO_SOURCE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'tip_material_status_key', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'COURSE_NUMBER', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    # preserve case, trim ends, collapse internal whitespace\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TIP_MATERIAL_KEY'] = tmp_1['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['TIP_MATERIAL_STATUS_KEY'] = tmp_2['TIP_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['TERM_CODE'] = tmp_3['TERM_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['subject_id'] = tmp_4['subject_id'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return None\n    s = str(s)\n    s = re.sub(r"\\s+", " ", s.strip())\n    return s if s != \'\' else None', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['ISBN'] = tmp_5['ISBN'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['RECORD_COUNT'] = pd.to_numeric(tmp_6['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_7['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
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
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['TITLE'] = tmp_2['TITLE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['AUTHOR'] = tmp_3['AUTHOR'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['EDITION'] = tmp_4['EDITION'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['PUBLISHER'] = tmp_5['PUBLISHER'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['MATERIAL_INFO_SOURCE'] = tmp_6['MATERIAL_INFO_SOURCE'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['NEW_SHELF_PRICE'] = pd.to_numeric(tmp_7['NEW_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['USED_SHELF_PRICE'] = pd.to_numeric(tmp_8['USED_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['RENTAL_NEW_PRICE'] = pd.to_numeric(tmp_9['RENTAL_NEW_PRICE'], errors='coerce').astype(float)
    # Step 11: CastType
    tmp_10 = tmp_9.copy()
    tmp_10['RENTAL_USED_PRICE'] = pd.to_numeric(tmp_10['RENTAL_USED_PRICE'], errors='coerce').astype(float)
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER', 'YEAR', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'RENTAL_NEW_PRICE', 'RENTAL_USED_PRICE', 'MATERIAL_INFO_SOURCE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['tip_material_status_key'] = tmp_0['tip_material_status_key'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TIP_MATERIAL_STATUS_CODE'] = tmp_1['TIP_MATERIAL_STATUS_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['TIP_MATERIAL_STATUS'] = tmp_2['TIP_MATERIAL_STATUS'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['WAREHOUSE_LOAD_DATE'] = tmp_3['WAREHOUSE_LOAD_DATE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['tip_material_status_key', 'TIP_MATERIAL_STATUS_CODE', 'TIP_MATERIAL_STATUS', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SUBJECT_CODE'] = tmp_0['SUBJECT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SUBJECT_CODE_DESC'] = tmp_1['SUBJECT_CODE_DESC'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['DEPARTMENT_CODE'] = tmp_2['DEPARTMENT_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['DEPARTMENT_NAME'] = tmp_3['DEPARTMENT_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['SCHOOL_CODE'] = tmp_4['SCHOOL_CODE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['SCHOOL_NAME'] = tmp_5['SCHOOL_NAME'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['COURSE_NUMBER'] = tmp_6['COURSE_NUMBER'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'COURSE_NUMBER', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_4, how='left', left_on='subject_id', right_on='SUBJECT_CODE').merge(prepared_table_2, how='left', on='TIP_MATERIAL_KEY').merge(prepared_table_3, how='left', left_on='TIP_MATERIAL_STATUS_KEY', right_on='tip_material_status_key')
# Identify rows that represent courses with materials using multiple plausible evidence columns
mk = integrated['TIP_MATERIAL_KEY'].astype(str).fillna('')
title = integrated.get('TITLE', pd.Series(index=integrated.index, dtype=object)).astype(str).fillna('')
author = integrated.get('AUTHOR', pd.Series(index=integrated.index, dtype=object)).astype(str).fillna('')
# Exclude explicit 'no materials' markers; accept others including priced/unpriced
no_mat_prefix = mk.str.lower().str.startswith('n/acourse has no materials')
no_mat_title = title.str.lower().str.contains('course has no materials', case=False, na=False)
no_mat_author = author.str.lower().str.contains('course has no materials', case=False, na=False)
mask_has_material = (~no_mat_prefix) & (~no_mat_title) & (~no_mat_author) & mk.str.len().gt(0)
filtered = integrated[mask_has_material].copy()
# Build surrogate course offering id
surrogate = filtered['TIP_SUBJECT_OFFERED_KEY'].astype(str)
needs_fallback = surrogate.str.lower().isin(['nan', ''])
filtered['COURSE_OFFERING_ID'] = surrogate.where(~needs_fallback, filtered['subject_id'].astype(str).str.strip() + '|' + filtered['TERM_CODE'].astype(str).str.strip())
# Group by department and school names
group_cols = ['DEPARTMENT_NAME','SCHOOL_NAME']
agg_df = filtered.groupby(group_cols, dropna=False).agg(
    unique_materials=('TIP_MATERIAL_KEY','nunique'),
    num_courses=('COURSE_OFFERING_ID','nunique'),
    avg_new_price=('NEW_SHELF_PRICE','mean'),
    avg_used_price=('USED_SHELF_PRICE','mean'),
    total_material_records=('TIP_MATERIAL_KEY','size'),
    distinct_material_statuses=('TIP_MATERIAL_STATUS','nunique')
).reset_index()
# Grand total across all schools and departments with nulls in those fields
grand_vals = {
    'DEPARTMENT_NAME': [None],
    'SCHOOL_NAME': [None],
    'unique_materials': [filtered['TIP_MATERIAL_KEY'].nunique()],
    'num_courses': [filtered['COURSE_OFFERING_ID'].nunique()],
    'avg_new_price': [filtered['NEW_SHELF_PRICE'].mean()],
    'avg_used_price': [filtered['USED_SHELF_PRICE'].mean()],
    'total_material_records': [filtered['TIP_MATERIAL_KEY'].size],
    'distinct_material_statuses': [filtered['TIP_MATERIAL_STATUS'].nunique()]
}
grand_df = pd.DataFrame(grand_vals)
# Concatenate and assign to target
cols = ['DEPARTMENT_NAME','SCHOOL_NAME','unique_materials','num_courses','avg_new_price','avg_used_price','total_material_records','distinct_material_statuses']
result = agg_df[cols]
target = pd.concat([result, grand_df[cols]], ignore_index=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
