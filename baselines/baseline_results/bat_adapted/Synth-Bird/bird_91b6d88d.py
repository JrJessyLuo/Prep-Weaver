import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['ID','Examination Date','Diagnosis']].copy()
    df['Examination Date'] = pd.to_datetime(df['Examination Date'], errors='coerce')
    target = df[['ID','Examination Date','Diagnosis']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['ID', 'Date', 'TP']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
patients_diagnosis = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
lab_results = prepared_table_2

# Assume prepared tables exist as DataFrames: patients_diagnosis, lab_results
# 1) Identify SJS patients (case-insensitive, substring match in Diagnosis)
sjs_patients = patients_diagnosis[patients_diagnosis['Diagnosis'].astype(str).str.contains('SJS', case=False, na=False)]

# 2) Join on patient ID to get their TP measurements
sjs_labs = sjs_patients.merge(lab_results, on='ID', how='inner')

# 3) Define normal range for Total Protein (TP). If not specified, commonly ~6.0-8.3 g/dL.
# Adjust if dataset metadata specifies another range.
LOW, HIGH = 6.0, 8.3

# Ensure TP is numeric
ts = pd.to_numeric(sjs_labs['TP'], errors='coerce')

# 4) Determine which patients have at least one normal TP value
sjs_labs = sjs_labs.assign(TP_num=ts)
normal_tp_patients = sjs_labs[(sjs_labs['TP_num'] >= LOW) & (sjs_labs['TP_num'] <= HIGH)]['ID'].dropna().drop_duplicates()

# 5) Count unique patients with normal TP
answer = len(normal_tp_patients)

target = pd.DataFrame({'count_sjs_patients_with_normal_tp': [answer]})

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
