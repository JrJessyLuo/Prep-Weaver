import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'DEPARTMENT_NAME', 'SUBJECT_TITLE', 'HGN_DESC', 'TOTAL_UNITS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_SCHOOL_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'RESPONSIBLE_FACULTY_NAME', 'SECTION_ID']}, 'table_indices': [0]}], [{'op': 'SelectCol', 'params': {'columns': ['SIS_COURSE_DESCRIPTION_KEY', 'COURSE', 'COURSE_DESCRIPTION', 'COURSE_DESCRIPTION_LONG', 'DEPARTMENT', 'DEPARTMENT_NAME', 'DEPT_NAME_IN_COMMENCEMENT_BK', 'SCHOOL_NAME', 'SCHOOL_NAME_IN_COMMENCEMENT_BK', 'FROM_TERM', 'FROM_TERM_DESCRIPTION', 'THRU_TERM', 'THRU_TERM_DESCRIPTION', 'COURSE_OPTION', 'COURSE_LEVEL', 'CIP_PROGRAM_CODE', 'IS_DEGREE_GRANTING', 'DEFAULT_ULTIMATE_DEGREE', 'GRADAUTE_LEVEL', 'GRADUATE_LEVEL', 'LAST_ACTIVITY_DATE', 'WAREHOUSE_LOAD_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'DEPARTMENT_NAME', 'SUBJECT_TITLE', 'HGN_DESC', 'TOTAL_UNITS']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['OFFER_DEPT_NAME'] = tmp_2['OFFER_DEPT_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['OFFER_SCHOOL_NAME'] = tmp_3['OFFER_SCHOOL_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['RESPONSIBLE_FACULTY_NAME'] = tmp_4['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'RESPONSIBLE_FACULTY_NAME', 'SECTION_ID']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['SIS_COURSE_DESCRIPTION_KEY', 'COURSE', 'COURSE_DESCRIPTION', 'COURSE_DESCRIPTION_LONG', 'DEPARTMENT', 'DEPARTMENT_NAME', 'DEPT_NAME_IN_COMMENCEMENT_BK', 'SCHOOL_NAME', 'SCHOOL_NAME_IN_COMMENCEMENT_BK', 'FROM_TERM', 'FROM_TERM_DESCRIPTION', 'THRU_TERM', 'THRU_TERM_DESCRIPTION', 'COURSE_OPTION', 'COURSE_LEVEL', 'CIP_PROGRAM_CODE', 'IS_DEGREE_GRANTING', 'DEFAULT_ULTIMATE_DEGREE', 'GRADAUTE_LEVEL', 'GRADUATE_LEVEL', 'LAST_ACTIVITY_DATE', 'WAREHOUSE_LOAD_DATE']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_8', pd.DataFrame()))

# Stage-2 program over the prepared tables.
_frames = []
if isinstance(prepared_table_1, pd.DataFrame) and not prepared_table_1.empty:
    _tmp = prepared_table_1.copy()
    _tmp['__prepared_table__'] = 'prepared_table_1'
    _frames.append(_tmp)
if isinstance(prepared_table_2, pd.DataFrame) and not prepared_table_2.empty:
    _tmp = prepared_table_2.copy()
    _tmp['__prepared_table__'] = 'prepared_table_2'
    _frames.append(_tmp)
if isinstance(prepared_table_3, pd.DataFrame) and not prepared_table_3.empty:
    _tmp = prepared_table_3.copy()
    _tmp['__prepared_table__'] = 'prepared_table_3'
    _frames.append(_tmp)
target = pd.concat(_frames, ignore_index=True, sort=False) if _frames else pd.DataFrame()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
