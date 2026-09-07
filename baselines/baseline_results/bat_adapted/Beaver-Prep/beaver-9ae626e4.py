import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['IAP_SUBJECT_SPONSOR_KEY','IAP_SUBJECT_SESSION_KEY','IAP_SUBJECT_CATEGORY_KEY']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['IAP_SUBJECT_SPONSOR_KEY','IAP_SUBJECT_SESSION_KEY','IAP_SUBJECT_CATEGORY_KEY']]
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
    prepared = table_1[['iap_subject_session_key']].copy()
    prepared = prepared.dropna(subset=['iap_subject_session_key'])
    prepared = prepared.drop_duplicates(subset=['iap_subject_session_key']).reset_index(drop=True)
    target = prepared[['iap_subject_session_key']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_sponsors = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_sessions = prepared_table_3

# Merge subjects with sessions to ensure we count valid sessions
sub_sess = prepared_subjects.merge(
    prepared_sessions, left_on='IAP_SUBJECT_SESSION_KEY', right_on='iap_subject_session_key', how='left'
)

# Aggregate per sponsor: count distinct session keys and distinct subjects (using category key as subject identifier)
agg = sub_sess.groupby('IAP_SUBJECT_SPONSOR_KEY').agg(
    num_iap_sessions=pd.NamedAgg(column='IAP_SUBJECT_SESSION_KEY', aggfunc=lambda s: s.dropna().nunique()),
    num_unique_subjects=pd.NamedAgg(column='IAP_SUBJECT_CATEGORY_KEY', aggfunc=lambda s: s.dropna().nunique())
).reset_index()

# Attach sponsor names
result = agg.merge(prepared_sponsors, on='IAP_SUBJECT_SPONSOR_KEY', how='left')[
    ['SPONSOR_NAME', 'num_iap_sessions', 'num_unique_subjects']
].sort_values('SPONSOR_NAME', kind='stable')

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
