import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_CODE', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    # retain human-readable casing: trim only\n    return s.strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_SCHOOL_NAME', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    # retain casing for display; trim only\n    return s.strip()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CLUSTER_TYPE', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()\n'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CLUSTER_TYPE_DESC', 'func': 'def transform(s):\n    s = "" if s is None else str(s)\n    # keep readable text; trim only\n    return s.strip()\n'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ENROLLMENT_NUMBER', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['CLUSTER_TYPE', 'CLUSTER_TYPE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'SUBJECT_ID', 'SUBJECT_ENROLLMENT_NUMBER', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_CODE', 'func': 'def transform(s):\n    return str(s).strip().upper()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'DEPARTMENT_NAME', 'func': 'def transform(s):\n    # trim but preserve human-readable casing\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SCHOOL_NAME', 'func': 'def transform(s):\n    # trim but preserve human-readable casing\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'IS_DEGREE_GRANTING', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'IS_DEGREE_GRANTING']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()\n', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['OFFER_DEPT_CODE'] = tmp_0['OFFER_DEPT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    # retain human-readable casing: trim only\n    return s.strip()\n', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['OFFER_DEPT_NAME'] = tmp_1['OFFER_DEPT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    # retain casing for display; trim only\n    return s.strip()\n', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['OFFER_SCHOOL_NAME'] = tmp_2['OFFER_SCHOOL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    return s.strip().upper()\n', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['CLUSTER_TYPE'] = tmp_3['CLUSTER_TYPE'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_5 = {}
    exec('def transform(s):\n    s = "" if s is None else str(s)\n    # keep readable text; trim only\n    return s.strip()\n', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_4['CLUSTER_TYPE_DESC'] = tmp_4['CLUSTER_TYPE_DESC'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['SUBJECT_ENROLLMENT_NUMBER'] = pd.to_numeric(tmp_5['SUBJECT_ENROLLMENT_NUMBER'], errors='coerce').fillna(0).astype(int)
    # Step 7: CastType
    tmp_6 = tmp_5.copy()
    tmp_6['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_6['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['CLUSTER_TYPE', 'CLUSTER_TYPE_DESC', 'OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'OFFER_SCHOOL_NAME', 'SUBJECT_ID', 'SUBJECT_ENROLLMENT_NUMBER', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().upper()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['DEPARTMENT_CODE'] = tmp_0['DEPARTMENT_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    # trim but preserve human-readable casing\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['DEPARTMENT_NAME'] = tmp_1['DEPARTMENT_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    # trim but preserve human-readable casing\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['SCHOOL_NAME'] = tmp_2['SCHOOL_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['IS_DEGREE_GRANTING'] = tmp_3['IS_DEGREE_GRANTING'].astype(str)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_NAME', 'IS_DEGREE_GRANTING']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, how='inner', left_on='OFFER_DEPT_CODE', right_on='DEPARTMENT_CODE')
# Exclude clusters or schools with no student data: require positive or non-null enrollment at the subject level
# Use NUM_ENROLLED_STUDENTS primarily; fall back to SUBJECT_ENROLLMENT_NUMBER
integrated['enroll_basis'] = integrated['NUM_ENROLLED_STUDENTS']
mask_null = integrated['enroll_basis'].isna()
integrated.loc[mask_null, 'enroll_basis'] = integrated.loc[mask_null, 'SUBJECT_ENROLLMENT_NUMBER']
# Keep rows where we have student data (>0)
with_students = integrated[integrated['enroll_basis'].fillna(0) > 0]
# Build grouping keys and aggregates
grp_cols = ['CLUSTER_TYPE', 'OFFER_DEPT_NAME', 'SCHOOL_NAME']
agg_df = with_students.groupby(grp_cols).agg(
    IS_DEGREE_GRANTING=('IS_DEGREE_GRANTING', 'first'),
    total_subjects=('SUBJECT_ID', 'nunique'),
    total_enrollment=('enroll_basis', 'sum'),
    average_enrollment=('enroll_basis', 'mean')
).reset_index()
# Final projection and ordering for readability
agg_df = agg_df.rename(columns={'OFFER_DEPT_NAME': 'department_name', 'SCHOOL_NAME': 'school_name'})
agg_df['average_enrollment'] = agg_df['average_enrollment']
columns = ['CLUSTER_TYPE', 'department_name', 'school_name', 'IS_DEGREE_GRANTING', 'total_subjects', 'total_enrollment', 'average_enrollment']
target = agg_df[columns]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
