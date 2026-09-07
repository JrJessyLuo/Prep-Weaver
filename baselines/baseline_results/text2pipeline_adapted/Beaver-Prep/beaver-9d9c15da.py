import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['SUBJECT_SUMMARY_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_ID_SORT', 'SUBJECT_OR_CLUSTER', 'MASTER_SUBJECT_ID', 'ULT_MASTER_SUBJECT_ID', 'CLUSTER_TYPE', 'CLUSTER_TYPE_DESC', 'CLUSTER_LIST', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'SUBJECT_GROUP_ID', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CLUSTER_TYPE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CLUSTER_TYPE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ENROLLMENT_NUMBER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CLUSTER_ENROLLMENT_NUMBER', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'HGN_CODE_DESC', 'target_columns': ['COURSE_LEVEL', '__discard'], 'func': "def transform(s):\n    text = str(s) if s is not None else ''\n    low = text.lower()\n    if 'graduate' in low:\n        level = 'Graduate'\n    elif 'undergrad' in low or 'not for graduate credit' in low:\n        level = 'Undergraduate'\n    else:\n        level = text\n    return [level, None]"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['__discard']}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'OFFER_DEPT_NAME', 'new_name': 'DEPARTMENT_NAME'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SUBJECT_OFFERED_SUMMARY_KEY', 'COMPOSITE_SUBJECT_KEY', 'TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'MASTER_SUBJECT_ID', 'CLUSTER_TYPE', 'CLUSTER_TYPE_DESC', 'CLUSTER_LIST', 'HGN_CODE', 'HGN_CODE_DESC', 'DEPARTMENT_NAME', 'SUBJECT_ENROLLMENT_NUMBER', 'CLUSTER_ENROLLMENT_NUMBER', 'NUM_ENROLLED_STUDENTS', 'SUBJECT_GROUPING_KEY', 'SUBJECT_SUMMARY_KEY', 'COURSE_LEVEL']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'IS_NO_COURSE_MATERIAL', 'MASTER_COURSE_NUMBER', 'MASTER_COURSE_NUMBER_DESC', 'MASTER_SUBJECT_ID', 'COURSE_NUMBER', 'COURSE_NUMBER_DESC', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID', 'NUM_ENROLLED_STUDENTS', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ISBN', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'subject_id', 'new_name': 'SUBJECT_ID'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RECORD_COUNT', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'AUTHOR', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'PUBLISHER', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'MATERIAL_INFO_SOURCE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NEW_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'USED_SHELF_PRICE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER', 'YEAR', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'RENTAL_NEW_PRICE', 'RENTAL_USED_PRICE', 'MATERIAL_INFO_SOURCE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['SUBJECT_SUMMARY_KEY', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_ID_SORT', 'SUBJECT_OR_CLUSTER', 'MASTER_SUBJECT_ID', 'ULT_MASTER_SUBJECT_ID', 'CLUSTER_TYPE', 'CLUSTER_TYPE_DESC', 'CLUSTER_LIST', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'SUBJECT_GROUP_ID', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_7', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SUBJECT_ID'] = tmp_0['SUBJECT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['COURSE_NUMBER'] = tmp_1['COURSE_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['SUBJECT_TITLE'] = tmp_2['SUBJECT_TITLE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['OFFER_DEPT_NAME'] = tmp_3['OFFER_DEPT_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['CLUSTER_TYPE'] = tmp_4['CLUSTER_TYPE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['CLUSTER_TYPE_DESC'] = tmp_5['CLUSTER_TYPE_DESC'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['TERM_CODE'] = tmp_6['TERM_CODE'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(tmp_7['SUBJECT_ENROLLMENT_NUMBER'], errors='coerce').fillna(0).astype(int)
    # Step 9: CastType
    tmp_8 = tmp_7.copy()
    tmp_8['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_8['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 10: CastType
    tmp_9 = tmp_8.copy()
    tmp_9['CLUSTER_ENROLLMENT_NUMBER'] = pd.to_numeric(tmp_9['CLUSTER_ENROLLMENT_NUMBER'], errors='coerce').astype(float)
    # Step 11: SplitColumn
    tmp_10 = tmp_9.copy()
    _ns_8 = {}
    exec("def transform(s):\n    text = str(s) if s is not None else ''\n    low = text.lower()\n    if 'graduate' in low:\n        level = 'Graduate'\n    elif 'undergrad' in low or 'not for graduate credit' in low:\n        level = 'Undergraduate'\n    else:\n        level = text\n    return [level, None]", globals(), _ns_8)
    _split_func_8 = _ns_8.get('transform') or _ns_8.get('transform') or _ns_8.get('split')
    _split_values_8 = tmp_10['HGN_CODE_DESC'].apply(_split_func_8)
    _split_values_8 = _split_values_8.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_10['COURSE_LEVEL'] = _split_values_8.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_10['__discard'] = _split_values_8.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 12: DropColumn
    tmp_11 = tmp_10.drop(columns=['__discard'], errors='ignore').copy()
    # Step 13: Rename
    tmp_12 = tmp_11.rename(columns={'OFFER_DEPT_NAME': 'DEPARTMENT_NAME'})
    # Step 14: SelectCol
    result = tmp_12.loc[:, ['SUBJECT_OFFERED_SUMMARY_KEY', 'COMPOSITE_SUBJECT_KEY', 'TERM_CODE', 'COURSE_NUMBER', 'SUBJECT_ID', 'SUBJECT_TITLE', 'MASTER_SUBJECT_ID', 'CLUSTER_TYPE', 'CLUSTER_TYPE_DESC', 'CLUSTER_LIST', 'HGN_CODE', 'HGN_CODE_DESC', 'DEPARTMENT_NAME', 'SUBJECT_ENROLLMENT_NUMBER', 'CLUSTER_ENROLLMENT_NUMBER', 'NUM_ENROLLED_STUDENTS', 'SUBJECT_GROUPING_KEY', 'SUBJECT_SUMMARY_KEY', 'COURSE_LEVEL']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SUBJECT_ID'] = tmp_0['SUBJECT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['COURSE_NUMBER'] = tmp_1['COURSE_NUMBER'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['SUBJECT_TITLE'] = tmp_3['SUBJECT_TITLE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['OFFER_DEPT_NAME'] = tmp_4['OFFER_DEPT_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_5['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'IS_NO_COURSE_MATERIAL', 'MASTER_COURSE_NUMBER', 'MASTER_COURSE_NUMBER_DESC', 'MASTER_SUBJECT_ID', 'COURSE_NUMBER', 'COURSE_NUMBER_DESC', 'SUBJECT_ID', 'SUBJECT_TITLE', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'RESPONSIBLE_FACULTY_NAME', 'RESPONSIBLE_FACULTY_MIT_ID', 'NUM_ENROLLED_STUDENTS', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_2', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['subject_id'] = tmp_2['subject_id'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['TIP_MATERIAL_KEY'] = tmp_3['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['TIP_MATERIAL_STATUS_KEY'] = tmp_4['TIP_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['ISBN'] = tmp_5['ISBN'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: Rename
    tmp_6 = tmp_5.rename(columns={'subject_id': 'SUBJECT_ID'})
    # Step 8: CastType
    tmp_7 = tmp_6.copy()
    tmp_7['RECORD_COUNT'] = pd.to_numeric(tmp_7['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID', 'ISBN', 'RECORD_COUNT', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_1', pd.DataFrame()))

def _prepare_table_5(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TITLE'] = tmp_0['TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['AUTHOR'] = tmp_1['AUTHOR'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['PUBLISHER'] = tmp_2['PUBLISHER'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['MATERIAL_INFO_SOURCE'] = tmp_3['MATERIAL_INFO_SOURCE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['NEW_SHELF_PRICE'] = pd.to_numeric(tmp_4['NEW_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['USED_SHELF_PRICE'] = pd.to_numeric(tmp_5['USED_SHELF_PRICE'], errors='coerce').astype(float)
    # Step 7: SelectCol
    result = tmp_5.loc[:, ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR', 'EDITION', 'PUBLISHER', 'YEAR', 'NEW_SHELF_PRICE', 'USED_SHELF_PRICE', 'RENTAL_NEW_PRICE', 'RENTAL_USED_PRICE', 'MATERIAL_INFO_SOURCE']].copy()
    return result

prepared_table_5 = _prepare_table_5(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
prepared = prepared_table_2.merge(prepared_table_3[['SUBJECT_ID','TERM_CODE','TIP_SUBJECT_OFFERED_KEY']], on=['SUBJECT_ID','TERM_CODE'], how='left')
prep_with_tip = prepared.merge(prepared_table_4, on=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID'], how='left')
prep_full = prep_with_tip.merge(prepared_table_5, on=['TIP_MATERIAL_KEY','ISBN'], how='left')
biol_mask_title = prep_full['SUBJECT_TITLE'].fillna('').str.contains('bio', case=False)
biol_mask_dept = prep_full['DEPARTMENT_NAME'].fillna('').str.contains('bio', case=False)
biol = prep_full[biol_mask_title | biol_mask_dept]
biol['is_tip'] = biol['TIP_MATERIAL_STATUS_KEY'].fillna('').str.upper().eq('TIP')
biol['is_library'] = biol['MATERIAL_INFO_SOURCE'].fillna('').str.upper().eq('ISBN')
# Aggregate material-level info per course offering
mat_agg = biol.groupby(['SUBJECT_ID','TERM_CODE','CLUSTER_TYPE','COURSE_LEVEL','DEPARTMENT_NAME','SUBJECT_TITLE'], dropna=False).agg(
    total_enroll=('SUBJECT_ENROLLMENT_NUMBER','sum'),
    uniq_materials=('TIP_MATERIAL_KEY', lambda s: s.dropna().nunique()),
    avg_new_price_tip=('NEW_SHELF_PRICE', lambda s: s[biol.loc[s.index, 'is_tip']].astype(float).mean() if s[biol.loc[s.index, 'is_tip']].notna().any() else float('nan')),
    avg_used_price_tip=('USED_SHELF_PRICE', lambda s: s[biol.loc[s.index, 'is_tip']].astype(float).mean() if s[biol.loc[s.index, 'is_tip']].notna().any() else float('nan')),
    tip_record_count_total=('RECORD_COUNT', lambda s: int(s[biol.loc[s.index, 'is_tip']].fillna(0).sum()) if s.notna().any() else 0),
    uniq_library_titles=('TITLE', lambda s: s[biol.loc[s.index, 'is_library']].dropna().nunique()),
    uniq_library_isbns=('ISBN', lambda s: s[biol.loc[s.index, 'is_library']].dropna().nunique())
).reset_index()
# Compute average enrollment within each cluster (over courses in same cluster type)
cluster_avg = mat_agg.groupby('CLUSTER_TYPE', dropna=False)['total_enroll'].mean().reset_index().rename(columns={'total_enroll':'avg_enrollment_within_cluster'})
result = mat_agg.merge(cluster_avg, on='CLUSTER_TYPE', how='left')
result = result.rename(columns={
    'DEPARTMENT_NAME':'department_name',
    'SUBJECT_TITLE':'course_title',
    'CLUSTER_TYPE':'cluster_type',
    'COURSE_LEVEL':'course_level',
    'total_enroll':'total_enrollments',
    'avg_enrollment_within_cluster':'average_enrollment_within_cluster',
    'uniq_materials':'number_of_unique_course_materials',
    'avg_new_price_tip':'average_new_price_for_TIP_materials',
    'avg_used_price_tip':'average_used_price_for_TIP_materials',
    'tip_record_count_total':'total_material_record_count_for_TIP_materials',
    'uniq_library_titles':'number_of_unique_library_titles',
    'uniq_library_isbns':'number_of_unique_library_ISBNs'
})
# Final projection per the question
cols = ['department_name','course_title','cluster_type','total_enrollments','average_enrollment_within_cluster','course_level','number_of_unique_course_materials','average_new_price_for_TIP_materials','average_used_price_for_TIP_materials','total_material_record_count_for_TIP_materials','number_of_unique_library_titles','number_of_unique_library_ISBNs']
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
