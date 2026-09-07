import pandas as pd
import numpy as np
import re

# The input DataFrames are provided in a dict named `tables`
# Mapping per instructions:
# tables['table_3'] -> SUBJECT_IAP_SCHEDULE.pkl
# tables['table_1'] -> IAP_SUBJECT_DETAIL.pkl
# tables['table_2'] -> IAP_SUBJECT_SESSION.pkl
# Others are available but not required for this task.

# 1) Load DataFrame from provided tables dict
df_sched = tables['table_3'].copy()

# 2) Filter SUBJECT_IAP_SCHEDULE to virtual sessions (MEET_PLACE contains keywords)
def is_virtual(text):
    if pd.isna(text):
        return False
    t = str(text).lower()
    keywords = [
        "zoom", "virtual", "online", "webex", "mitx", "remote", "teams", "google meet",
        "livestream", "webinar", "videoconference", "video conference"
    ]
    return any(k in t for k in keywords)

df_sched['IS_VIRTUAL'] = df_sched['MEET_PLACE'].apply(is_virtual)
df_virtual = df_sched[df_sched['IS_VIRTUAL']].copy()

# 3) Normalize MEET_START_TIME and MEET_END_TIME to timedeltas for duration computation
def parse_time_str(t):
    if pd.isna(t):
        return pd.NaT
    s = str(t).strip().upper()
    s = re.sub(r'[^0-9APM:]', '', s)
    if ':' in s:
        if not any(x in s for x in ['AM', 'PM']):
            return pd.NaT
        ts = pd.to_datetime(s, format='%I:%M%p', errors='coerce')
        if pd.isna(ts):
            ts = pd.to_datetime(s, errors='coerce')
        return ts
    else:
        m = re.fullmatch(r'(\d{1,4})(AM|PM)', s)
        if not m:
            return pd.NaT
        digits, ap = m.groups()
        if len(digits) <= 2:
            hh = int(digits)
            mm = 0
        else:
            hh = int(digits[:-2])
            mm = int(digits[-2:])
        if not (0 <= hh <= 12 and 0 <= mm < 60):
            return pd.NaT
        formatted = f"{hh:02d}:{mm:02d}{ap}"
        ts = pd.to_datetime(formatted, format='%I:%M%p', errors='coerce')
        return ts

start_dt = df_virtual['MEET_START_TIME'].apply(parse_time_str)
end_dt = df_virtual['MEET_END_TIME'].apply(parse_time_str)

def to_time_delta(ts):
    if pd.isna(ts):
        return pd.NaT
    return pd.to_timedelta(ts.hour, unit='h') + pd.to_timedelta(ts.minute, unit='m') + pd.to_timedelta(ts.second, unit='s')

df_virtual['START_TD'] = start_dt.apply(to_time_delta)
df_virtual['END_TD'] = end_dt.apply(to_time_delta)

def compute_duration(start_td, end_td):
    if pd.isna(start_td) or pd.isna(end_td):
        return pd.NaT
    dur = end_td - start_td
    if pd.notna(dur) and dur < pd.Timedelta(0):
        dur = dur + pd.Timedelta(days=1)
    return dur

df_virtual['DURATION'] = [
    compute_duration(s, e) for s, e in zip(df_virtual['START_TD'], df_virtual['END_TD'])
]

# 4) Compute required metrics:
# - total number of subjects involved in virtual IAP sessions
# We need to identify unique SUBJECT_IDs. SUBJECT_ID may be NaN in schedule; if so, join via session if available.
# First, collect subject IDs present directly.
subject_ids_direct = df_virtual['SUBJECT_ID'] if 'SUBJECT_ID' in df_virtual.columns else pd.Series([], dtype='float64')

# If SUBJECT_ID missing or to be safe, also map via session table using keys present in schedule (TERM_CODE, SESSION_NUMBER).
# Attempt a left merge with IAP_SUBJECT_SESSION to fetch SUBJECT_IDs where missing.
df_sess = tables['table_2'].copy()
merge_keys = [k for k in ['TERM_CODE', 'SESSION_NUMBER'] if k in df_virtual.columns and k in df_sess.columns]
if len(merge_keys) > 0:
    df_map = df_virtual[merge_keys].drop_duplicates()
    df_map = df_map.merge(df_sess[merge_keys + ['SUBJECT_ID']].drop_duplicates(), on=merge_keys, how='left')
    subject_ids_from_sess = df_map['SUBJECT_ID']
else:
    subject_ids_from_sess = pd.Series([], dtype='float64')

# Combine subject IDs from both sources
subj_ids = pd.concat([subject_ids_direct, subject_ids_from_sess], ignore_index=True)
# Clean to unique non-null
subj_ids_unique = pd.Series(pd.unique(subj_ids.dropna()))

total_subjects = int(len(subj_ids_unique))

# - total fee: sum of fees for those subjects from IAP_SUBJECT_DETAIL (assuming FEE column)
df_detail = tables['table_1'].copy()
fee_col = None
for c in df_detail.columns:
    if c.upper() == 'FEE' or re.sub(r'\W+', '', c).upper() == 'FEE':
        fee_col = c
        break

if fee_col is not None and 'SUBJECT_ID' in df_detail.columns:
    fees = df_detail[df_detail['SUBJECT_ID'].isin(subj_ids_unique)][fee_col]
    # Coerce to numeric
    fees_num = pd.to_numeric(fees, errors='coerce')
    total_fee = float(fees_num.fillna(0).sum())
else:
    total_fee = float(0)

# - shortest and longest sessions by duration among virtual rows with valid durations
valid_dur = df_virtual[pd.notna(df_virtual['DURATION'])].copy()
if len(valid_dur) > 0:
    shortest_row = valid_dur.loc[valid_dur['DURATION'].idxmin()]
    longest_row = valid_dur.loc[valid_dur['DURATION'].idxmax()]
    shortest_duration = shortest_row['DURATION']
    longest_duration = longest_row['DURATION']
else:
    shortest_duration = pd.NaT
    longest_duration = pd.NaT

# Prepare a one-row DataFrame with the answers
answer_df = pd.DataFrame([{
    'total_subjects': total_subjects,
    'total_fee': total_fee,
    'shortest_session_duration': pd.to_timedelta(shortest_duration) if pd.notna(shortest_duration) else pd.NaT,
    'longest_session_duration': pd.to_timedelta(longest_duration) if pd.notna(longest_duration) else pd.NaT
}])

# Package final result
result = {'virtual_iap_summary': answer_df}