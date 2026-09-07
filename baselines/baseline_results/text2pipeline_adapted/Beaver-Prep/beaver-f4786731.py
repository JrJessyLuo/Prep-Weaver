import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME', 'INSTRUCTOR_NAME']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'LIBRARY_RESERVE_CATALOG_KEY', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_COURSE_INSTRUCTOR_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY']}, 'table_indices': [0]}], [{'op': 'StandardizeString', 'params': {'column_name': 'LIBRARY_SUBJECT_OFFERED_KEY', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['LIBRARY_SUBJECT_OFFERED_KEY']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: SelectCol
    result = df.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'COURSE_NAME', 'INSTRUCTOR_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['LIBRARY_RESERVE_CATALOG_KEY'] = tmp_0['LIBRARY_RESERVE_CATALOG_KEY'].astype(str)
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['LIBRARY_COURSE_INSTRUCTOR_KEY'] = tmp_1['LIBRARY_COURSE_INSTRUCTOR_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: StandardizeString
    tmp_2 = tmp_1.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_2['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_2['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'LIBRARY_RESERVE_CATALOG_KEY']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

def _prepare_table_3(_source):
    df = _source.copy()
    # Step 1: StandardizeString
    tmp_0 = df.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'] = tmp_0['LIBRARY_SUBJECT_OFFERED_KEY'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 2: SelectCol
    result = tmp_0.loc[:, ['LIBRARY_SUBJECT_OFFERED_KEY']].copy()
    return result

prepared_table_3 = _prepare_table_3(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
t1 = prepared_table_1.copy()
t2 = prepared_table_2.copy()
t3 = prepared_table_3.copy()

# Integrate all prepared tables
integrated = t2.merge(t1, how='left', on='LIBRARY_COURSE_INSTRUCTOR_KEY')
integrated = integrated.merge(t3, how='left', on='LIBRARY_SUBJECT_OFFERED_KEY')

# Compute amount of material per course instructor key and subject offered key
mat_counts = (
    integrated.groupby([
        'LIBRARY_COURSE_INSTRUCTOR_KEY',
        'LIBRARY_SUBJECT_OFFERED_KEY',
        'INSTRUCTOR_NAME',
        'COURSE_NAME'
    ], dropna=False)['LIBRARY_RESERVE_CATALOG_KEY']
    .nunique()
    .reset_index(name='AMOUNT_OF_MATERIAL')
)

# Return unique instructor names, course titles, amount of material, by the instructor key and subject offered key
target = mat_counts[['LIBRARY_COURSE_INSTRUCTOR_KEY', 'LIBRARY_SUBJECT_OFFERED_KEY', 'INSTRUCTOR_NAME', 'COURSE_NAME', 'AMOUNT_OF_MATERIAL']].drop_duplicates()

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
