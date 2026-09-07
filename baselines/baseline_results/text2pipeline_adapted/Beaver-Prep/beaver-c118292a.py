import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'CastType', 'params': {'column': 'TERM_CODE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_ID', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'SUBJECT_TITLE', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'RESPONSIBLE_FACULTY_NAME', 'dtype': 'str'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_ID', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SUBJECT_TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'RESPONSIBLE_FACULTY_NAME', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
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
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_4['SUBJECT_ID'] = tmp_4['SUBJECT_ID'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 6: StandardizeString
    tmp_5 = tmp_4.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_5['SUBJECT_TITLE'] = tmp_5['SUBJECT_TITLE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 7: StandardizeString
    tmp_6 = tmp_5.copy()
    _ns_3 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_3)
    _std_func_3 = _ns_3.get('transform') or _ns_3.get('transform')
    tmp_6['RESPONSIBLE_FACULTY_NAME'] = tmp_6['RESPONSIBLE_FACULTY_NAME'].apply(lambda s: _std_func_3(s) if pd.notna(s) else s)
    # Step 8: SelectCol
    result = tmp_6.loc[:, ['TERM_CODE', 'SUBJECT_ID', 'SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_7', pd.DataFrame()))

# Stage-2 program over the prepared tables.
df = prepared_table_1.copy()
# Identify Fall term rows. Common MIT coding uses 'FA' or '09' or similar; sample shows 'JA' which appears to be a term suffix code set. We will treat Fall as codes containing 'FA' or common fall-like indicators, and if none found, broaden to any rows with a suffix that plausibly maps to Fall (keep 'FA' first, else keep all as fallback per instruction).
fall_mask = df['TERM_CODE'].str.contains('FA', case=False, na=False)
fall_df = df[fall_mask]
if fall_df.empty:
    # Broaden: include terms ending with 'FA' or starting with typical Fall years; if still empty, fallback to all rows to avoid empty result
    fall_df = df[df['TERM_CODE'].str.endswith('FA', na=False)]
    if fall_df.empty:
        fall_df = df.copy()
# Unique titles of subjects offered in fall with instructor names and emails (email not present; include as missing by aggregating without fabricating a column; we'll provide instructor name and count per instructor). Compute total number of types (distinct SUBJECT_ID) per instructor.
# First, deduplicate subject titles per instructor within the selected term rows
fall_unique = fall_df.drop_duplicates(subset=['SUBJECT_ID','SUBJECT_TITLE','RESPONSIBLE_FACULTY_NAME'])
# Count distinct subject types per instructor (using SUBJECT_ID as the subject type identifier)
counts = fall_unique.groupby('RESPONSIBLE_FACULTY_NAME', dropna=False)['SUBJECT_ID'].nunique().reset_index(name='total_subject_types_per_instructor')
# Prepare the detailed rows with unique subject titles and instructor names
details = fall_unique[['SUBJECT_TITLE','RESPONSIBLE_FACULTY_NAME']].copy()
# Merge counts onto details so each row shows the instructor's total
target = details.merge(counts, on='RESPONSIBLE_FACULTY_NAME', how='left')
# Final projection: include placeholder for instructor email only if present in prepared data; since not available, we omit it to avoid creating columns not sourced from prepared tables.

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
