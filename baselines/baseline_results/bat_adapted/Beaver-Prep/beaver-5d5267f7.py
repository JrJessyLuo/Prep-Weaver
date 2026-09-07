import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['TIP_MATERIAL_STATUS_KEY','TIP_MATERIAL_KEY','subject_id','TERM_CODE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['tip_material_status_key','TIP_MATERIAL_STATUS']].copy()
    df['TIP_MATERIAL_STATUS'] = df['TIP_MATERIAL_STATUS'].replace({'nan': pd.NA, 'NaN': pd.NA, 'NAN': pd.NA})
    target = df[['tip_material_status_key','TIP_MATERIAL_STATUS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['SUBJECT_ID','DEPARTMENT_NAME']].copy()
    df['DEPARTMENT_NAME'] = df['DEPARTMENT_NAME'].replace('nan', pd.NA)
    target = df.groupby('SUBJECT_ID', as_index=False)['DEPARTMENT_NAME'].first()[['SUBJECT_ID','DEPARTMENT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_material_usage = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_material_status_lu = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_subjects = prepared_table_3

# Assume prepared dataframes: prepared_material_usage, prepared_material_status_lu, prepared_subjects

# Normalize join keys/cases
mu = prepared_material_usage.copy()
sl = prepared_material_status_lu.copy()
subj = prepared_subjects.copy()

# Join to status lookup
mu_sl = mu.merge(sl, left_on='TIP_MATERIAL_STATUS_KEY', right_on='tip_material_status_key', how='left')

# Join to subjects to get school/department
mu_full = mu_sl.merge(subj, left_on='subject_id', right_on='SUBJECT_ID', how='left')

# Derive publication year from TERM_CODE when possible (e.g., '2016FA' -> 2016)
def extract_year(term):
    if pd.isna(term):
        return pd.NA
    s = str(term)
    # take leading 4 digits if present
    return int(s[:4]) if len(s) >= 4 and s[:4].isdigit() else pd.NA

mu_full['PUB_YEAR'] = mu_full['TERM_CODE'].apply(extract_year)

# Group by material status (use description when available, else fall back to key)
status_name = mu_full['TIP_MATERIAL_STATUS'].fillna('')
status_fallback = mu_full['TIP_MATERIAL_STATUS_KEY'].fillna('')
mu_full['MATERIAL_STATUS'] = status_name.where(status_name.str.len() > 0, status_fallback)

# Compute aggregations per material status
agg = mu_full.groupby('MATERIAL_STATUS').agg(
    total_materials=('TIP_MATERIAL_KEY', lambda s: s.dropna().nunique()),
    total_subjects=('subject_id', lambda s: s.dropna().nunique()),
    total_schools=('DEPARTMENT_NAME', lambda s: s.dropna().nunique()),
    most_recent_publication_year=('PUB_YEAR', lambda s: s.dropna().max() if len(s.dropna())>0 else pd.NA)
).reset_index()

# Final result per material status
target = agg.sort_values('MATERIAL_STATUS')

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
