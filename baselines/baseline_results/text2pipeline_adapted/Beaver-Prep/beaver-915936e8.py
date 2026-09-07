import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE']}, 'table_indices': [0]}], [{'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'FIRST_DAY_OF_CLASSES', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'Rename', 'params': {'rename_map': [{'old_name': 'FIRST_DAY_OF_CLASSES', 'new_name': 'FIRST_DAY_OF_CLASSES_DT'}]}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES_DT']}, 'table_indices': [0]}]]

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
    tmp_1['SUBJECT_TITLE'] = tmp_1['SUBJECT_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['ACADEMIC_YEAR', 'TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_6', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: CastType
    tmp_0 = df.copy()
    tmp_0['ACADEMIC_YEAR'] = pd.to_numeric(tmp_0['ACADEMIC_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['FIRST_DAY_OF_CLASSES'] = pd.to_datetime(tmp_1['FIRST_DAY_OF_CLASSES'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 3: Rename
    tmp_2 = tmp_1.rename(columns={'FIRST_DAY_OF_CLASSES': 'FIRST_DAY_OF_CLASSES_DT'})
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['term_code', 'ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES_DT']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_5', pd.DataFrame()))

# Stage-2 program over the prepared tables.
integrated = prepared_table_1.merge(prepared_table_2, left_on='TERM_CODE', right_on='term_code', how='inner')
# Ensure academic year column exists after merge (prefer the year from the term/calendar table if both exist)
if 'ACADEMIC_YEAR_y' in integrated.columns:
    integrated['ACADEMIC_YEAR_MERGED'] = integrated['ACADEMIC_YEAR_y']
elif 'ACADEMIC_YEAR' in integrated.columns:
    integrated['ACADEMIC_YEAR_MERGED'] = integrated['ACADEMIC_YEAR']
elif 'ACADEMIC_YEAR_x' in integrated.columns:
    integrated['ACADEMIC_YEAR_MERGED'] = integrated['ACADEMIC_YEAR_x']
else:
    # Fallback: try to derive from TERM_CODE prefix (first 4 chars)
    integrated['ACADEMIC_YEAR_MERGED'] = integrated['TERM_CODE'].astype(str).str[:4]

# Sort within academic year by start date ascending; if date missing, keep but order last
if 'FIRST_DAY_OF_CLASSES_DT' not in integrated.columns:
    integrated['FIRST_DAY_OF_CLASSES_DT'] = None

integrated = integrated.sort_values(['ACADEMIC_YEAR_MERGED', 'FIRST_DAY_OF_CLASSES_DT', 'SUBJECT_ID'], ascending=[True, True, True])

# Compute cumulative count per academic year using the sorted order
integrated['CUMULATIVE_COURSES_BY_YEAR'] = integrated.groupby('ACADEMIC_YEAR_MERGED').cumcount() + 1

# Building name not present in available prepared tables; include a placeholder column with None
integrated['BUILDING_NAME'] = None

# Select and rename columns
target = integrated[[
    'SUBJECT_TITLE',
    'BUILDING_NAME',
    'CUMULATIVE_COURSES_BY_YEAR',
    'FIRST_DAY_OF_CLASSES_DT',
    'ACADEMIC_YEAR_MERGED'
]].rename(columns={
    'SUBJECT_TITLE': 'course_name',
    'BUILDING_NAME': 'building_name',
    'ACADEMIC_YEAR_MERGED': 'ACADEMIC_YEAR'
}).sort_values(['ACADEMIC_YEAR', 'FIRST_DAY_OF_CLASSES_DT']).reset_index(drop=True)

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
