import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'LIBRARY_RESERVE_CATALOG_KEY', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'SUBJECT_ID']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'NUM_ENROLLED_STUDENTS', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_SUBJECT_OFFERED_KEY', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS']}, 'table_indices': [0]}]]

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
    tmp_2['SUBJECT_ID'] = tmp_2['SUBJECT_ID'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY', 'SUBJECT_ID']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_6', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(tmp_1['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['LIBRARY_SUBJECT_OFFERED_KEY', 'OFFER_DEPT_NAME', 'NUM_ENROLLED_STUDENTS']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_1', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, on='LIBRARY_SUBJECT_OFFERED_KEY', how='inner')
# Compute per-department aggregations
# Courses using library materials: count distinct course offerings (LIBRARY_SUBJECT_OFFERED_KEY)
# Catalog items associated: count distinct LIBRARY_RESERVE_CATALOG_KEY
# Average enrollment per course: mean of NUM_ENROLLED_STUDENTS over distinct courses using materials in that dept
# To compute average enrollment per course, first collapse to unique course offerings with their enrollment and department
courses = integrated[['LIBRARY_SUBJECT_OFFERED_KEY','OFFER_DEPT_NAME','NUM_ENROLLED_STUDENTS']].drop_duplicates()
# Department-level counts
dept_course_counts = courses.groupby('OFFER_DEPT_NAME', as_index=False).size().rename(columns={'size':'total_courses_using_library_materials'})
# Catalog item counts per dept from integrated (each row is a catalog-course link) using distinct catalog keys
dept_catalog_counts = integrated.groupby('OFFER_DEPT_NAME', as_index=False)['LIBRARY_RESERVE_CATALOG_KEY'].nunique().rename(columns={'LIBRARY_RESERVE_CATALOG_KEY':'catalog_items_associated'})
# Average enrollment per course per dept
dept_avg_enroll = courses.groupby('OFFER_DEPT_NAME', as_index=False)['NUM_ENROLLED_STUDENTS'].mean().rename(columns={'NUM_ENROLLED_STUDENTS':'average_enrollment_per_course'})
# Merge department-level metrics
dept_metrics = dept_course_counts.merge(dept_catalog_counts, on='OFFER_DEPT_NAME', how='outer').merge(dept_avg_enroll, on='OFFER_DEPT_NAME', how='outer')
# Grand total across all departments
grand_courses = courses['LIBRARY_SUBJECT_OFFERED_KEY'].nunique()
grand_catalog = integrated['LIBRARY_RESERVE_CATALOG_KEY'].nunique()
grand_avg_enroll = courses['NUM_ENROLLED_STUDENTS'].mean()
grand = dept_metrics.head(0).copy()
grand['OFFER_DEPT_NAME'] = ['Grand Total']
grand['total_courses_using_library_materials'] = [grand_courses]
grand['catalog_items_associated'] = [grand_catalog]
grand['average_enrollment_per_course'] = [grand_avg_enroll]
# Combine
result = pd.concat([dept_metrics, grand], ignore_index=True, sort=False)
# Final projection and friendly column names
result = result.rename(columns={'OFFER_DEPT_NAME':'department_name'})[
    ['department_name','total_courses_using_library_materials','catalog_items_associated','average_enrollment_per_course']
]
# Optionally sort with Grand Total last
is_grand = (result['department_name'].str.lower()=='grand total')
result = pd.concat([result[~is_grand].sort_values('department_name', kind='mergesort'), result[is_grand]], ignore_index=True)
target = result

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
