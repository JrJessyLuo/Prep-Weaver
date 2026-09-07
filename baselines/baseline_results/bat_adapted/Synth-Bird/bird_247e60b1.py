import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['ID','SEX','Diagnosis','combined_dates']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    labs = table_1.loc[:, ['ID', 'Date', 'HGB']].copy()
    labs['Date'] = pd.to_datetime(labs['Date'], errors='coerce')
    target = labs[['ID', 'Date', 'HGB']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
patients_dx = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs = prepared_table_2

# Assume prepared tables are provided as patients_dx and labs
# 1) Filter SLE patients
sle = patients_dx[patients_dx['Diagnosis'].str.upper().str.contains('SLE', na=False)].copy()

# 2) Determine normal hemoglobin threshold by sex
# Typical adult reference ranges (g/dL): Male 13.5-17.5, Female 12.0-15.5
# We'll classify normal if HGB is within these inclusive ranges.
labs_clean = labs.copy()
labs_clean = labs_clean[pd.to_numeric(labs_clean['HGB'], errors='coerce').notna()].copy()
labs_clean['HGB'] = pd.to_numeric(labs_clean['HGB'], errors='coerce')

# 3) Join SLE patients with labs
merged = sle.merge(labs_clean, on='ID', how='inner')

# 4) Compute sex-specific normal flag
sex_upper = merged['SEX'].str.upper()
normal_hgb = (
    ((sex_upper == 'M') & (merged['HGB'].between(13.5, 17.5, inclusive='both')))
    | ((sex_upper == 'F') & (merged['HGB'].between(12.0, 15.5, inclusive='both')))
)
merged = merged[normal_hgb].copy()

# 5) Derive age proxy to find oldest among these patients
# combined_dates appears like 'YYYY-MM-DD|...'; treat first token as birthdate if present
birth = merged['combined_dates'].fillna('').str.split('|').str[0]
merged['birth_date'] = pd.to_datetime(birth, errors='coerce')

# If multiple lab rows per patient, we just need the patient-level oldest; pick min birth_date (oldest) per ID
# Keep SEX for output
cand = merged[['ID', 'SEX', 'birth_date']].drop_duplicates()

# Prefer rows with valid birth_date; if none have valid birth_date, fall back to using earliest available Date as proxy for age ranking (older likely have earlier birth, but this is a weak proxy)
if cand['birth_date'].notna().any():
    # Oldest = smallest birth_date
    oldest_row = cand.sort_values(['birth_date', 'ID']).iloc[[0]]
else:
    # Fallback: parse lab Date and take the earliest-date patient (as a proxy); then pick arbitrarily if ties
    merged['lab_dt'] = pd.to_datetime(merged['Date'], errors='coerce')
    cand2 = merged[['ID', 'SEX', 'lab_dt']].dropna(subset=['lab_dt'])
    if not cand2.empty:
        oldest_row = cand2.sort_values(['lab_dt', 'ID']).iloc[[0]][['ID','SEX']]
    else:
        # If no dates at all, just pick the first by ID to return something deterministic
        oldest_row = merged[['ID','SEX']].drop_duplicates().sort_values('ID').iloc[[0]]

# Final answer: ID and SEX of the oldest SLE patient with normal HGB
answer = oldest_row[['ID', 'SEX']]

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
