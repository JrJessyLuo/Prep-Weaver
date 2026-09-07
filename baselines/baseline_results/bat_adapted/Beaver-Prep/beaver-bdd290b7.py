import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['IAP_SUBJECT_PERSON_KEY','TERM_CODE','FEE','MAX_ENROLLMENT']].copy()
    df['FEE'] = pd.to_numeric(df['FEE'], errors='coerce')
    df['MAX_ENROLLMENT'] = pd.to_numeric(df['MAX_ENROLLMENT'], errors='coerce')
    target = df.drop_duplicates(subset=['IAP_SUBJECT_PERSON_KEY','TERM_CODE','FEE','MAX_ENROLLMENT']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import numpy as np
    df = table_1[['iap_subject_person_key','PERSON_NAME','PERSON_EMAIL']].copy()
    df['PERSON_NAME'] = df['PERSON_NAME'].replace({'nan': np.nan, 'NaN': np.nan, '': np.nan})
    df['PERSON_EMAIL'] = df['PERSON_EMAIL'].replace({'nan': np.nan, 'NaN': np.nan, '': np.nan})
    target = df.groupby('iap_subject_person_key', as_index=False).agg({'PERSON_NAME': lambda s: s.dropna().iloc[0] if s.dropna().shape[0] else np.nan, 'PERSON_EMAIL': lambda s: s.dropna().iloc[0] if s.dropna().shape[0] else np.nan})[['iap_subject_person_key','PERSON_NAME','PERSON_EMAIL']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
iap_persons = prepared_table_2

# Assume prepared tables are provided as dataframes: iap_subjects, iap_persons
# 1) Integrate on person key
merged = iap_subjects.merge(iap_persons, left_on='IAP_SUBJECT_PERSON_KEY', right_on='iap_subject_person_key', how='left')

# 2) Derive academic year from TERM_CODE (e.g., '2021JA' -> '2021')
merged['ACADEMIC_YEAR'] = merged['TERM_CODE'].astype(str).str[:4]

# 3) Ensure numeric types for aggregations
merged['FEE_num'] = pd.to_numeric(merged['FEE'], errors='coerce')
merged['MAX_ENROLLMENT_num'] = pd.to_numeric(merged['MAX_ENROLLMENT'], errors='coerce')

# 4) Aggregate per individual and academic year
agg = (
    merged.groupby(['iap_subject_person_key','PERSON_EMAIL','PERSON_NAME','ACADEMIC_YEAR'], dropna=False)
          .agg(
              total_iap_subjects=('IAP_SUBJECT_PERSON_KEY','size'),
              min_fee=('FEE_num','min'),
              max_fee=('FEE_num','max'),
              total_course_enrollment=('MAX_ENROLLMENT_num','sum')
          )
          .reset_index()
)

# 5) Select and rename columns for the final answer
answer = agg.rename(columns={
    'PERSON_EMAIL': 'email',
    'PERSON_NAME': 'name',
    'ACADEMIC_YEAR': 'academic_year',
    'total_iap_subjects': 'total_number_of_IAP_subjects',
    'min_fee': 'minimum_fee',
    'max_fee': 'maximum_fee',
    'total_course_enrollment': 'total_course_enrollment'
})

target = answer[['email','name','academic_year','total_number_of_IAP_subjects','minimum_fee','maximum_fee','total_course_enrollment']]

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
