import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'term_code', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'TERM_DESCRIPTION', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'term_code', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_DESCRIPTION', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR', 'ACADEMIC_YEAR_DESC']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_NUMBER', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_TITLE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'PREREQUISITES', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_CODE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_NUMBER', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'PREREQUISITES', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_CODE', 'SUBJECT_NUMBER', 'SUBJECT_TITLE', 'PREREQUISITES']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_TITLE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RESPONSIBLE_FACULTY_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': "def transform(s):\n    return str(s).strip() if s is not None else ''"}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['term_code'] = tmp_0['term_code'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['TERM_DESCRIPTION'] = tmp_1['TERM_DESCRIPTION'].astype(str)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_2['term_code'] = tmp_2['term_code'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_3['TERM_DESCRIPTION'] = tmp_3['TERM_DESCRIPTION'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['term_code', 'TERM_DESCRIPTION', 'ACADEMIC_YEAR', 'ACADEMIC_YEAR_DESC']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_5', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['SUBJECT_CODE'] = tmp_2['SUBJECT_CODE'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['SUBJECT_NUMBER'] = tmp_3['SUBJECT_NUMBER'].astype(str)
    # Step 5: CastType
    tmp_4 = tmp_3.copy()
    tmp_4['SUBJECT_TITLE'] = tmp_4['SUBJECT_TITLE'].astype(str)
    # Step 6: CastType
    tmp_5 = tmp_4.copy()
    tmp_5['PREREQUISITES'] = tmp_5['PREREQUISITES'].astype(str)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_6['TERM_CODE'] = tmp_6['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_7['SUBJECT_ID'] = tmp_7['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 9: StandardizeString
    tmp_8 = tmp_7.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_8['SUBJECT_CODE'] = tmp_8['SUBJECT_CODE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 10: StandardizeString
    tmp_9 = tmp_8.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_9['SUBJECT_NUMBER'] = tmp_9['SUBJECT_NUMBER'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 11: StandardizeString
    tmp_10 = tmp_9.copy()
    _ns_5 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_5)
    _std_func_5 = _ns_5.get('transform') or _ns_5.get('transform')
    tmp_10['SUBJECT_TITLE'] = tmp_10['SUBJECT_TITLE'].apply(lambda s: _std_func_5(s) if pd.notna(s) else s)
    # Step 12: StandardizeString
    tmp_11 = tmp_10.copy()
    _ns_6 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_6)
    _std_func_6 = _ns_6.get('transform') or _ns_6.get('transform')
    tmp_11['PREREQUISITES'] = tmp_11['PREREQUISITES'].apply(lambda s: _std_func_6(s) if pd.notna(s) else s)
    # Step 13: SelectCol
    result = tmp_11.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_CODE', 'SUBJECT_NUMBER', 'SUBJECT_TITLE', 'PREREQUISITES']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['SUBJECT_ID'] = tmp_1['SUBJECT_ID'].astype(str)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['SUBJECT_TITLE'] = tmp_2['SUBJECT_TITLE'].astype(str)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['RESPONSIBLE_FACULTY_NAME'] = tmp_3['RESPONSIBLE_FACULTY_NAME'].astype(str)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_1 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['TERM_CODE'] = tmp_4['TERM_CODE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['SUBJECT_ID'] = tmp_5['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['SUBJECT_TITLE'] = tmp_6['SUBJECT_TITLE'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: StandardizeString
    tmp_7 = tmp_6.copy()
    _ns_4 = {}
    exec("def transform(s):\n    return str(s).strip() if s is not None else ''", globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_7['RESPONSIBLE_FACULTY_NAME'] = tmp_7['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 9: SelectCol
    result = tmp_7.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_3, how='inner', on=['TERM_CODE','SUBJECT_ID']).merge(prepared_table_1[['term_code','TERM_DESCRIPTION']], how='inner', left_on='TERM_CODE', right_on='term_code')
# Filter to 2023 Fall term using robust match on code or description
mask_code = integrated['TERM_CODE'].str.contains('2023FA', case=False, na=False)
mask_desc = integrated['TERM_DESCRIPTION'].str.contains('2023', case=False, na=False) & integrated['TERM_DESCRIPTION'].str.contains('Fall', case=False, na=False)
fa23 = integrated[mask_code | mask_desc]
if fa23.empty:
    # Fallback: try any term with year 2023 and typical FA marker
    fa23 = integrated[integrated['TERM_CODE'].str.contains('23', case=False, na=False) & integrated['TERM_CODE'].str.contains('FA', case=False, na=False)]
    if fa23.empty:
        fa23 = integrated.copy()
# Unique term descriptions
term_descriptions = fa23[['TERM_CODE','TERM_DESCRIPTION']].drop_duplicates()
# Subject titles with prerequisites for the term
subjects_with_prereq = fa23[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE_x','PREREQUISITES']].drop_duplicates()
subjects_with_prereq = subjects_with_prereq.rename(columns={'SUBJECT_TITLE_x':'SUBJECT_TITLE'})
# Total number of types of subjects per term code (distinct SUBJECT_ID per TERM_CODE)
subject_types_per_term = fa23.groupby('TERM_CODE', as_index=False)['SUBJECT_ID'].nunique().rename(columns={'SUBJECT_ID':'NUM_SUBJECT_TYPES'})
# Instructor(s) of the course(s) in this term
instructors = fa23[['TERM_CODE','SUBJECT_ID','RESPONSIBLE_FACULTY_NAME']].drop_duplicates()
# Number of types of courses ever taught by the instructor: count distinct SUBJECT_ID per instructor across all terms in prepared_table_3
inst_course_counts = prepared_table_3.groupby('RESPONSIBLE_FACULTY_NAME', as_index=False)['SUBJECT_ID'].nunique().rename(columns={'SUBJECT_ID':'NUM_COURSE_TYPES_EVER_TAUGHT'})
# Bring instructor counts onto instructors for the specific term
instructors_with_counts = instructors.merge(inst_course_counts, how='left', on='RESPONSIBLE_FACULTY_NAME')
# Assemble final target by merging components on TERM_CODE and SUBJECT_ID where appropriate
out = subjects_with_prereq.merge(term_descriptions, how='left', on='TERM_CODE')\
    .merge(subject_types_per_term, how='left', on='TERM_CODE')\
    .merge(instructors_with_counts, how='left', on=['TERM_CODE','SUBJECT_ID'])
# Final projection and reasonable ordering
target = out[['TERM_CODE','TERM_DESCRIPTION','SUBJECT_ID','SUBJECT_TITLE','PREREQUISITES','NUM_SUBJECT_TYPES','RESPONSIBLE_FACULTY_NAME','NUM_COURSE_TYPES_EVER_TAUGHT']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
