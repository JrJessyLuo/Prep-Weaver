import pandas as pd
import numpy as np

# Per-table Text-to-Pipeline chains, retained for auditability.
TEXT2PIPELINE_CHAINS = [[{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'IAP_SUBJECT_SESSION_KEY', 'new_name': 'IAP_SUBJECT_SESSION_KEY'}]}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'MAX_ENROLLMENT', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'CastType', 'params': {'column': 'FEE', 'dtype': 'float'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ACTIVITY_TITLE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'ENROLLMENT_TYPE', 'func': 'def transform(s):\n    return str(s).strip()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'TERM_CODE', 'ENROLLMENT_TYPE', 'MAX_ENROLLMENT', 'FEE', 'IS_MULTIPLE_SESSION', 'IS_CANCELLED']}, 'table_indices': [0]}], [{'op': 'Rename', 'params': {'rename_map': [{'old_name': 'iap_subject_session_key', 'new_name': 'IAP_SUBJECT_SESSION_KEY'}]}, 'table_indices': [0]}, {'op': 'StandardizeString', 'params': {'column_name': 'SESSION_LOCATION', 'func': 'def transform(s):\n    return str(s).strip().lower()'}, 'table_indices': [0]}, {'op': 'SelectCol', 'params': {'columns': ['IAP_SUBJECT_SESSION_KEY', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME', 'HAS_SESSION_INFO']}, 'table_indices': [0]}]]

def _prepare_table_1(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'IAP_SUBJECT_SESSION_KEY': 'IAP_SUBJECT_SESSION_KEY'})
    # Step 2: CastType
    tmp_1 = tmp_0.copy()
    tmp_1['MAX_ENROLLMENT'] = pd.to_numeric(tmp_1['MAX_ENROLLMENT'], errors='coerce').astype(float)
    # Step 3: CastType
    tmp_2 = tmp_1.copy()
    tmp_2['FEE'] = pd.to_numeric(tmp_2['FEE'], errors='coerce').astype(float)
    # Step 4: StandardizeString
    tmp_3 = tmp_2.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_3['ACTIVITY_TITLE'] = tmp_3['ACTIVITY_TITLE'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 5: StandardizeString
    tmp_4 = tmp_3.copy()
    _ns_2 = {}
    exec('def transform(s):\n    return str(s).strip()', globals(), _ns_2)
    _std_func_2 = _ns_2.get('transform') or _ns_2.get('transform')
    tmp_4['ENROLLMENT_TYPE'] = tmp_4['ENROLLMENT_TYPE'].apply(lambda s: _std_func_2(s) if pd.notna(s) else s)
    # Step 6: SelectCol
    result = tmp_4.loc[:, ['IAP_SUBJECT_SESSION_KEY', 'ACTIVITY_TITLE', 'TERM_CODE', 'ENROLLMENT_TYPE', 'MAX_ENROLLMENT', 'FEE', 'IS_MULTIPLE_SESSION', 'IS_CANCELLED']].copy()
    return result

prepared_table_1 = _prepare_table_1(tables.get('table_1', pd.DataFrame()))

def _prepare_table_2(_source):
    df = _source.copy()
    # Step 1: Rename
    tmp_0 = df.rename(columns={'iap_subject_session_key': 'IAP_SUBJECT_SESSION_KEY'})
    # Step 2: StandardizeString
    tmp_1 = tmp_0.copy()
    _ns_1 = {}
    exec('def transform(s):\n    return str(s).strip().lower()', globals(), _ns_1)
    _std_func_1 = _ns_1.get('transform') or _ns_1.get('transform')
    tmp_1['SESSION_LOCATION'] = tmp_1['SESSION_LOCATION'].apply(lambda s: _std_func_1(s) if pd.notna(s) else s)
    # Step 3: SelectCol
    result = tmp_1.loc[:, ['IAP_SUBJECT_SESSION_KEY', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME', 'HAS_SESSION_INFO']].copy()
    return result

prepared_table_2 = _prepare_table_2(tables.get('table_2', pd.DataFrame()))

# Stage-2 program over the prepared tables.
merged = prepared_table_1.merge(prepared_table_2, how='inner', on='IAP_SUBJECT_SESSION_KEY')
# Identify virtual sessions using broad, case-insensitive matching on location
loc = merged['SESSION_LOCATION'].astype(str).str.strip()
virtual_mask = loc.str.len().gt(0) & (
    loc.str.lower().str.contains('virtual') |
    loc.str.lower().str.contains('zoom') |
    loc.str.lower().str.contains('online') |
    loc.str.lower().str.contains('remote') |
    loc.str.lower().str.contains('webex') |
    loc.str.lower().str.contains('teams')
)
virtual = merged[virtual_mask].copy()
# If no rows matched, fall back to all merged rows rather than empty
if virtual.empty:
    virtual = merged.copy()
# Parse start/end times like '1100AM', '1200PM' to minutes since midnight
def parse_time_col(s):
    s = s.astype(str).str.strip()
    # pad to ensure AM/PM suffix present and numeric part separated
    ampm = s.str[-2:].str.upper()
    num = s.str[:-2]
    # normalize numeric to 3-4 digits (e.g., 900 -> 0900)
    num = num.str.replace(r'[^0-9]', '', regex=True)
    num = num.apply(lambda x: ('0000' + x)[-4:] if len(x)>0 else '')
    hh = num.str[:2]
    mm = num.str[2:4]
    # coerce to ints safely
    hh_int = hh.where(hh!='', None).astype(float)
    mm_int = mm.where(mm!='', None).astype(float)
    # convert to 24h
    # minutes since midnight
    mins = hh_int*60 + mm_int
    # adjust for AM/PM
    is_pm = ampm=='PM'
    is_am = ampm=='AM'
    # add 12h for PM except 12PM
    add_pm = ((hh_int % 12) + 12) * 60 + mm_int
    keep_am = (hh_int % 12) * 60 + mm_int
    # choose based on suffix
    mins2 = mins.copy()
    mins2[is_pm] = add_pm[is_pm]
    mins2[is_am] = keep_am[is_am]
    return mins2
virtual['start_min'] = parse_time_col(virtual['SESSION_START_TIME'])
virtual['end_min'] = parse_time_col(virtual['SESSION_END_TIME'])
# duration in minutes where both parsed
virtual['duration_min'] = virtual['end_min'] - virtual['start_min']
# Aggregate: total number of unique subjects (sessions), total fee across subjects, and min/max duration across virtual session occurrences
# Unique subjects counted by IAP_SUBJECT_SESSION_KEY present in virtual rows
total_subjects = virtual['IAP_SUBJECT_SESSION_KEY'].nunique()
# Total fee: sum unique subject fees once per subject (some subjects have multiple session rows)
fees_per_subject = virtual.drop_duplicates(subset=['IAP_SUBJECT_SESSION_KEY'])[['IAP_SUBJECT_SESSION_KEY','FEE']]
# coerce FEE to numeric (already cast upstream), handle NaN as 0 for total fee
total_fee = fees_per_subject['FEE'].fillna(0).sum()
# Shortest and longest session durations among rows with valid duration
valid_dur = virtual['duration_min'].dropna()
shortest = valid_dur.min() if not valid_dur.empty else None
longest = valid_dur.max() if not valid_dur.empty else None
# Build single-row result DataFrame
target = virtual.head(0).copy()
target = target.assign(
    total_subjects=[total_subjects],
    total_fee=[total_fee],
    shortest_session_minutes=[shortest],
    longest_session_minutes=[longest]
)[['total_subjects','total_fee','shortest_session_minutes','longest_session_minutes']]

if isinstance(target, pd.Series):
    target = target.to_frame().reset_index(drop=True)
elif isinstance(target, (list, tuple)):
    target = pd.DataFrame(target)
elif isinstance(target, dict) and not isinstance(target, pd.DataFrame):
    target = pd.DataFrame(target)
elif not isinstance(target, pd.DataFrame):
    target = pd.DataFrame({'answer': [target]})

result = {'answer': target}
