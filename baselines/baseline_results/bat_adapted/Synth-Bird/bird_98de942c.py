import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['ID','Examination Date','Diagnosis']].copy()
    df['Examination Date'] = pd.to_datetime(df['Examination Date'], errors='coerce')
    df['Examination Date'] = df['Examination Date'].dt.strftime('%Y-%m-%d')
    target = df[['ID','Examination Date','Diagnosis']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['ID','Date']].copy()
    target['Date'] = pd.to_datetime(target['Date'], errors='coerce').dt.normalize()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
patients_diagnosis = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
lab_results = prepared_table_2

# Ensure consistent ID typing (table_1 had float-like strings, table_2 had ints)
patients_diagnosis['ID'] = patients_diagnosis['ID'].astype(str).str.replace('.0$', '', regex=True).str.strip()
lab_results['ID'] = lab_results['ID'].astype(str).str.strip()

# Filter for the specific patient
pid = '30609'
pat = patients_diagnosis[patients_diagnosis['ID'] == pid]

# Get all lab test dates for this patient
labs = lab_results[lab_results['ID'] == pid][['Date']].dropna().drop_duplicates().sort_values('Date')

# Extract diagnosis (could be multiple rows; collect unique non-null values)
diagnosis_vals = pat['Diagnosis'].dropna().astype(str).str.strip().unique().tolist()
diagnosis = ', '.join([d for d in diagnosis_vals if d]) if diagnosis_vals else ''

# Prepare final answer structure
answer = {
    'patient_id': pid,
    'diagnosis': diagnosis,
    'lab_test_dates': labs['Date'].tolist()
}

target = pd.DataFrame([answer])

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
