import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['TERM_CODE','IAP_SUBJECT_SESSION_KEY','FEE','MAX_ENROLLMENT']].copy()
    df['FEE'] = pd.to_numeric(df['FEE'], errors='coerce')
    df['MAX_ENROLLMENT'] = pd.to_numeric(df['MAX_ENROLLMENT'], errors='coerce')
    target = df.drop_duplicates(subset=['TERM_CODE','IAP_SUBJECT_SESSION_KEY','FEE','MAX_ENROLLMENT']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['term_code','TERM_DESCRIPTION']].copy()
    prepared = prepared.drop_duplicates(subset=['term_code'])
    target = prepared[['term_code','TERM_DESCRIPTION']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
iap_sessions_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
terms_prepared = prepared_table_2

# Assume iap_sessions_prepared and terms_prepared are dataframes created from the respective table_targets
# Clean and ensure correct dtypes
s = iap_sessions_prepared.copy()
# Convert FEE and MAX_ENROLLMENT to numeric, coerce errors to NaN
s['FEE'] = pd.to_numeric(s['FEE'], errors='coerce')
s['MAX_ENROLLMENT'] = pd.to_numeric(s['MAX_ENROLLMENT'], errors='coerce')

# Aggregate per term
agg = s.groupby('TERM_CODE', as_index=False).agg(
    TOTAL_IAP_SESSIONS=('IAP_SUBJECT_SESSION_KEY', 'nunique'),
    TOTAL_FEE_COLLECTED=('FEE', 'sum'),
    MIN_ENROLLMENT=('MAX_ENROLLMENT', 'min'),
    MAX_ENROLLMENT=('MAX_ENROLLMENT', 'max')
)

# Join to term descriptions
result = agg.merge(terms_prepared, left_on='TERM_CODE', right_on='term_code', how='left')

# Select and order columns as requested
result = result[[
    'TERM_CODE',
    'TERM_DESCRIPTION',
    'TOTAL_IAP_SESSIONS',
    'TOTAL_FEE_COLLECTED',
    'MIN_ENROLLMENT',
    'MAX_ENROLLMENT'
]].sort_values('TERM_CODE')

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
