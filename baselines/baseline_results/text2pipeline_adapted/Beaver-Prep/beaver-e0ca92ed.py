import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'subject_id', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'subject_id', 'new_name': 'SUBJECT_ID'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ACADEMIC_YEAR', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_CODE', 'SUBJECT_NUMBER', 'DEPARTMENT_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': "def transform(s):\n    # Trim whitespace but preserve original casing and dot-format (e.g., 'HAA.1656')\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()\n"}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': "def transform(s):\n    # Strip leading/trailing spaces and collapse internal whitespace without changing case\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return None\n    t = str(s).strip()\n    return ' '.join(t.split())\n"}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['SUBJECT_ID', 'TERM_CODE', 'RESPONSIBLE_FACULTY_NAME', 'FORM_TYPE', 'FORM_TYPE_DESC']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ACADEMIC_YEAR'] = pd.to_numeric(tmp_0['ACADEMIC_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['subject_id'] = tmp_1['subject_id'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'subject_id': 'SUBJECT_ID'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['ACADEMIC_YEAR', 'SUBJECT_ID', 'SUBJECT_TITLE', 'SUBJECT_CODE', 'SUBJECT_NUMBER', 'DEPARTMENT_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_2', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec("def transform(s):\n    # Trim whitespace but preserve original casing and dot-format (e.g., 'HAA.1656')\n    return None if s is None or (isinstance(s, float) and str(s) == 'nan') else str(s).strip()\n", globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['SUBJECT_ID'] = tmp_0['SUBJECT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec("def transform(s):\n    # Strip leading/trailing spaces and collapse internal whitespace without changing case\n    if s is None or (isinstance(s, float) and str(s) == 'nan'):\n        return None\n    t = str(s).strip()\n    return ' '.join(t.split())\n", globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['RESPONSIBLE_FACULTY_NAME'] = tmp_1['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].astype(str)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['SUBJECT_ID', 'TERM_CODE', 'RESPONSIBLE_FACULTY_NAME', 'FORM_TYPE', 'FORM_TYPE_DESC']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_6', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_2.merge(prepared_table_1, how='inner', on='SUBJECT_ID')
# Filter to academic year 2022, preserving instructor names and course type info
integrated_2022 = integrated[integrated['ACADEMIC_YEAR'] == 2022]
# If responsible faculty names are missing, keep them as is; counting types per instructor requires grouping
# Define a robust course type using FORM_TYPE_DESC when available, else fall back to FORM_TYPE
course_type = integrated_2022['FORM_TYPE_DESC'].where(integrated_2022['FORM_TYPE_DESC'].notna() & (integrated_2022['FORM_TYPE_DESC'].astype(str).str.strip() != ''), integrated_2022['FORM_TYPE'])
integrated_2022 = integrated_2022.assign(course_type=course_type)
# Aggregate: total number of distinct types of courses per instructor within AY 2022
# Keep instructor name as provided; treat NaN as a separate category but drop pure missing names from count grouping to avoid an unnamed bucket dominating
tmp = integrated_2022.copy()
# Normalize instructor name nulls to NaN consistently
tmp['RESPONSIBLE_FACULTY_NAME'] = tmp['RESPONSIBLE_FACULTY_NAME'].where(tmp['RESPONSIBLE_FACULTY_NAME'].notna() & (tmp['RESPONSIBLE_FACULTY_NAME'].astype(str).str.strip() != ''), None)
# Compute counts per instructor; keep rows even if name is None but they won't contribute to named instructors' counts
grouped = tmp.groupby(['ACADEMIC_YEAR', 'RESPONSIBLE_FACULTY_NAME'], dropna=False)['course_type'].nunique().reset_index(name='total_types_of_courses')
# Project requested columns and, if there are unnamed instructors only, still return them; otherwise, prefer named instructors
target = grouped[['ACADEMIC_YEAR', 'RESPONSIBLE_FACULTY_NAME', 'total_types_of_courses']].sort_values(['RESPONSIBLE_FACULTY_NAME', 'total_types_of_courses'], ascending=[True, False])

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
