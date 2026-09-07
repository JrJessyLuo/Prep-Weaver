import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['ID', 'Date', 'RNP']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['Examination Date'] = pd.to_datetime(df['Examination Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    target = df[['ID', 'Examination Date', 'Symptoms', 'Diagnosis']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
labs_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
admissions_prepared = prepared_table_2

# Assume labs_prepared and admissions_prepared dataframes are available
# 1) Harmonize join key types
labs_prepared_h = labs_prepared.copy()
admissions_prepared_h = admissions_prepared.copy()

# Coerce IDs to string without decimal artifacts for robust joining
labs_prepared_h['ID_key'] = labs_prepared_h['ID'].astype(str).str.replace('\.0$', '', regex=True)
admissions_prepared_h['ID_key'] = admissions_prepared_h['ID'].astype(str).str.replace('\.0$', '', regex=True)

# 2) Define normal RNP (anti-ribonuclear protein) values: treat '-' or 'negative' (case-insensitive) as normal
# Keep non-null only
rnp_series = labs_prepared_h['RNP'].astype(str).str.strip().str.lower()
normal_mask = rnp_series.isin(['-', 'negative', 'neg', 'normal'])
normal_rnp = labs_prepared_h[normal_mask].copy()

# 3) Identify admitted patients from admissions_prepared. Use Symptoms/Diagnosis containing 'admit' or 'hospital' as proxy.
# (Adjust patterns as needed for dataset conventions.)
for col in ['Symptoms', 'Diagnosis']:
    if col in admissions_prepared_h.columns:
        admissions_prepared_h[col] = admissions_prepared_h[col].astype(str).str.lower()

admit_mask = (
    admissions_prepared_h['Symptoms'].str.contains('admit|hospital', na=False) |
    admissions_prepared_h['Diagnosis'].str.contains('admit|hospital', na=False)
)
admitted = admissions_prepared_h[admit_mask].copy()

# 4) Integrate on patient ID
merged = pd.merge(
    normal_rnp[['ID_key']].drop_duplicates(),
    admitted[['ID_key']].drop_duplicates(),
    on='ID_key', how='inner'
)

# 5) Count unique patients meeting both criteria
answer = len(merged['ID_key'].unique())

answer

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
