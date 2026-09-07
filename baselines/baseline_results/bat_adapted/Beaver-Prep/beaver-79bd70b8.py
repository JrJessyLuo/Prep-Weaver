import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['IAP_SUBJECT_SPONSOR_KEY','IAP_SUBJECT_SESSION_KEY','TERM_CODE','MAX_ENROLLMENT','FEE','IS_CANCELLED']].copy()
    df['MAX_ENROLLMENT'] = pd.to_numeric(df['MAX_ENROLLMENT'], errors='coerce')
    df['FEE'] = pd.to_numeric(df['FEE'], errors='coerce')
    target = df.drop_duplicates()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['IAP_SUBJECT_SPONSOR_KEY','SPONSOR_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['iap_subject_session_key','HAS_SESSION_INFO']].copy()
    df['HAS_SESSION_INFO'] = df['HAS_SESSION_INFO'].astype('string').str.strip().replace({'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA})
    df = df.groupby('iap_subject_session_key', as_index=False)['HAS_SESSION_INFO'].max()
    target = df[['iap_subject_session_key','HAS_SESSION_INFO']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
iap_sponsors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
iap_sessions = prepared_table_3

# Assume prepared tables: iap_subjects, iap_sponsors, iap_sessions
# 1) Join subjects to sponsors for names
sub_with_names = iap_subjects.merge(iap_sponsors, on='IAP_SUBJECT_SPONSOR_KEY', how='left')

# 2) Join subjects to sessions to get HAS_SESSION_INFO per session key
sub_with_sess = sub_with_names.merge(iap_sessions, left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key', how='left')

# 3) Derive helper flags
# Consider a session to have info if HAS_SESSION_INFO == 'Y'
sub_with_sess['has_info_flag'] = (sub_with_sess['HAS_SESSION_INFO'] == 'Y').astype(int)
sub_with_sess['no_info_flag'] = ((sub_with_sess['HAS_SESSION_INFO'] == 'N') | sub_with_sess['HAS_SESSION_INFO'].isna()).astype(int)

# 4) Aggregate per sponsor name
agg = sub_with_sess.groupby(['IAP_SUBJECT_SPONSOR_KEY','SPONSOR_NAME'], dropna=False).agg(
    sessions_held = ('IAP_SUBJECT_SESSION_KEY','nunique'),
    total_enrollment = ('MAX_ENROLLMENT', lambda s: pd.to_numeric(s, errors='coerce').sum(min_count=1)),
    min_fee = ('FEE', lambda s: pd.to_numeric(s, errors='coerce').min()),
    max_fee = ('FEE', lambda s: pd.to_numeric(s, errors='coerce').max()),
    sessions_with_info = ('has_info_flag','sum'),
    sessions_without_info = ('no_info_flag','sum')
).reset_index()

# 5) Select and rename columns for output
answer = agg[['SPONSOR_NAME','sessions_held','total_enrollment','min_fee','max_fee','sessions_with_info','sessions_without_info']]

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
