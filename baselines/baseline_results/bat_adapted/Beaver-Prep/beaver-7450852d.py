import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['IAP_SUBJECT_SESSION_KEY','TERM_CODE','ENROLLMENT_TYPE','FEE','IS_CANCELLED','IS_MULTIPLE_SESSION']].copy()
    df = df.groupby('IAP_SUBJECT_SESSION_KEY', as_index=False).agg({'TERM_CODE':'first','ENROLLMENT_TYPE':'first','FEE':'first','IS_CANCELLED':'first','IS_MULTIPLE_SESSION':'first'})
    target = df[['IAP_SUBJECT_SESSION_KEY','TERM_CODE','ENROLLMENT_TYPE','FEE','IS_CANCELLED','IS_MULTIPLE_SESSION']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df = df.replace({'nan': pd.NA, 'NaN': pd.NA, 'NAN': pd.NA})
    df['SESSION_LOCATION'] = df['SESSION_LOCATION'].astype('string').str.strip()
    df['SESSION_START_TIME'] = df['SESSION_START_TIME'].astype('string').str.strip()
    df['SESSION_END_TIME'] = df['SESSION_END_TIME'].astype('string').str.strip()
    df['SESSION_DATE'] = df['SESSION_DATE'].astype('string').str.strip()
    df['HAS_SESSION_INFO'] = df['HAS_SESSION_INFO'].astype('string').str.strip()
    df['SESSION_DATE'] = pd.to_datetime(df['SESSION_DATE'], format='%d-%b-%y', errors='coerce').dt.strftime('%Y-%m-%d')
    target = df[['iap_subject_session_key','SESSION_LOCATION','SESSION_START_TIME','SESSION_END_TIME','SESSION_DATE','HAS_SESSION_INFO']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sessions = prepared_table_2

# Assume prepared_subjects and prepared_sessions are already materialized per the target schemas.

# Join subjects to sessions on the session key
joined = prepared_subjects.merge(
    prepared_sessions,
    left_on='IAP_SUBJECT_SESSION_KEY',
    right_on='iap_subject_session_key',
    how='inner'
)

# Filter to IAP term codes (TERM_CODE ending with 'JA' commonly denotes IAP) and non-cancelled subjects
joined = joined[(joined['TERM_CODE'].astype(str).str.contains('JA', na=False)) & (joined['IS_CANCELLED'] != 'Y')]

# Identify virtual sessions by location text
loc = joined['SESSION_LOCATION'].astype(str).str.lower()
virtual_mask = loc.str.contains('virtual', na=False) | loc.str.contains('zoom', na=False) | loc.str.contains('online', na=False)
virt = joined[virtual_mask].copy()

# Parse times to compute duration in minutes; coerce errors to NaT
# Normalize times like '1100AM', '1200PM', '1030AM'
def parse_time(s):
    s = str(s).strip().upper()
    if s == 'NAN' or s == '' or s == 'NA':
        return pd.NaT
    # Insert colon before last two digits if missing
    m = re.match(r'^(\d{1,2})(\d{2})(AM|PM)$', s)
    if m:
        h, mnt, ap = m.groups()
        return pd.to_datetime(f"{h}:{mnt} {ap}", format='%I:%M %p', errors='coerce')
    # Try generic parser
    return pd.to_datetime(s, format='%I:%M%p', errors='coerce')

start_ts = virt['SESSION_START_TIME'].map(parse_time)
end_ts = virt['SESSION_END_TIME'].map(parse_time)

# Compute duration in minutes, dropping rows without valid times
valid = start_ts.notna() & end_ts.notna()
virt_valid = virt[valid].copy()
virt_valid['duration_min'] = (end_ts[valid] - start_ts[valid]).dt.total_seconds() / 60.0

# Total number of subjects involved in virtual sessions (distinct IAP subject session keys)
num_subjects = virt_valid['IAP_SUBJECT_SESSION_KEY'].nunique()

# Total fee across those subjects; treat missing as 0, sum distinct per subject to avoid double-counting across multiple session rows
fees = virt_valid[['IAP_SUBJECT_SESSION_KEY', 'FEE']].drop_duplicates('IAP_SUBJECT_SESSION_KEY').copy()
fees['FEE'] = pd.to_numeric(fees['FEE'], errors='coerce').fillna(0)
total_fee = float(fees['FEE'].sum())

# Shortest and longest session durations among virtual sessions (in minutes)
shortest = float(virt_valid['duration_min'].min()) if not virt_valid.empty else None
longest = float(virt_valid['duration_min'].max()) if not virt_valid.empty else None

answer = {
    'total_subjects': int(num_subjects),
    'total_fee': total_fee,
    'shortest_session_minutes': shortest,
    'longest_session_minutes': longest
}

target = pd.DataFrame([answer])

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
