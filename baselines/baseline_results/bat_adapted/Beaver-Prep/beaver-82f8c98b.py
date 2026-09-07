import pandas as pd
import numpy as np

def _prep_1(table_1):
    source = table_1.copy()
    source['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(source['NUM_ENROLLED_STUDENTS'], errors='coerce')
    target = source[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','NUM_ENROLLED_STUDENTS']].drop_duplicates()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','subject_id','TIP_MATERIAL_KEY']].copy()
    df = df.drop_duplicates()
    target = df[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','subject_id','TIP_MATERIAL_KEY']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['TIP_MATERIAL_KEY','RENTAL_NEW_PRICE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
subjects_by_dept = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
subject_material_links = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
material_prices = prepared_table_3

# Merge subjects with material links on TIP_SUBJECT_OFFERED_KEY (restrict to matching TERM_CODE where available)
links = subject_material_links
subs = subjects_by_dept
# If TERM_CODE exists on both, enforce equality to avoid cross-term bleed
merged_sl = subs.merge(links, on='TIP_SUBJECT_OFFERED_KEY', how='left', suffixes=('', '_lk'))
if 'TERM_CODE_lk' in merged_sl.columns:
    # In case merge created TERM_CODE_lk from links; filter rows where terms match or links missing
    term_match = (merged_sl['TERM_CODE_lk'].isna()) | (merged_sl['TERM_CODE'] == merged_sl['TERM_CODE_lk'])
    merged_sl = merged_sl.loc[term_match].drop(columns=[c for c in ['TERM_CODE_lk'] if c in merged_sl.columns])

# Bring in rental new prices
merged_full = merged_sl.merge(material_prices, on='TIP_MATERIAL_KEY', how='left')

# Clean numeric types
subs_cols = ['NUM_ENROLLED_STUDENTS']
for c in subs_cols:
    if c in merged_full.columns:
        merged_full[c] = pd.to_numeric(merged_full[c], errors='coerce')
merged_full['RENTAL_NEW_PRICE'] = pd.to_numeric(merged_full['RENTAL_NEW_PRICE'], errors='coerce')

# Compute per-department aggregates
# - department name
# - total number of types of TIP subjects (distinct SUBJECT_ID)
# - total enrolled students (sum NUM_ENROLLED_STUDENTS across offerings; then group by dept)
# - min/max rental new price (ignoring NaN/zero-only if desired; here include non-null values)

# Distinct subjects per department
distinct_subjects = merged_full[['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'SUBJECT_ID']].drop_duplicates()
subjects_count = distinct_subjects.groupby(['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], as_index=False).agg(total_tip_subject_types=('SUBJECT_ID', 'nunique'))

# Total enrolled students per department (from subject offerings)
enrollment = subs.groupby(['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], as_index=False)['NUM_ENROLLED_STUDENTS'].sum().rename(columns={'NUM_ENROLLED_STUDENTS':'total_enrolled_students'})

# Min/max rental new price per department (from materials joined to subjects)
price_agg = merged_full[['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME', 'RENTAL_NEW_PRICE']].dropna()
price_agg = price_agg.groupby(['OFFER_DEPT_CODE', 'OFFER_DEPT_NAME'], as_index=False).agg(
    min_rental_new_price=('RENTAL_NEW_PRICE','min'),
    max_rental_new_price=('RENTAL_NEW_PRICE','max')
)

# Combine all
result = subjects_count.merge(enrollment, on=['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], how='outer')\
                     .merge(price_agg, on=['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], how='left')

# Final select and rename for clarity
answer = result.rename(columns={'OFFER_DEPT_NAME':'department_name'})[
    ['department_name', 'total_tip_subject_types', 'total_enrolled_students', 'min_rental_new_price', 'max_rental_new_price']
]

answer = answer.sort_values('department_name').reset_index(drop=True)

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
