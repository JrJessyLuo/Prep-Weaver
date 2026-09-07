import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['ID','Birthday','Diagnosis_Part1','Diagnosis_Part2']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.loc[:, ['ID', 'Date', 'HGB']].copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    target = df[['ID', 'Date', 'HGB']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
patients_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs_prepared = prepared_table_2

# Assume patients_prepared and labs_prepared are available DataFrames
# 1) Clean and typecast
lp = labs_prepared.copy()
pt = patients_prepared.copy()

# Ensure numeric HGB and parse dates
lp['HGB'] = pd.to_numeric(lp['HGB'], errors='coerce')
lp['Date'] = pd.to_datetime(lp['Date'], errors='coerce')
pt['Birthday'] = pd.to_datetime(pt['Birthday'], errors='coerce')

# 2) Drop rows with missing essentials
lp = lp.dropna(subset=['ID', 'Date', 'HGB'])
pt = pt.dropna(subset=['ID', 'Birthday'])

# 3) Integrate on patient ID
merged = lp.merge(pt, on='ID', how='inner')

# 4) Compute age at exam (in years, floor)
age_in_years = (merged['Date'] - merged['Birthday']).dt.days // 365
merged['AgeAtExam'] = age_in_years

# 5) Find the record with the highest hemoglobin
idx = merged['HGB'].idxmax()
row = merged.loc[idx]

# 6) Compose doctor's diagnosis
diag_parts = [str(row.get('Diagnosis_Part1', '') or ''), str(row.get('Diagnosis_Part2', '') or '')]
diag = ' '.join(p for p in diag_parts if p and p.lower() != 'none').strip()

# 7) Final answer payload
answer = {
    'age_at_exam_years': int(row['AgeAtExam']) if pd.notnull(row['AgeAtExam']) else None,
    'doctor_diagnosis': diag if diag else None,
    'max_hemoglobin': float(row['HGB']) if pd.notnull(row['HGB']) else None,
    'patient_id': int(row['ID']) if pd.notnull(row['ID']) else None,
    'exam_date': row['Date'].date().isoformat() if pd.notnull(row['Date']) else None
}

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
