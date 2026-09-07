import pandas as pd
import numpy as np

def _prep_1(table_1):
    import pandas as pd
    df = table_1.copy()
    df['patient_id'] = df['patient_id'].astype(str).str.strip().str.strip('"').str.strip("'")
    df['ID'] = df['ID'].astype(str).str.strip()
    df['value'] = df['value'].astype(str).str.strip()
    df['ID_lc'] = df['ID'].str.lower()
    sex_mask = df['ID_lc'].str.contains(r'\bsex\b|\bgender\b', regex=True, na=False)
    sex_rows = df.loc[sex_mask, ['patient_id','value']].copy()
    sex_rows['sex'] = sex_rows['value'].replace({'-': pd.NA, '': pd.NA, 'nan': pd.NA, 'none': pd.NA, 'None': pd.NA})
    sex_rows['sex'] = sex_rows['sex'].astype('string').str.strip().str.lower()
    sex_rows['sex'] = sex_rows['sex'].replace({'m': 'Male', 'male': 'Male', 'man': 'Male', 'f': 'Female', 'female': 'Female', 'woman': 'Female'})
    sex_rows['sex'] = sex_rows['sex'].where(sex_rows['sex'].isin(['Male','Female']), pd.NA)
    sex_dedup = sex_rows.sort_values(['patient_id']).groupby('patient_id', as_index=False)['sex'].first()
    patients = df[['patient_id']].drop_duplicates()
    target = patients.merge(sex_dedup, on='patient_id', how='left')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    lab_results = table_1.loc[:, ['ID', 'Date', 'WBC', 'FG']].copy()
    lab_results['Date'] = pd.to_datetime(lab_results['Date'], errors='coerce')
    lab_results['WBC'] = pd.to_numeric(lab_results['WBC'], errors='coerce')
    lab_results['FG'] = pd.to_numeric(lab_results['FG'], errors='coerce')
    target = lab_results
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
patients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
lab_results = prepared_table_2

# Assume `patients` and `lab_results` are the prepared tables from BAT.
# 1) Standardize join keys
lab_results['ID'] = lab_results['ID'].astype(str).str.strip().str.replace('"','', regex=False)
patients['patient_id'] = patients['patient_id'].astype(str).str.strip().str.replace('"','', regex=False)

# 2) Keep only male patients
male_patients = patients[patients['sex'].str.upper().str.strip().isin(['M','MALE'])]

# 3) Join male patients to lab results
male_labs = male_patients.merge(lab_results, left_on='patient_id', right_on='ID', how='inner')

# 4) Define normal WBC range (adjust if domain knowledge specifies different)
# Common clinical adult normal WBC: 4.0 to 10.0 x10^3/µL
wbc_norm_low, wbc_norm_high = 4.0, 10.0

# 5) Determine per-patient whether they have any normal WBC measurement
wbc_ok = (
    male_labs.dropna(subset=['WBC'])
             .assign(wbc_normal=lambda df: (df['WBC'] >= wbc_norm_low) & (df['WBC'] <= wbc_norm_high))
             .groupby('patient_id', as_index=False)['wbc_normal'].max()
)

# 6) Determine per-patient whether they have any abnormal fibrinogen (FG) measurement
# Typical adult fibrinogen reference: 200–400 mg/dL (use if no dataset-specific range is provided)
fg_norm_low, fg_norm_high = 200.0, 400.0
fg_flag = (
    male_labs.dropna(subset=['FG'])
             .assign(fg_abnormal=lambda df: (df['FG'] < fg_norm_low) | (df['FG'] > fg_norm_high))
             .groupby('patient_id', as_index=False)['fg_abnormal'].max()
)

# 7) Patients who have a normal WBC (any time) and abnormal FG (any time)
per_patient = wbc_ok.merge(fg_flag, on='patient_id', how='inner')
answer_count = int(((per_patient['wbc_normal'] == True) & (per_patient['fg_abnormal'] == True)).sum())

result = answer_count

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
