import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'LIBRARY_RESERVE_CATALOG_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_FROM', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'DATE_TO', 'date_format': '%Y-%m-%d'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'COURSE_NAME', 'DEPARTMENT']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'CATALOG_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['library_reserve_catalog_key', 'CATALOG_YEAR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['LIBRARY_RESERVE_CATALOG_KEY'] = pd.to_numeric(tmp_0['LIBRARY_RESERVE_CATALOG_KEY'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_1['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'TERM_CODE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'] = tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['DATE_FROM'] = pd.to_datetime(tmp_1['DATE_FROM'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 3: StandardizeDatetime
    tmp_2 = tmp_1.copy()
    tmp_2['DATE_TO'] = pd.to_datetime(tmp_2['DATE_TO'], errors='coerce').dt.strftime('%Y-%m-%d')
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME', 'COURSE_NAME', 'DEPARTMENT']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['CATALOG_YEAR'] = pd.to_numeric(tmp_0['CATALOG_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['library_reserve_catalog_key', 'CATALOG_YEAR']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_5', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['term_code'] = tmp_1['term_code'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_2['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_SUBJECT_OFFERED_KEY', 'term_code', 'SUBJECT_ID', 'SUBJECT_TITLE', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_3', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')
integrated = integrated.merge(prepared_table_3, left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key', how='left')
integrated = integrated.merge(prepared_table_4, left_on=['LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE'], right_on=['LIBRARY_SUBJECT_OFFERED_KEY','term_code'], how='left')
# Compute totals per instructor
# Treat CATALOG_YEAR <= 0 as missing for min/max computations
integrated['CATALOG_YEAR_CLEAN'] = integrated['CATALOG_YEAR']
try:
    integrated.loc[integrated['CATALOG_YEAR_CLEAN'] <= 0, 'CATALOG_YEAR_CLEAN'] = None
except Exception:
    pass
agg = integrated.groupby(['INSTRUCTOR_NAME'], dropna=False).agg(
    TOTAL_RESERVE_MATERIALS=('LIBRARY_RESERVE_CATALOG_KEY','nunique'),
    MIN_PUBLICATION_YEAR=('CATALOG_YEAR_CLEAN','min'),
    MAX_PUBLICATION_YEAR=('CATALOG_YEAR_CLEAN','max'),
    TOTAL_ENROLLED_STUDENTS=('NUM_ENROLLED_STUDENTS','sum'),
    COURSE_NAME_EX=('COURSE_NAME','first'),
    DEPARTMENT_EX=('DEPARTMENT','first')
).reset_index()
# Prefer to keep instructor name plus context columns
target = agg[['INSTRUCTOR_NAME','COURSE_NAME_EX','DEPARTMENT_EX','TOTAL_RESERVE_MATERIALS','MIN_PUBLICATION_YEAR','MAX_PUBLICATION_YEAR','TOTAL_ENROLLED_STUDENTS']].rename(columns={'COURSE_NAME_EX':'COURSE_NAME','DEPARTMENT_EX':'DEPARTMENT'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
