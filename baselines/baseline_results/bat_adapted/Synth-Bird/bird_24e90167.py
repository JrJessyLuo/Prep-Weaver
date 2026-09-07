import pandas as pd
import numpy as np

def _prep_1(table_1):
    labs = table_1.loc[:, ['ID', 'Date', 'CRE']].copy()
    labs['Date'] = pd.to_datetime(labs['Date'], errors='coerce')
    labs['CRE'] = pd.to_numeric(labs['CRE'], errors='coerce')
    target = labs[['ID', 'Date', 'CRE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df_attr = table_1[table_1['ID'].eq('Attribute')].iloc[0]
    df_val = table_1[table_1['ID'].eq('Value')].iloc[0]
    attr_long = df_attr.drop(labels=['ID']).reset_index()
    attr_long.columns = ['patient_code','attribute']
    val_long = df_val.drop(labels=['ID']).reset_index()
    val_long.columns = ['patient_code','value']
    long = pd.merge(attr_long, val_long, on='patient_code', how='inner')
    target = long[long['attribute'].eq('Birthday')][['patient_code','value']].rename(columns={'value':'Birthday'}).drop_duplicates(subset=['patient_code']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
labs_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
demographics_prepared = prepared_table_2

# Assume labs_prepared and demographics_prepared are provided by BAT per the target schemas.

# 1) Integrate on patient identifier
labs_prepared['ID'] = labs_prepared['ID'].astype(str)
demographics_prepared['patient_code'] = demographics_prepared['patient_code'].astype(str)
merged = labs_prepared.merge(demographics_prepared, left_on='ID', right_on='patient_code', how='inner')

# 2) Parse dates and creatinine
merged['Date_parsed'] = pd.to_datetime(merged['Date'], errors='coerce')
# Birthday in demographics_prepared is a single date string per patient
merged['Birthday_parsed'] = pd.to_datetime(merged['Birthday'], errors='coerce')

# 3) Determine age-at-lab (in years)
# Use floor of year difference; if either date missing, result is NaN
def age_years(birth, when):
    if pd.isna(birth) or pd.isna(when):
        return pd.NA
    return (when.year - birth.year) - ((when.month, when.day) < (birth.month, birth.day))

merged['age'] = [age_years(b, d) for b, d in zip(merged['Birthday_parsed'], merged['Date_parsed'])]

# 4) Identify abnormal creatinine
# Without reference ranges by sex/age, use a generic flag: treat CRE as abnormal if outside [0.6, 1.3] mg/dL
# (Adjust if local lab ranges are known.)
cre = pd.to_numeric(merged['CRE'], errors='coerce')
merged['cre_abnormal'] = (cre < 0.6) | (cre > 1.3)

# 5) Among patients whose creatinine level is abnormal, count how many are not yet 70 at the time of the lab
subset = merged[merged['cre_abnormal'] & merged['age'].notna()]
count_not_70 = (subset['age'] < 70).sum()

answer = int(count_not_70)

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
