import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_MATERIAL_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TITLE', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'AUTHOR', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'TIP_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'OFFER_DEPT_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'TERM_CODE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'library_reserve_catalog_key', 'new_name': 'LIBRARY_RESERVE_CATALOG_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CATALOG_TITLE', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'CATALOG_AUTHOR_NAME', 'func': 'def transform(s):\n    return str(s).strip() if s is not None else s'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'CATALOG_ISBN', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_RESERVE_CATALOG_KEY', 'CATALOG_TITLE', 'CATALOG_AUTHOR_NAME', 'CATALOG_ISBN']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'INSTRUCTOR_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_MATERIAL_STATUS_KEY', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_MATERIAL_STATUS', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['TERM_CODE'] = tmp_0['TERM_CODE'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['TIP_MATERIAL_KEY'] = tmp_1['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['TERM_CODE'] = tmp_2['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TIP_MATERIAL_KEY', 'TIP_MATERIAL_STATUS_KEY', 'TERM_CODE', 'subject_id', 'ISBN']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_MATERIAL_KEY'] = tmp_0['TIP_MATERIAL_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TITLE'] = tmp_1['TITLE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['AUTHOR'] = tmp_2['AUTHOR'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['TIP_MATERIAL_KEY', 'ISBN', 'TITLE', 'AUTHOR']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['TIP_SUBJECT_OFFERED_KEY'] = tmp_0['TIP_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['TERM_CODE'] = tmp_1['TERM_CODE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_2['SUBJECT_ID'] = tmp_2['SUBJECT_ID'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_4 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_4)
    _std_func_4 = _ns_4.get('transform') or _ns_4.get('transform')
    tmp_3['OFFER_DEPT_NAME'] = tmp_3['OFFER_DEPT_NAME'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE', 'SUBJECT_ID', 'OFFER_DEPT_NAME']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_6', pd.DataFrame()))

def _prepare_table_4(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'] = tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_1['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
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
    tmp_3['SUBJECT_ID'] = tmp_3['SUBJECT_ID'].apply(lambda s: _std_func_4(s) if pd.notna(s) else s)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_MATERIAL_STATUS_KEY', 'TERM_CODE', 'SUBJECT_ID']].copy()
    return result

prepared_table_4 = _prepare_table_4(tables.get('table_2', pd.DataFrame()))

def _prepare_table_5(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'library_reserve_catalog_key': 'LIBRARY_RESERVE_CATALOG_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['CATALOG_TITLE'] = tmp_1['CATALOG_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip() if s is not None else s', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['CATALOG_AUTHOR_NAME'] = tmp_2['CATALOG_AUTHOR_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: CastType
    tmp_3 = tmp_2.copy()
    tmp_3['CATALOG_ISBN'] = tmp_3['CATALOG_ISBN'].astype(str)
    # Step 5: SelectCol
    result = tmp_3.loc[:, ['LIBRARY_RESERVE_CATALOG_KEY', 'CATALOG_TITLE', 'CATALOG_AUTHOR_NAME', 'CATALOG_ISBN']].copy()
    return result

prepared_table_5 = _prepare_table_5(tables.get('table_3', pd.DataFrame()))

def _prepare_table_6(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'] = tmp_0['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['INSTRUCTOR_NAME'] = tmp_1['INSTRUCTOR_NAME'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'INSTRUCTOR_NAME']].copy()
    return result

prepared_table_6 = _prepare_table_6(tables.get('table_7', pd.DataFrame()))

def _prepare_table_7(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_MATERIAL_STATUS_KEY'] = tmp_0['LIBRARY_MATERIAL_STATUS_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_1['LIBRARY_MATERIAL_STATUS'] = tmp_1['LIBRARY_MATERIAL_STATUS'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_MATERIAL_STATUS_KEY', 'LIBRARY_MATERIAL_STATUS']].copy()
    return result

prepared_table_7 = _prepare_table_7(tables.get('table_9', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_3, how='left', left_on=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE'], right_on=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE'])
# Bring in TIP material bibliographic info
integrated = integrated.merge(prepared_table_2, how='left', on=['TIP_MATERIAL_KEY','ISBN'])
# Map to library reserves by subject/term to know availability
lib_link = prepared_table_4.merge(prepared_table_5, how='left', on='LIBRARY_RESERVE_CATALOG_KEY')
# Join library link to subjects/terms (TIP side) via SUBJECT_ID and TERM_CODE alignment
integrated = integrated.merge(lib_link, how='left', left_on=['SUBJECT_ID','TERM_CODE'], right_on=['SUBJECT_ID','TERM_CODE'])
# Attach instructor info to count instructors per library book
integrated = integrated.merge(prepared_table_6, how='left', on='LIBRARY_COURSE_INSTRUCTOR_KEY')
# Derive availability flag: available if library reserve catalog entry exists (LIBRARY_RESERVE_CATALOG_KEY not null)
integrated['Availability'] = integrated['LIBRARY_RESERVE_CATALOG_KEY'].notna().map({True:'Available in Library', False:'Not Available in Library'})
# Compute total instructors per library book per department (count distinct instructors per library catalog key within department)
# First, create a helper for instructor counts
instr_counts = (integrated.groupby(['OFFER_DEPT_NAME','LIBRARY_RESERVE_CATALOG_KEY'])['INSTRUCTOR_NAME']
                .nunique()
                .reset_index(name='Total_Instructors_per_Library_Book'))
# Merge back
integrated = integrated.merge(instr_counts, how='left', on=['OFFER_DEPT_NAME','LIBRARY_RESERVE_CATALOG_KEY'])
# Total number of materials available in the library for the department: count distinct LIBRARY_RESERVE_CATALOG_KEY where available
dept_available = (integrated[integrated['Availability']=='Available in Library']
                  .groupby('OFFER_DEPT_NAME')['LIBRARY_RESERVE_CATALOG_KEY']
                  .nunique()
                  .reset_index(name='Total_Materials_Available_in_Department'))
# Total number of available materials across all departments (single scalar)
total_available_all = int(integrated[integrated['Availability']=='Available in Library']['LIBRARY_RESERVE_CATALOG_KEY'].nunique())
integrated = integrated.merge(dept_available, how='left', on='OFFER_DEPT_NAME')
integrated['Total_Available_Materials_All_Departments'] = total_available_all
# Select final fields per department with TIP material details
target = integrated[['OFFER_DEPT_NAME', 'TITLE', 'AUTHOR', 'ISBN', 'TERM_CODE', 'Availability', 'Total_Instructors_per_Library_Book', 'Total_Materials_Available_in_Department', 'Total_Available_Materials_All_Departments']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
