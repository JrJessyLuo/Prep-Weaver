import pandas as pd
import numpy as np

def _prep_1(table_1):
    labs = table_1.loc[:, ['ID', 'Date', 'IGG']].copy()
    labs['Date'] = pd.to_datetime(labs['Date'], errors='coerce')
    labs['IGG'] = pd.to_numeric(labs['IGG'], errors='coerce')
    target = labs[['ID', 'Date', 'IGG']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    patients = table_1[['ID','Admission']].copy()
    patients['Admission'] = patients['Admission'].replace({'-': pd.NA, '': pd.NA, 'nan': pd.NA})
    patients['ID'] = pd.to_numeric(patients['ID'], errors='coerce').astype('Int64')
    patients = patients.dropna(subset=['ID'])
    patients = patients.drop_duplicates(subset=['ID'], keep='first')
    target = patients[['ID','Admission']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
labs_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
patients_prepared = prepared_table_2

# Assume labs_prepared and patients_prepared are the synthesized per-table outputs
# 1) Integrate on patient ID
integrated = labs_prepared.merge(patients_prepared, on='ID', how='inner')

# 2) Define normal IGG range (domain-specific; adjust if metadata provides reference ranges)
# Placeholder example range for adults: 700–1600 mg/dL
lower, upper = 700.0, 1600.0

# 3) Cast IGG to numeric and filter to normal IGG rows
ig_numeric = pd.to_numeric(integrated['IGG'], errors='coerce')
normal_igg = integrated[(ig_numeric >= lower) & (ig_numeric <= upper)]

# 4) Determine admission indicator (assuming '-' or similar means not admitted; anything else like '+'/'Yes'/'Admitted' means admitted)
adm_col = normal_igg['Admission'].astype(str).str.strip().str.lower()
admitted_mask = adm_col.isin(['+', 'yes', 'y', 'admitted', 'inpatient', '1', 'true'])

# 5) Count unique patients with normal IGG who were admitted
result = admitted_mask.groupby(normal_igg['ID']).any().sum()

answer = int(result)

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
