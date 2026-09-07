import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['iap_subject_person_key','PERSON_ROLE','PERSON_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['IAP_SUBJECT_PERSON_KEY','IAP_SUBJECT_CATEGORY_KEY','FEE']].copy()
    prepared['FEE'] = pd.to_numeric(prepared['FEE'], errors='coerce')
    target = prepared[['IAP_SUBJECT_PERSON_KEY','IAP_SUBJECT_CATEGORY_KEY','FEE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']].copy()
    prepared['IAP_SUBJECT_CATEGORY_KEY'] = prepared['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip()
    prepared['IAP_CATEGORY_NAME'] = prepared['IAP_CATEGORY_NAME'].astype(str).str.strip()
    target = prepared.drop_duplicates(subset=['IAP_SUBJECT_CATEGORY_KEY','IAP_CATEGORY_NAME']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_people = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_subjects = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_categories = prepared_table_3

# Assume prepared_people, prepared_subjects, prepared_categories are available DataFrames
# Clean potential whitespace in category keys to ensure joins
prepared_categories = prepared_categories.assign(IAP_SUBJECT_CATEGORY_KEY=prepared_categories['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip())
prepared_subjects = prepared_subjects.assign(IAP_SUBJECT_CATEGORY_KEY=prepared_subjects['IAP_SUBJECT_CATEGORY_KEY'].astype(str).str.strip())

# Join subjects to people by person key
sp = prepared_subjects.merge(
    prepared_people,
    left_on='IAP_SUBJECT_PERSON_KEY',
    right_on='iap_subject_person_key',
    how='inner'
)

# Join categories to get category name
spc = sp.merge(
    prepared_categories,
    on='IAP_SUBJECT_CATEGORY_KEY',
    how='left'
)

# Convert fee to numeric for averaging
spc['FEE'] = pd.to_numeric(spc['FEE'], errors='coerce')

# Group by role and category name: count distinct people in this role and compute average fee
result = (
    spc.groupby(['PERSON_ROLE', 'IAP_CATEGORY_NAME'])
       .agg(role_count=('PERSON_NAME', lambda s: s.nunique()),
            average_fee=('FEE', 'mean'))
       .reset_index()
)

# Sort by role_count descending
result = result.sort_values(['role_count', 'PERSON_ROLE', 'IAP_CATEGORY_NAME'], ascending=[False, True, True])

# Final columns
result = result[['PERSON_ROLE', 'IAP_CATEGORY_NAME', 'role_count', 'average_fee']]

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
