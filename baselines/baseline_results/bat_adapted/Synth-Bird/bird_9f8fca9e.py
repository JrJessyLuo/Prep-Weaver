import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['ID','SEX','Birthday','FirstDate_Admission']].copy()
    df['Birthday'] = pd.to_datetime(df['Birthday'], errors='coerce').dt.strftime('%Y-%m-%d')
    df['FirstDate_Admission'] = df['FirstDate_Admission'].astype(str).str.split('|', n=1).str[0].replace({'NA': pd.NA, 'nan': pd.NA, 'None': pd.NA, '-': pd.NA, '': pd.NA})
    df['FirstDate_Admission'] = pd.to_datetime(df['FirstDate_Admission'], errors='coerce').dt.strftime('%Y-%m-%d')
    target = df[['ID','SEX','Birthday','FirstDate_Admission']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.loc[:, ['ID', 'Date', 'RBC']].copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['RBC'] = pd.to_numeric(df['RBC'], errors='coerce')
    target = df[['ID', 'Date', 'RBC']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
patients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs = prepared_table_2

# Assume prepared tables are provided as dataframes: patients, labs
# 1) Integrate on patient ID
merged = labs.merge(patients, on='ID', how='inner')

# 2) Compute age at lab date to assess age >= 50 at time of RBC measurement
# Parse dates
merged['lab_date'] = pd.to_datetime(merged['Date'], errors='coerce')
merged['birth_date'] = pd.to_datetime(merged['Birthday'], errors='coerce')

# Age in years at lab date
merged['age_years'] = ((merged['lab_date'] - merged['birth_date']).dt.days / 365.25)

# 3) Restrict to female and age >= 50
female50 = merged[(merged['SEX'].str.upper() == 'F') & (merged['age_years'] >= 50)]

# 4) Identify abnormal RBC.
# If lab reference ranges are unknown, flag outside a typical adult female reference range (approx): 3.8 to 5.2 x10^6/µL
# Adjust as needed if local reference is available elsewhere.
female50['RBC_val'] = pd.to_numeric(female50['RBC'], errors='coerce')
abnormal = female50[(female50['RBC_val'] < 3.8) | (female50['RBC_val'] > 5.2)]

# 5) For each patient, determine if they were admitted (any non-missing/non-'NA|-' FirstDate_Admission)
# Normalize admission indicator
def admitted_flag(v):
    if pd.isna(v):
        return False
    s = str(v).strip()
    return (s != '') and (s.lower() != 'na|-') and (s.lower() != 'na') and (s != '-')

abnormal['admitted'] = abnormal['FirstDate_Admission'].apply(admitted_flag)

# 6) Produce patient-level result (any abnormal RBC record qualifies)
result = (abnormal
          .sort_values(['ID','lab_date'])
          .groupby('ID', as_index=False)
          .agg({
              'SEX':'first',
              'birth_date':'first',
              'admitted':'max'  # any admission -> True
          }))

# 7) Final selected columns
target = result.rename(columns={'admitted':'admitted_to_hospital'})
# target columns: ID, SEX, birth_date, admitted_to_hospital

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
