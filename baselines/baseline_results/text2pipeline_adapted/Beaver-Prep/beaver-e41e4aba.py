import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'DEPARTMENT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SCHOOL_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SCHOOL_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DLC_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    return re.sub(r"\\s+", " ", s)'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    return re.sub(r"\\s+", " ", s)'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DLC_KEY', 'func': 'def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    return re.sub(r"\\s+", " ", s)'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': []}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'DLC_KEY']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'COURSE_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_CODE_DESC', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SCHOOL_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SCHOOL_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['COURSE_NUMBER', 'SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'COURSE_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'HGN_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'HGN_CODE_DESC', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'OFFER_DEPT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HGN_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'HGN_CODE_DESC', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SUBJECT_ID', 'target_columns': ['SUBJECT_PREFIX', 'SUBJECT_NUM_RAW'], 'func': "def transform(s):\n    s = str(s)\n    if '.' in s:\n        parts = s.split('.', 1)\n        return [parts[0], parts[1]]\n    else:\n        return [s, '']"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_NUM_RAW', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SplitColumn', 'params': {'source_column': 'SUBJECT_NUM_RAW', 'target_columns': ['SUBJECT_NUM'], 'func': "def transform(s):\n    import math\n    try:\n        return [float(s)]\n    except Exception:\n        return [float('nan')]"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['COURSE_NUMBER', 'SUBJECT_ID', 'HGN_CODE', 'HGN_CODE_DESC', 'OFFER_DEPT_CODE', 'SUBJECT_PREFIX', 'SUBJECT_NUM']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['DEPARTMENT_CODE'] = tmp_0['DEPARTMENT_CODE'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['DEPARTMENT_NAME'] = tmp_1['DEPARTMENT_NAME'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['SCHOOL_CODE'] = tmp_2['SCHOOL_CODE'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['SCHOOL_NAME'] = tmp_3['SCHOOL_NAME'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['DLC_KEY'] = tmp_4['DLC_KEY'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['DEPARTMENT_CODE'] = tmp_5['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    return re.sub(r"\\s+", " ", s)', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_6['DEPARTMENT_NAME'] = tmp_6['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    s = re.sub(r"\\s+", " ", s)\n    return s.upper()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_7['SCHOOL_CODE'] = tmp_7['SCHOOL_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    return re.sub(r"\\s+", " ", s)', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_8['SCHOOL_NAME'] = tmp_8['SCHOOL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import re\n    s = \'\' if s is None else str(s)\n    s = s.strip()\n    return re.sub(r"\\s+", " ", s)', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_9['DLC_KEY'] = tmp_9['DLC_KEY'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 11: Rename
    tmp_10 = tmp_9.rename(columns={})
    # Step 12: SelectCol
    result = tmp_10.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME', 'DLC_KEY']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['COURSE_NUMBER'] = tmp_0['COURSE_NUMBER'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SUBJECT_CODE'] = tmp_1['SUBJECT_CODE'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['SUBJECT_CODE_DESC'] = tmp_2['SUBJECT_CODE_DESC'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['DEPARTMENT_CODE'] = tmp_3['DEPARTMENT_CODE'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['DEPARTMENT_NAME'] = tmp_4['DEPARTMENT_NAME'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['SCHOOL_CODE'] = tmp_5['SCHOOL_CODE'].astype(str)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['SCHOOL_NAME'] = tmp_6['SCHOOL_NAME'].astype(str)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_7['COURSE_NUMBER'] = tmp_7['COURSE_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_8['SUBJECT_CODE'] = tmp_8['SUBJECT_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_9['SUBJECT_CODE_DESC'] = tmp_9['SUBJECT_CODE_DESC'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_10['DEPARTMENT_CODE'] = tmp_10['DEPARTMENT_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_11['DEPARTMENT_NAME'] = tmp_11['DEPARTMENT_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_12['SCHOOL_CODE'] = tmp_12['SCHOOL_CODE'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 14: StandardizeString
    tmp_13 = tmp_12.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_13['SCHOOL_NAME'] = tmp_13['SCHOOL_NAME'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 15: SelectCol
    result = tmp_13.loc[:, ['COURSE_NUMBER', 'SUBJECT_CODE', 'SUBJECT_CODE_DESC', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['COURSE_NUMBER'] = tmp_0['COURSE_NUMBER'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['HGN_CODE'] = tmp_2['HGN_CODE'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['HGN_CODE_DESC'] = tmp_3['HGN_CODE_DESC'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['OFFER_DEPT_CODE'] = tmp_4['OFFER_DEPT_CODE'].astype(str)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_5['COURSE_NUMBER'] = tmp_5['COURSE_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_6['SUBJECT_ID'] = tmp_6['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_7['HGN_CODE'] = tmp_7['HGN_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_8['HGN_CODE_DESC'] = tmp_8['HGN_CODE_DESC'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_9['OFFER_DEPT_CODE'] = tmp_9['OFFER_DEPT_CODE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 11: SplitColumn
    tmp_10 = tmp_9.copy()
    _ns_6 = {}
    exec("def transform(s):\n    s = str(s)\n    if '.' in s:\n        parts = s.split('.', 1)\n        return [parts[0], parts[1]]\n    else:\n        return [s, '']", globals(), _ns_6)
    _split_func_6 = _ns_6.get('transform') or _ns_6.get('transform') or _ns_6.get('split')
    _split_values_6 = tmp_10['SUBJECT_ID'].apply(_split_func_6)
    _split_values_6 = _split_values_6.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_10['SUBJECT_PREFIX'] = _split_values_6.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    tmp_10['SUBJECT_NUM_RAW'] = _split_values_6.apply(lambda x: x[1] if len(x) > 1 else pd.NA)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_11['SUBJECT_NUM_RAW'] = tmp_11['SUBJECT_NUM_RAW'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 13: SplitColumn
    tmp_12 = tmp_11.copy()
    _ns_8 = {}
    exec("def transform(s):\n    import math\n    try:\n        return [float(s)]\n    except Exception:\n        return [float('nan')]", globals(), _ns_8)
    _split_func_8 = _ns_8.get('transform') or _ns_8.get('transform') or _ns_8.get('split')
    _split_values_8 = tmp_12['SUBJECT_NUM_RAW'].apply(_split_func_8)
    _split_values_8 = _split_values_8.apply(lambda x: x if isinstance(x, (list, tuple, pd.Series)) else [x])
    tmp_12['SUBJECT_NUM'] = _split_values_8.apply(lambda x: x[0] if len(x) > 0 else pd.NA)
    # Step 14: SelectCol
    result = tmp_12.loc[:, ['COURSE_NUMBER', 'SUBJECT_ID', 'HGN_CODE', 'HGN_CODE_DESC', 'OFFER_DEPT_CODE', 'SUBJECT_PREFIX', 'SUBJECT_NUM']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_3.merge(prepared_table_2, how='left', left_on=['COURSE_NUMBER'], right_on=['COURSE_NUMBER'])
# Prefer department alignment via OFFER_DEPT_CODE when available; fall back to table_2 DEPARTMENT_CODE
integrated['JOIN_DEPT_CODE'] = integrated['OFFER_DEPT_CODE'].where(integrated['OFFER_DEPT_CODE'].notna() & (integrated['OFFER_DEPT_CODE']!=''), integrated['DEPARTMENT_CODE'])
# Attach DLC and authoritative school naming from table_1 via department code
integrated = integrated.merge(prepared_table_1, how='left', left_on='JOIN_DEPT_CODE', right_on='DEPARTMENT_CODE', suffixes=('', '_auth'))
# Choose school fields, prefer table_1 school if present, else table_2 school
integrated['SCHOOL_CODE_FINAL'] = integrated['SCHOOL_CODE'].where(integrated['SCHOOL_CODE'].notna() & (integrated['SCHOOL_CODE']!=''), integrated['SCHOOL_CODE_auth'])
integrated['SCHOOL_NAME_FINAL'] = integrated['SCHOOL_NAME'].where(integrated['SCHOOL_NAME'].notna() & (integrated['SCHOOL_NAME']!=''), integrated['SCHOOL_NAME_auth'])
# Graduate level: use HGN_CODE_DESC directly
# Aggregate per school: total SIS subjects (distinct SUBJECT_ID), min/max course numbers (based on SUBJECT_NUM within each COURSE_NUMBER group), and total number of departments offering subjects (distinct JOIN_DEPT_CODE)
# Compute min/max per COURSE_NUMBER within school using SUBJECT_NUM; when all NaN, min/max stay NaN and we'll fallback to lexicographic on SUBJECT_ID suffix
tmp = integrated.copy()
# For fallback lexicographic number from SUBJECT_ID when SUBJECT_NUM is NaN, try to parse numeric part
fallback_num = tmp['SUBJECT_ID'].str.split('.', n=1).str[1]
# Remove non-numeric trailing parts (keep leading numeric portion)
fallback_num = fallback_num.str.extract(r'^(\d+(?:\.\d+)?)', expand=False)
# Prefer SUBJECT_NUM where available
tmp['NUM_FOR_MINMAX'] = tmp['SUBJECT_NUM']
tmp['NUM_FOR_MINMAX'] = tmp['NUM_FOR_MINMAX'].where(tmp['NUM_FOR_MINMAX'].notna(), fallback_num.astype(float, errors='ignore'))
# Group and aggregate
grp_keys = ['SCHOOL_CODE_FINAL', 'SCHOOL_NAME_FINAL']
agg_df = tmp.groupby(grp_keys).agg(
    total_sis_subjects=('SUBJECT_ID', 'nunique'),
    min_course_number=('NUM_FOR_MINMAX', 'min'),
    max_course_number=('NUM_FOR_MINMAX', 'max'),
    total_departments_offering=('JOIN_DEPT_CODE', 'nunique')
).reset_index()
# Bring DLC key: if multiple DLCs per school, list distinct DLC_KEYs concatenated; graduate level: list distinct HGN_CODE_DESCs observed per school
dlc_per_school = tmp.groupby(grp_keys)['DLC_KEY'].apply(lambda s: ', '.join(sorted(set([x for x in s.dropna().astype(str) if x])))).reset_index(name='DLC_KEY')
grad_level_per_school = tmp.groupby(grp_keys)['HGN_CODE_DESC'].apply(lambda s: ', '.join(sorted(set([x for x in s.dropna().astype(str) if x])))).reset_index(name='graduate_level')
res = agg_df.merge(dlc_per_school, on=grp_keys, how='left').merge(grad_level_per_school, on=grp_keys, how='left')
# Final projection and ordering
target = res.rename(columns={
    'SCHOOL_CODE_FINAL': 'school_code',
    'SCHOOL_NAME_FINAL': 'school_name',
    'DLC_KEY': 'dlc_key',
    'graduate_level': 'graduate_level',
    'total_sis_subjects': 'total_sis_subjects',
    'min_course_number': 'min_course_number',
    'max_course_number': 'max_course_number',
    'total_departments_offering': 'total_departments_offering'
})[['school_code', 'school_name', 'dlc_key', 'graduate_level', 'total_sis_subjects', 'min_course_number', 'max_course_number', 'total_departments_offering']].sort_values(['school_code', 'school_name'])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
