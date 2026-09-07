import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'SUBJECT_ID', 'new_name': 'COURSE_ID'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['COURSE_ID', 'SUBJECT_TITLE', 'ACADEMIC_YEAR', 'TERM_CODE']}, 'table_indices': [0]}], [{'op': 'StandardizeDatetime', 'params': {'column_name': 'TERM_START_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'StandardizeDatetime', 'params': {'column_name': 'TERM_END_DATE', 'date_format': '%d-%b-%y'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'ACADEMIC_YEAR', 'dtype': 'int'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['term_code', 'ACADEMIC_YEAR', 'TERM_START_DATE', 'TERM_END_DATE']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'SUBJECT_ID': 'COURSE_ID'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    import re\n    return re.sub(r"\\s+", " ", str(s).strip())', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SUBJECT_TITLE'] = tmp_1['SUBJECT_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['COURSE_ID', 'SUBJECT_TITLE', 'ACADEMIC_YEAR', 'TERM_CODE']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_7', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: StandardizeDatetime
    tmp_0 = df.copy()
    tmp_0['TERM_START_DATE'] = pd.to_datetime(tmp_0['TERM_START_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 2: StandardizeDatetime
    tmp_1 = tmp_0.copy()
    tmp_1['TERM_END_DATE'] = pd.to_datetime(tmp_1['TERM_END_DATE'], errors='coerce').dt.strftime('%d-%b-%y')
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['ACADEMIC_YEAR'] = pd.to_numeric(tmp_2['ACADEMIC_YEAR'], errors='coerce').fillna(0).astype(int)
    # Step 4: SelectCol
    result = tmp_2.loc[:, ['term_code', 'ACADEMIC_YEAR', 'TERM_START_DATE', 'TERM_END_DATE']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_4', pd.DataFrame()))

# Stage-2 program over the prepared tables.
# Merge course info with term info to obtain dates and year context
integrated = prepared_table_1.merge(prepared_table_2, left_on='TERM_CODE', right_on='term_code', how='left')

# Parse term start/end dates from strings; coerce errors to NaT for robustness
integrated['TERM_START_DATE'] = pd.to_datetime(integrated['TERM_START_DATE'], errors='coerce', infer_datetime_format=True, dayfirst=False)
integrated['TERM_END_DATE'] = pd.to_datetime(integrated['TERM_END_DATE'], errors='coerce', infer_datetime_format=True, dayfirst=False)

# Duration in days (inclusive)
integrated['duration_days'] = (integrated['TERM_END_DATE'] - integrated['TERM_START_DATE']).dt.days + 1

# Use term start date as course start date for ordering
integrated['course_start_date'] = integrated['TERM_START_DATE']

# Ensure academic year used for partitioning is from the course table when available; fall back to term table if missing
integrated['AY_PART'] = integrated['ACADEMIC_YEAR_x'].where(integrated['ACADEMIC_YEAR_x'].notna(), integrated['ACADEMIC_YEAR_y'])

# Sort within partition and compute centered rolling mean with window size 5
integrated = integrated.sort_values(['AY_PART', 'course_start_date', 'COURSE_ID']).reset_index(drop=True)
integrated['running_avg_duration_days'] = (
    integrated.groupby('AY_PART', group_keys=False)['duration_days']
    .apply(lambda s: s.rolling(window=5, center=True, min_periods=1).mean())
)

# Building name not available in provided prepared tables; set to None for completeness
integrated['BUILDING_NAME'] = None

# Final projection
target = integrated[['SUBJECT_TITLE', 'BUILDING_NAME', 'duration_days', 'running_avg_duration_days', 'AY_PART', 'course_start_date']].rename(columns={'AY_PART': 'ACADEMIC_YEAR'})

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
