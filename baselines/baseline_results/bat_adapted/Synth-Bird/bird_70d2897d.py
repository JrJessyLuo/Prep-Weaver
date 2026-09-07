import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'GPT']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date', 'GPT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['ID','Diagnosis']].copy()
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce').astype('Int64')
    df = df.dropna(subset=['ID'])
    df['Diagnosis'] = df['Diagnosis'].astype('string')
    df = df.sort_values(['ID'])
    target = df.groupby('ID', as_index=False)['Diagnosis'].agg(lambda s: s.dropna().iloc[0] if s.dropna().shape[0] > 0 else pd.NA)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_lab_results = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_patient_diagnosis = prepared_table_2

# Assume prepared_lab_results and prepared_patient_diagnosis are provided DataFrames
# 1) Clean types
labs = prepared_lab_results.copy()
# Coerce GPT to numeric
labs['GPT'] = pd.to_numeric(labs['GPT'], errors='coerce')
# Coerce Date to datetime (this is laboratory date; kept but not used for DOB ordering)
labs['Date'] = pd.to_datetime(labs['Date'], errors='coerce')
# Coerce ID to string for consistent joining
labs['ID'] = labs['ID'].astype(str)

pt = prepared_patient_diagnosis.copy()
pt['ID'] = pt['ID'].astype(str)

# 2) Determine ALT (GPT) normal range threshold. If not provided, a common adult upper limit is ~40 U/L.
ALT_ULN = 40.0

# 3) Filter lab results to ALT beyond normal range
labs_abnormal = labs[labs['GPT'] > ALT_ULN]

# 4) Integrate with diagnoses on ID
merged = labs_abnormal.merge(pt, on='ID', how='left')

# 5) If a separate date of birth column existed, we'd sort by it. Since only 'Date' exists and represents exam date, 
#    we proceed with that as the available chronological proxy. Replace 'Date_of_Birth' with actual DOB if available.
result = merged.sort_values(by=['Date'], ascending=True)[['ID', 'Diagnosis']].drop_duplicates()

# 6) The final output is the list of diagnoses (with patient IDs) for patients with ALT beyond normal range, ordered by ascending date.
answer = result

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
