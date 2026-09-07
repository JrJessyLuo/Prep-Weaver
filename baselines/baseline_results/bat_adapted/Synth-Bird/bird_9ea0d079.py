import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['patient_id'] = (df['prefix'].astype(str) + df['id_core'].astype(str) + df['suffix'].astype(str)).str.replace('"', '', regex=False)
    target = df[['patient_id', 'attr', 'val']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    labs = table_1.loc[:, ['ID', 'Date', 'UA']].copy()
    labs['Date'] = pd.to_datetime(labs['Date'], errors='coerce')
    target = labs[['ID', 'Date', 'UA']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
patients_long_attrs = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs = prepared_table_2

# Prepared inputs assumed: labs, patients_long_attrs
# 1) Normalize patients_long_attrs patient_id by removing surrounding quotes if any
pla = patients_long_attrs.copy()
pla['patient_id'] = pla['patient_id'].astype(str).str.replace('^\"|\"$', '', regex=True)

# 2) Extract a single sex value per patient from long attributes
# Common attribute names could be 'Sex', 'Gender', etc.; prefer Sex if multiple
sex_map = (pla[pla['attr'].str.lower().isin(['sex','gender'])]
             .assign(sex=lambda d: d['val'].astype(str).str.strip().str.lower()
                                   .map({'m':'male','male':'male','f':'female','female':'female'})
                                   .fillna(d['val'].astype(str)))
             [['patient_id','sex']]
             .dropna()
             .drop_duplicates(subset=['patient_id'], keep='first'))

# 3) Clean UA and determine abnormality
lb = labs.copy()
lb['UA'] = pd.to_numeric(lb['UA'], errors='coerce')
# Assume adult reference: males 3.4-7.0 mg/dL, females 2.4-6.0 mg/dL
# We'll first merge sex, then flag abnormal by sex-specific ranges
merged = lb.merge(sex_map, left_on='ID', right_on='patient_id', how='inner')

# Define sex-specific ranges
def ua_abnormal(row):
    ua = row['UA']
    if pd.isna(ua):
        return False
    sx = str(row.get('sex','')).lower()
    if sx == 'male':
        return (ua < 3.4) or (ua > 7.0)
    if sx == 'female':
        return (ua < 2.4) or (ua > 6.0)
    # If unknown sex, exclude from abnormal set for this question
    return False

merged['abnormal_ua'] = merged.apply(ua_abnormal, axis=1)

# 4) Restrict to abnormal UA rows
abn = merged[merged['abnormal_ua']]

# 5) Count unique patients by sex among abnormal UA
unique_patients = abn.dropna(subset=['sex']).drop_duplicates(subset=['patient_id'])
counts = unique_patients['sex'].str.lower().value_counts()
male_count = int(counts.get('male', 0))
female_count = int(counts.get('female', 0))

# 6) Compute ratio male:female as a string; handle zero division
ratio = f"{male_count}:{female_count}" if female_count != 0 else (f"{male_count}:0" if male_count>0 else "0:0")

answer = {
    'male_count': male_count,
    'female_count': female_count,
    'ratio_male_to_female': ratio
}

target = pd.Series(answer)

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
