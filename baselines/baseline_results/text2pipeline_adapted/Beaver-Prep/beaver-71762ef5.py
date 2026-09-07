import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE_DESC', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'COURSE_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    if s is None:\n        return s\n    s = str(s)\n    return s.strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'COURSE_NUMBER', 'target_columns': ['COURSE_LEVEL', '_drop_tmp_cn_rest'], 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    m = re.match(r"^\\s*([A-Za-z]+)(.*)$", s)\n    if m:\n        return [m.group(1), m.group(2)]\n    return [None, s]'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['COURSE_LEVEL', 'SUBJECT_CODE'], 'target_column': 'COURSE_LEVEL', 'func': "def transform(row):\n    # If COURSE_LEVEL is missing/empty, fall back to SUBJECT_CODE uppercased\n    lvl = row.get('COURSE_LEVEL')\n    subj = row.get('SUBJECT_CODE')\n    lvl = None if (lvl is None or str(lvl).strip() == '') else str(lvl)\n    if lvl is None:\n        return None if subj is None else str(subj).upper()\n    return lvl"}, 'table_indices': [0]}, {'op': 'DropColumn', 'params': {'drop_columns': ['_drop_tmp_cn_rest']}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'COURSE_NUMBER', 'COURSE_LEVEL']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'department_full_name', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPT_BUDGET_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DEPARTMENT_LAST_ACTIVITY_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'department_full_name', 'IS_DEGREE_GRANTING', 'DLC_KEY']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SIS_ADMIN_DEPARTMENT_CODE', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None or (isinstance(s,float) and s!=s) else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SIS_ADMIN_DEPARTMENT_NAME', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None or (isinstance(s,float) and s!=s) else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_PHONE_AREA_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'department_phone_number', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'Concatenate', 'params': {'concatenate_columns': ['DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number'], 'target_column': 'PHONE', 'func': 'def transform(row):\n    ac = row.get(\'DEPARTMENT_PHONE_AREA_CODE\')\n    num = row.get(\'department_phone_number\')\n    def clean(x):\n        if x is None:\n            return \'\'\n        s = str(x)\n        if s.lower()==\'nan\':\n            return \'\'\n        return s.strip()\n    ac = clean(ac)\n    num = clean(num)\n    if not ac and not num:\n        return \'\'\n    if ac and num:\n        return f"{ac}-{num}"\n    return num or ac'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'LAST_ACTIVITY_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SIS_ADMIN_DEPARTMENT_CODE', 'new_name': 'DEPARTMENT_CODE'}, {'old_name': 'SIS_ADMIN_DEPARTMENT_NAME', 'new_name': 'DEPARTMENT_NAME'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'PHONE', 'DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SUBJECT_CODE'] = tmp_0['SUBJECT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SUBJECT_CODE_DESC'] = tmp_1['SUBJECT_CODE_DESC'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['DEPARTMENT_CODE'] = tmp_2['DEPARTMENT_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['DEPARTMENT_NAME'] = tmp_3['DEPARTMENT_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['SCHOOL_CODE'] = tmp_4['SCHOOL_CODE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    import re\n    if s is None:\n        return s\n    s = str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['SCHOOL_NAME'] = tmp_5['SCHOOL_NAME'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['COURSE_NUMBER'] = tmp_6['COURSE_NUMBER'].astype(str)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_7 = {}
    exec('def transform(s):\n    if s is None:\n        return s\n    s = str(s)\n    return s.strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_7['COURSE_NUMBER'] = tmp_7['COURSE_NUMBER'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 9: SplitColumn
    tmp_8 = tmp_7.copy()
    _ns_8 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    m = re.match(r"^\\s*([A-Za-z]+)(.*)$", s)\n    if m:\n        return [m.group(1), m.group(2)]\n    return [None, s]', globals(), _ns_8)
    _split_func_8 = _ns_8.get('transform') or _ns_8.get('transform') or _ns_8.get('split')
    _split_values_8 = tmp_8['COURSE_NUMBER'].apply(_split_func_8)
    _split_values_8 = _split_values_8.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_8['COURSE_LEVEL'] = _split_values_8.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_8['_drop_tmp_cn_rest'] = _split_values_8.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 10: Concatenate
    tmp_9 = tmp_8.copy()
    _ns_9 = {}
    exec("def transform(row):\n    # If COURSE_LEVEL is missing/empty, fall back to SUBJECT_CODE uppercased\n    lvl = row.get('COURSE_LEVEL')\n    subj = row.get('SUBJECT_CODE')\n    lvl = None if (lvl is None or str(lvl).strip() == '') else str(lvl)\n    if lvl is None:\n        return None if subj is None else str(subj).upper()\n    return lvl", globals(), _ns_9)
    _concat_func_9 = _ns_9.get('transform') or _ns_9.get('transform') or _ns_9.get('concat')
    tmp_9['COURSE_LEVEL'] = tmp_9[['COURSE_LEVEL', 'SUBJECT_CODE']].apply(_concat_func_9, axis=1)
    # Step 11: DropColumn
    tmp_10 = tmp_9.drop(columns=['_drop_tmp_cn_rest'], errors='ignore').copy()
    # Step 12: StandardizeDatetime
    tmp_11 = tmp_10.copy()
    tmp_11['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_11['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 13: SelectCol
    result = tmp_11.loc[:, ['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'COURSE_NUMBER', 'COURSE_LEVEL']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['DEPARTMENT_CODE'] = tmp_0['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['DEPARTMENT_NAME'] = tmp_1['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['department_full_name'] = tmp_2['department_full_name'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['SCHOOL_CODE'] = tmp_3['SCHOOL_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import re\n    s = "" if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['SCHOOL_NAME'] = tmp_4['SCHOOL_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['DEPT_BUDGET_CODE'] = tmp_5['DEPT_BUDGET_CODE'].astype(str)
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['DEPARTMENT_LAST_ACTIVITY_DATE'] = pd.to_datetime(tmp_6['DEPARTMENT_LAST_ACTIVITY_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 8: StandardizeDatetime
    tmp_7 = tmp_6.copy()
    tmp_7['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_7['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'department_full_name', 'IS_DEGREE_GRANTING', 'DLC_KEY']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None or (isinstance(s,float) and s!=s) else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SIS_ADMIN_DEPARTMENT_CODE'] = tmp_0['SIS_ADMIN_DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None or (isinstance(s,float) and s!=s) else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SIS_ADMIN_DEPARTMENT_NAME'] = tmp_1['SIS_ADMIN_DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['DEPARTMENT_PHONE_AREA_CODE'] = tmp_2['DEPARTMENT_PHONE_AREA_CODE'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['department_phone_number'] = tmp_3['department_phone_number'].astype(str)
    # Step 5: Concatenate
    tmp_4 = tmp_3.copy()
    _ns_3 = {}
    exec('def transform(row):\n    ac = row.get(\'DEPARTMENT_PHONE_AREA_CODE\')\n    num = row.get(\'department_phone_number\')\n    def clean(x):\n        if x is None:\n            return \'\'\n        s = str(x)\n        if s.lower()==\'nan\':\n            return \'\'\n        return s.strip()\n    ac = clean(ac)\n    num = clean(num)\n    if not ac and not num:\n        return \'\'\n    if ac and num:\n        return f"{ac}-{num}"\n    return num or ac', globals(), _ns_3)
    _concat_func_3 = _ns_3.get('transform') or _ns_3.get('transform') or _ns_3.get('concat')
    tmp_4['PHONE'] = tmp_4[['DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number']].apply(_concat_func_3, axis=1)
    # Step 6: StandardizeDatetime
    tmp_5 = tmp_4.copy()
    tmp_5['LAST_ACTIVITY_DATE'] = pd.to_datetime(tmp_5['LAST_ACTIVITY_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 7: StandardizeDatetime
    tmp_6 = tmp_5.copy()
    tmp_6['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(tmp_6['WAREHOUSE_LOAD_DATE'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 8: Rename
    tmp_7 = tmp_6.rename(columns={'SIS_ADMIN_DEPARTMENT_CODE': 'DEPARTMENT_CODE', 'SIS_ADMIN_DEPARTMENT_NAME': 'DEPARTMENT_NAME'})
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'PHONE', 'DEPARTMENT_PHONE_AREA_CODE', 'department_phone_number']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge course offerings (prepared_table_1) with department-school reference (prepared_table_2)
integrated = prepared_table_1.merge(
    prepared_table_2,
    how='left',
    on=['DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_CODE','SCHOOL_NAME'],
    suffixes=('_t1','_t2')
)
# Merge in department phone info
integrated = integrated.merge(
    prepared_table_3[['DEPARTMENT_CODE','DEPARTMENT_NAME','PHONE','department_phone_number']],
    how='left',
    on=['DEPARTMENT_CODE','DEPARTMENT_NAME']
)
# Unify phone value
integrated['PHONE_UNIFIED'] = integrated['PHONE']
mask_missing = integrated['PHONE_UNIFIED'].isna() | (integrated['PHONE_UNIFIED'].astype(str).str.strip()== '')
integrated.loc[mask_missing, 'PHONE_UNIFIED'] = integrated['department_phone_number']
# Aggregate distinct phone counts per school/department
phone_counts = (
    integrated.assign(PHONE_UNIFIED=integrated['PHONE_UNIFIED'].astype(str))
    .groupby(['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME'], dropna=False)['PHONE_UNIFIED']
    .nunique(dropna=True)
    .reset_index(name='total_phone_numbers')
)
# Most common course level per department
level_counts = (
    integrated.groupby(['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME','COURSE_LEVEL'], dropna=False)
    .size()
    .reset_index(name='cnt')
)
level_counts['rank'] = level_counts.groupby(['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME'])['cnt'].rank(method='dense', ascending=False)
# pick top; break ties by alphabetical COURSE_LEVEL
top_levels = (
    level_counts[level_counts['rank']==1]
    .sort_values(['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME','COURSE_LEVEL'])
    .drop(columns=['rank'])
    .drop_duplicates(subset=['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME'], keep='first')
)
# Merge results
result = phone_counts.merge(
    top_levels[['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME','COURSE_LEVEL']],
    how='left',
    on=['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME']
)
# Final selection and ordering
target = (
    result[['SCHOOL_CODE','SCHOOL_NAME','DEPARTMENT_CODE','DEPARTMENT_NAME','total_phone_numbers','COURSE_LEVEL']]
    .sort_values(['SCHOOL_CODE','DEPARTMENT_CODE'])
    .reset_index(drop=True)
)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
