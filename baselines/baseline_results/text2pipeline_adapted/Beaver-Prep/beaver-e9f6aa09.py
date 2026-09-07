import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'COURSE_NUMBER', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE_DESC', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_CODE', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SUBJECT_CODE', 'SCHOOL_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'COURSE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_DESCRIPTION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_DESCRIPTION_LONG', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPT_NAME_IN_COMMENCEMENT_BK', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME_IN_COMMENCEMENT_BK', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'FROM_TERM', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'THRU_TERM', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_OPTION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'COURSE_LEVEL', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'IS_DEGREE_GRANTING', 'func': 'def transform(s):\n    s = str(s).strip()\n    return s.upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEFAULT_ULTIMATE_DEGREE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'GRADAUTE_LEVEL', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'GRADUATE_LEVEL', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LAST_ACTIVITY_DATE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'WAREHOUSE_LOAD_DATE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'DEPARTMENT', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_DEGREE_GRANTING', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT', 'IS_DEGREE_GRANTING']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['COURSE_NUMBER'] = tmp_0['COURSE_NUMBER'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SUBJECT_CODE'] = tmp_1['SUBJECT_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['SUBJECT_CODE_DESC'] = tmp_2['SUBJECT_CODE_DESC'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['DEPARTMENT_CODE'] = tmp_3['DEPARTMENT_CODE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['DEPARTMENT_NAME'] = tmp_4['DEPARTMENT_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['SCHOOL_CODE'] = tmp_5['SCHOOL_CODE'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['SCHOOL_NAME'] = tmp_6['SCHOOL_NAME'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['SUBJECT_CODE', 'SCHOOL_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['COURSE'] = tmp_0['COURSE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['COURSE_DESCRIPTION'] = tmp_1['COURSE_DESCRIPTION'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['COURSE_DESCRIPTION_LONG'] = tmp_2['COURSE_DESCRIPTION_LONG'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['DEPARTMENT'] = tmp_3['DEPARTMENT'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['DEPARTMENT_NAME'] = tmp_4['DEPARTMENT_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_5['DEPT_NAME_IN_COMMENCEMENT_BK'] = tmp_5['DEPT_NAME_IN_COMMENCEMENT_BK'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_7 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_7)
    _std_func_7 = _ns_7.get('transform') or _ns_7.get('transform')
    tmp_6['SCHOOL_NAME'] = tmp_6['SCHOOL_NAME'].apply(lambda s: _std_func_7(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_8 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_8)
    _std_func_8 = _ns_8.get('transform') or _ns_8.get('transform')
    tmp_7['SCHOOL_NAME_IN_COMMENCEMENT_BK'] = tmp_7['SCHOOL_NAME_IN_COMMENCEMENT_BK'].apply(lambda s: _std_func_8(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_9 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_9)
    _std_func_9 = _ns_9.get('transform') or _ns_9.get('transform')
    tmp_8['FROM_TERM'] = tmp_8['FROM_TERM'].apply(lambda s: _std_func_9(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_10 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_10)
    _std_func_10 = _ns_10.get('transform') or _ns_10.get('transform')
    tmp_9['THRU_TERM'] = tmp_9['THRU_TERM'].apply(lambda s: _std_func_10(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_11 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_11)
    _std_func_11 = _ns_11.get('transform') or _ns_11.get('transform')
    tmp_10['COURSE_OPTION'] = tmp_10['COURSE_OPTION'].apply(lambda s: _std_func_11(s) if pd.notna(s) else s)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_12 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_12)
    _std_func_12 = _ns_12.get('transform') or _ns_12.get('transform')
    tmp_11['COURSE_LEVEL'] = tmp_11['COURSE_LEVEL'].apply(lambda s: _std_func_12(s) if pd.notna(s) else s)
    # Step 13: StandardizeString
    tmp_12 = tmp_11.copy()
    _ns_13 = {}
    exec('def transform(s):\n    s = str(s).strip()\n    return s.upper()', globals(), _ns_13)
    _std_func_13 = _ns_13.get('transform') or _ns_13.get('transform')
    tmp_12['IS_DEGREE_GRANTING'] = tmp_12['IS_DEGREE_GRANTING'].apply(lambda s: _std_func_13(s) if pd.notna(s) else s)
    # Step 14: StandardizeString
    tmp_13 = tmp_12.copy()
    _ns_14 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_14)
    _std_func_14 = _ns_14.get('transform') or _ns_14.get('transform')
    tmp_13['DEFAULT_ULTIMATE_DEGREE'] = tmp_13['DEFAULT_ULTIMATE_DEGREE'].apply(lambda s: _std_func_14(s) if pd.notna(s) else s)
    # Step 15: StandardizeString
    tmp_14 = tmp_13.copy()
    _ns_15 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_15)
    _std_func_15 = _ns_15.get('transform') or _ns_15.get('transform')
    tmp_14['GRADAUTE_LEVEL'] = tmp_14['GRADAUTE_LEVEL'].apply(lambda s: _std_func_15(s) if pd.notna(s) else s)
    # Step 16: StandardizeString
    tmp_15 = tmp_14.copy()
    _ns_16 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_16)
    _std_func_16 = _ns_16.get('transform') or _ns_16.get('transform')
    tmp_15['GRADUATE_LEVEL'] = tmp_15['GRADUATE_LEVEL'].apply(lambda s: _std_func_16(s) if pd.notna(s) else s)
    # Step 17: StandardizeString
    tmp_16 = tmp_15.copy()
    _ns_17 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_17)
    _std_func_17 = _ns_17.get('transform') or _ns_17.get('transform')
    tmp_16['LAST_ACTIVITY_DATE'] = tmp_16['LAST_ACTIVITY_DATE'].apply(lambda s: _std_func_17(s) if pd.notna(s) else s)
    # Step 18: StandardizeString
    tmp_17 = tmp_16.copy()
    _ns_18 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_18)
    _std_func_18 = _ns_18.get('transform') or _ns_18.get('transform')
    tmp_17['WAREHOUSE_LOAD_DATE'] = tmp_17['WAREHOUSE_LOAD_DATE'].apply(lambda s: _std_func_18(s) if pd.notna(s) else s)
    # Step 19: CastType
    tmp_18 = tmp_17.copy()
    tmp_18['DEPARTMENT'] = tmp_18['DEPARTMENT'].astype(str)
    # Step 20: CastType
    tmp_19 = tmp_18.copy()
    tmp_19['IS_DEGREE_GRANTING'] = tmp_19['IS_DEGREE_GRANTING'].astype(str)
    # Step 21: SelectCol
    result = tmp_19.loc[:, ['DEPARTMENT', 'IS_DEGREE_GRANTING']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, left_on='DEPARTMENT', right_on='SUBJECT_CODE', how='left')
# Aggregate counts per school
grp = integrated.groupby('SCHOOL_NAME', dropna=False)
result = grp.agg(
    total_courses=('DEPARTMENT', 'count'),
    total_degree_granting=('IS_DEGREE_GRANTING', lambda s: (s.str.upper()=='Y').sum())
).reset_index()
# Final projection and naming
target = result[['SCHOOL_NAME', 'total_courses', 'total_degree_granting']].rename(columns={'SCHOOL_NAME':'school_name'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
