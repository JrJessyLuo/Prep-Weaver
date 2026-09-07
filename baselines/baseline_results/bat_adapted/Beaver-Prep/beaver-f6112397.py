import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['IAP_SUBJECT_CATEGORY_KEY','TERM_CODE','FEE','MAX_ENROLLMENT']].copy()
    df['TERM_CODE'] = df['TERM_CODE'].astype(str).str.strip()
    df['FEE'] = pd.to_numeric(df['FEE'], errors='coerce')
    df['MAX_ENROLLMENT'] = pd.to_numeric(df['MAX_ENROLLMENT'], errors='coerce')
    target = df[['IAP_SUBJECT_CATEGORY_KEY','TERM_CODE','FEE','MAX_ENROLLMENT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']].copy()
    df['IAP_SUBJECT_CATEGORY_KEY'] = df['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip()
    target = df[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    term_years = table_1[['TERM_CODE','ACADEMIC_YEAR']].drop_duplicates()
    term_years = term_years.sort_values(['TERM_CODE','ACADEMIC_YEAR']).reset_index(drop=True)
    target = term_years[['TERM_CODE','ACADEMIC_YEAR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
iap_subjects = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
iap_categories = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
term_years = prepared_table_3

# Start from prepared tables
s = iap_subjects.copy()
# Normalize keys and numeric fields
s['IAP_SUBJECT_CATEGORY_KEY'] = s['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip()
# Coerce fee and max enrollment to numeric, treating non-numeric as NaN
s['FEE'] = pd.to_numeric(s['FEE'], errors='coerce')
s['MAX_ENROLLMENT'] = pd.to_numeric(s['MAX_ENROLLMENT'], errors='coerce')

cats = iap_categories.copy()
cats['IAP_SUBJECT_CATEGORY_KEY'] = cats['IAP_SUBJECT_CATEGORY_KEY'].astype(str).strip()

terms = term_years.copy()

# Join to get academic year
sj = s.merge(terms[['TERM_CODE','ACADEMIC_YEAR']].drop_duplicates(), on='TERM_CODE', how='left')
# Join to get category name
sj = sj.merge(cats[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']].drop_duplicates(), on='IAP_SUBJECT_CATEGORY_KEY', how='left')

# Aggregate by category and academic year
result = (
    sj.groupby(['IAP_CATEGORY_NAME','ACADEMIC_YEAR'], dropna=False)
      .agg(
          total_fee_collected = ('FEE', lambda x: pd.Series(x).dropna().sum()),
          total_iap_subjects = ('TERM_CODE', 'count'),
          min_enrollment = ('MAX_ENROLLMENT', 'min'),
          max_enrollment = ('MAX_ENROLLMENT', 'max')
      )
      .reset_index()
      .rename(columns={'IAP_CATEGORY_NAME':'category_name','ACADEMIC_YEAR':'academic_year'})
)

# Optional sorting for readability
result = result.sort_values(['category_name','academic_year'])

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
