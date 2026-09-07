import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['IAP_SUBJECT_CATEGORY_KEY','IAP_SUBJECT_SPONSOR_KEY','IAP_SUBJECT_SESSION_KEY','ACTIVITY_TITLE','IS_MULTIPLE_SESSION','IS_CANCELLED','TERM_CODE']
    target = table_1.loc[:, cols].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']].copy()
    df['IAP_SUBJECT_CATEGORY_KEY'] = df['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip()
    df['IAP_CATEGORY_NAME'] = df['IAP_CATEGORY_NAME'].astype(str).str.strip()
    target = df.drop_duplicates(subset=['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['IAP_SUBJECT_SPONSOR_KEY','SPONSOR_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['iap_subject_session_key','SESSION_TITLE','SESSION_START_TIME','SESSION_END_TIME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
iap_categories = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
iap_sponsors = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
iap_sessions = prepared_table_4

# Assume prepared DataFrames: iap_subjects, iap_categories, iap_sponsors, iap_sessions

# Integrate lookups
subjects_cat = iap_subjects.merge(iap_categories, on='IAP_SUBJECT_CATEGORY_KEY', how='left')
subjects_cat_spon = subjects_cat.merge(iap_sponsors, on='IAP_SUBJECT_SPONSOR_KEY', how='left')

# Join sessions (one-to-many). Keep session fields for listing; count sessions per subject.
subj_sess = subjects_cat_spon.merge(iap_sessions, left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key', how='left')

# Compute total number of sessions per subject key
session_counts = iap_sessions.groupby('iap_subject_session_key', dropna=False).size().rename('TOTAL_SESSIONS').reset_index()
result = subj_sess.merge(session_counts, left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key', how='left')

# Select and present requested fields
result = result[[
    'ACTIVITY_TITLE',                # subject title
    'IAP_CATEGORY_NAME',            # category name
    'SESSION_TITLE',                # session title
    'SESSION_START_TIME',
    'SESSION_END_TIME',
    'SPONSOR_NAME',                 # sponsor name
    'TOTAL_SESSIONS'                # total sessions for the subject
]].sort_values(['ACTIVITY_TITLE', 'SESSION_TITLE'], na_position='last')

target = result

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
