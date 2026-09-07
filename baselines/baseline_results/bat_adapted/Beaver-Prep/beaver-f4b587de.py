import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['IAP_SUBJECT_SESSION_KEY','TERM_CODE','ACTIVITY_TITLE','ENROLLMENT_TYPE','IAP_SUBJECT_PERSON_KEY']].copy()
    prepared = prepared.drop_duplicates(subset=['IAP_SUBJECT_SESSION_KEY','TERM_CODE','ACTIVITY_TITLE','ENROLLMENT_TYPE','IAP_SUBJECT_PERSON_KEY'])
    target = prepared[['IAP_SUBJECT_SESSION_KEY','TERM_CODE','ACTIVITY_TITLE','ENROLLMENT_TYPE','IAP_SUBJECT_PERSON_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import pandas as pd
    df = table_1[['iap_subject_session_key','SESSION_LOCATION','SESSION_DATE','SESSION_START_TIME','SESSION_END_TIME']].copy()
    df = df.replace({'nan': pd.NA, 'NaN': pd.NA, '': pd.NA})
    df['SESSION_LOCATION'] = df['SESSION_LOCATION'].astype('string').str.strip()
    df['SESSION_LOCATION'] = df['SESSION_LOCATION'].replace({'<NA>': pd.NA})
    df['SESSION_DATE'] = pd.to_datetime(df['SESSION_DATE'], format='%d-%b-%y', errors='coerce').dt.strftime('%Y-%m-%d')
    df['SESSION_START_TIME'] = pd.to_datetime(df['SESSION_START_TIME'], format='%I%M%p', errors='coerce').dt.strftime('%H:%M:%S')
    df['SESSION_END_TIME'] = pd.to_datetime(df['SESSION_END_TIME'], format='%I%M%p', errors='coerce').dt.strftime('%H:%M:%S')
    target = df[['iap_subject_session_key','SESSION_LOCATION','SESSION_DATE','SESSION_START_TIME','SESSION_END_TIME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['term_code','TERM_START_DATE']].copy()
    df['TERM_START_DATE'] = df['TERM_START_DATE'].replace({'nan': pd.NA, 'NaN': pd.NA, 'None': pd.NA, '': pd.NA})
    df['TERM_START_DATE'] = pd.to_datetime(df['TERM_START_DATE'], format='%d-%b-%y', errors='coerce')
    target = df[['term_code','TERM_START_DATE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_iap_sessions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_8'])
prepared_terms = prepared_table_3

# Assume prepared_iap_subjects, prepared_iap_sessions, prepared_terms are dataframes built per table_targets

# 1) Join subjects to sessions on session key
s = prepared_iap_subjects.merge(
    prepared_iap_sessions,
    left_on='IAP_SUBJECT_SESSION_KEY',
    right_on='iap_subject_session_key',
    how='left'
)

# 2) Join to terms on term_code to get term start date
s = s.merge(
    prepared_terms[['term_code', 'TERM_START_DATE']],
    left_on='TERM_CODE',
    right_on='term_code',
    how='left'
)

# 3) Filter to independent activities (case-insensitive contains 'independent' in ENROLLMENT_TYPE)
mask = s['ENROLLMENT_TYPE'].astype(str).str.contains('independent', case=True, na=False)
s = s[mask]

# 4) Select and rename output columns
out = s[[
    'ACTIVITY_TITLE',
    'SESSION_LOCATION',
    'TERM_START_DATE',
    'IAP_SUBJECT_PERSON_KEY'
]].rename(columns={
    'ACTIVITY_TITLE': 'activity_title',
    'SESSION_LOCATION': 'location',
    'TERM_START_DATE': 'term_start_date',
    'IAP_SUBJECT_PERSON_KEY': 'supervisor_name'  # Placeholder: actual name lookup would require a person dimension not provided here
})

# 5) Deduplicate and sort by ascending term_start_date
out = out.drop_duplicates().sort_values(by=['term_start_date', 'activity_title'], ascending=[True, True])

# Final result in 'out'
target = out

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
