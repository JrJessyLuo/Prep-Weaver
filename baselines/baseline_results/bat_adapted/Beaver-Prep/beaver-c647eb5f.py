import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df = df.replace({'nan': pd.NA, 'NaN': pd.NA, 'NAN': pd.NA})
    df['iap_subject_session_key'] = df['iap_subject_session_key'].astype('string')
    df['SESSION_LOCATION'] = df['SESSION_LOCATION'].astype('string').str.strip()
    df['SESSION_DATE'] = df['SESSION_DATE'].astype('string').str.strip()
    df['SESSION_START_TIME'] = df['SESSION_START_TIME'].astype('string').str.strip()
    df['SESSION_END_TIME'] = df['SESSION_END_TIME'].astype('string').str.strip()
    df = df.drop_duplicates(subset=['iap_subject_session_key'], keep='first')
    target = df[['iap_subject_session_key', 'SESSION_LOCATION', 'SESSION_DATE', 'SESSION_START_TIME', 'SESSION_END_TIME']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    subjects = table_1[['IAP_SUBJECT_SESSION_KEY','ACTIVITY_TITLE','FEE']].copy()
    subjects['FEE'] = pd.to_numeric(subjects['FEE'], errors='coerce')
    subjects['ACTIVITY_TITLE'] = subjects['ACTIVITY_TITLE'].replace({np.nan: None})
    prepared = subjects.groupby('IAP_SUBJECT_SESSION_KEY', as_index=False).agg({'ACTIVITY_TITLE': lambda s: s.dropna().iloc[0] if not s.dropna().empty else np.nan, 'FEE': lambda s: s.dropna().iloc[0] if not s.dropna().empty else np.nan})
    prepared['FEE'] = prepared['FEE'].fillna(0)
    target = prepared[['IAP_SUBJECT_SESSION_KEY','ACTIVITY_TITLE','FEE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_sessions = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subjects = prepared_table_2

# Merge sessions with subject/activity metadata on the session key
merged = prepared_sessions.merge(
    prepared_subjects,
    left_on='iap_subject_session_key',
    right_on='IAP_SUBJECT_SESSION_KEY',
    how='left'
)

# Normalize and filter to physical locations (exclude virtual/online markers)
loc = merged['SESSION_LOCATION'].astype(str).str.strip()
virtual_markers = ['virtual', 'zoom', 'online', 'remote']
mask_physical = ~loc.str.lower().fillna('').str.contains('|'.join(virtual_markers)) & (loc != '') & (loc.str.lower() != 'nan')
phys = merged.loc[mask_physical].copy()

# Parse times and compute duration (in minutes)

def parse_time(s):
    if pd.isna(s):
        return pd.NaT
    s = str(s).strip().upper()
    # Handle times like 1100AM, 1200PM, 1:30PM, etc.
    # Insert colon if missing
    if ':' not in s and len(s) in (5,6):
        # e.g., 1100AM -> 11:00AM, 0930AM -> 09:30AM
        ampm = s[-2:]
        core = s[:-2]
        if len(core) == 4:
            s = core[:2] + ':' + core[2:] + ampm
        elif len(core) == 3:
            s = core[:1] + ':' + core[1:] + ampm
    # Try multiple formats
    for fmt in ['%I:%M%p', '%I%p']:
        try:
            return pd.to_datetime(s, format=fmt, errors='raise')
        except Exception:
            continue
    return pd.NaT

phys['start_dt'] = phys['SESSION_START_TIME'].apply(parse_time)
phys['end_dt'] = phys['SESSION_END_TIME'].apply(parse_time)

# If end < start (spans noon/midnight parsing artifacts), add 12 hours where appropriate
cross_mask = (phys['start_dt'].notna() & phys['end_dt'].notna() & (phys['end_dt'] < phys['start_dt']))
phys.loc[cross_mask, 'end_dt'] = phys.loc[cross_mask, 'end_dt'] + pd.Timedelta(hours=12)

phys['duration_min'] = (phys['end_dt'] - phys['start_dt']).dt.total_seconds() / 60.0

# Coerce fee to numeric and treat NaN as 0 for total fee aggregation
phys['fee_num'] = pd.to_numeric(phys['FEE'], errors='coerce').fillna(0)

# Aggregate by physical location (building name/room string in SESSION_LOCATION)
agg = phys.groupby('SESSION_LOCATION', dropna=False).agg(
    total_subjects=('iap_subject_session_key', 'nunique'),
    total_fee=('fee_num', 'sum'),
    shortest_session_min=('duration_min', 'min'),
    longest_session_min=('duration_min', 'max')
).reset_index().rename(columns={'SESSION_LOCATION': 'building'})

# Final result per physical IAP session location
target = agg[['building', 'total_subjects', 'total_fee', 'shortest_session_min', 'longest_session_min']]

_answer_value = None
if 'answer' in locals():
    _answer_value = answer
elif 'target' in locals() and not isinstance(target, pd.DataFrame):
    _answer_value = target
elif 'result' in locals() and not isinstance(result, dict):
    _answer_value = result
elif 'result' in locals() and isinstance(result, dict) and 'answer' in result:
    _answer_value = result['answer']
elif 'target' in locals():
    _answer_value = target
if not isinstance(_answer_value, pd.DataFrame):
    _answer_value = pd.DataFrame({'answer': [_answer_value]})
result = {'answer': _answer_value}
