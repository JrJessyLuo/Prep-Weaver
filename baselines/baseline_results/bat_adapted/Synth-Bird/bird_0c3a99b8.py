import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'SM']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date', 'SM']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
    df['ID'] = df['ID'].astype('Int64')
    df['riqi'] = pd.to_datetime(df['riqi'], errors='coerce')
    df['Thrombosis'] = pd.to_numeric(df['Thrombosis'], errors='coerce').astype('Int64')
    target = df[['ID','riqi','Thrombosis']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_table_2 = _prep_2(tables['table_1'])

# Assume prepared_table_1 and prepared_table_2 are dataframes with the target schemas above.
# 1) Normalize ID types for joining
prepared_table_1 = prepared_table_1.copy()
prepared_table_2 = prepared_table_2.copy()
prepared_table_1['ID'] = pd.to_numeric(prepared_table_1['ID'], errors='coerce')
prepared_table_2['ID'] = pd.to_numeric(prepared_table_2['ID'], errors='coerce')

# 2) Define a helper to interpret normal anti-SM from SM values
# Treat normal as negative or not elevated; typical encodings observed: '-', '−', 'nan' (unknown), '+', '+-', etc.
# Here we consider normal anti-SM as explicit negative markers: values like '-', '−', 'neg', 'normal', '0', '0.0'.
# We will exclude missing/NaN from the normal cohort (cannot assert normal).

def is_normal_sm(val):
    if pd.isna(val):
        return False
    s = str(val).strip().lower()
    return s in {'-', '−', 'neg', 'negative', 'normal', '0', '0.0'}

normal_sm = prepared_table_1[prepared_table_1['SM'].apply(is_normal_sm)]

# 3) If multiple rows per patient exist, keep unique patient IDs in normal SM cohort
normal_patient_ids = normal_sm[['ID']].dropna().drop_duplicates()

# 4) Join to thrombosis table on ID to assess thrombosis status
joined = normal_patient_ids.merge(prepared_table_2[['ID', 'Thrombosis']], on='ID', how='left')

# 5) Determine patients without thrombosis. If multiple rows per patient in table_2, consider patient has thrombosis if any Thrombosis==1.
agg = joined.groupby('ID', as_index=False)['Thrombosis'].max(min_count=1)
# Thrombosis==1 means has thrombosis; 0 or NaN treated as no recorded thrombosis
no_thrombosis_patients = agg[(agg['Thrombosis'].isna()) | (agg['Thrombosis'] == 0)]

answer = len(no_thrombosis_patients)
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
