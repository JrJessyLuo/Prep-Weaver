import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'APTT']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce').dt.normalize()
    prepared['APTT'] = pd.to_numeric(prepared['APTT'], errors='coerce')
    target = prepared[['ID', 'Date', 'APTT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['ID','Examination Date','Thrombosis']].copy()
    df['Examination Date'] = pd.to_datetime(df['Examination Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    thr = df['Thrombosis'].astype('string').str.strip().str.replace('"','', regex=False).str.replace("'",'', regex=False).str.strip()
    thr = thr.replace({'1':1,'0':0,'yes':1,'no':0,'y':1,'n':0,'true':1,'false':0,'t':1,'f':0,'positive':1,'negative':0,'pos':1,'neg':0,'+':1,'-':0})
    df['Thrombosis'] = pd.to_numeric(thr, errors='coerce').astype('Int64')
    target = df[['ID','Examination Date','Thrombosis']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_lab_tests = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_clinical_outcomes = prepared_table_2

# Assume prepared_lab_tests and prepared_clinical_outcomes are already synthesized from table_1 and table_2 respectively.
# Normalize types
labs = prepared_lab_tests.copy()
clin = prepared_clinical_outcomes.copy()

# Coerce IDs to numeric where possible to align formats
labs['ID'] = pd.to_numeric(labs['ID'], errors='coerce')
clin['ID'] = pd.to_numeric(clin['ID'], errors='coerce')

# Merge on patient ID (visit-level dates are not consistently aligned across sources)
merged = labs.merge(clin[['ID', 'Thrombosis']], on='ID', how='inner')

# Define abnormal APTT: keep rows where APTT is a valid number and outside a typical normal range.
# Without provided reference ranges, treat any non-null APTT as measurable and abnormal if < 25 or > 35 seconds (adjust if domain metadata exists).
merged['APTT_num'] = pd.to_numeric(merged['APTT'], errors='coerce')
abnormal = merged[merged['APTT_num'].notna() & ((merged['APTT_num'] < 25) | (merged['APTT_num'] > 35))]

# Normalize thrombosis indicator: treat '"1"', '1', 1, True, 'yes' as positive; '"0"', '0', 0, False, 'no' as negative; ignore NaN/unknown.
thr = abnormal.copy()
val = thr['Thrombosis'].astype(str).str.strip().str.strip('"\'').str.lower()
thr['thrombosis_flag'] = val.isin(['1','true','yes','y'])
thrombosis_missing = val.isin(['nan','none','', 'na'])

# Count patients with abnormal APTT who do NOT have thrombosis (explicit negatives only)
no_thrombosis = thr[~thr['thrombosis_flag'] & ~thrombosis_missing]

# Count unique patients (not visits)
result = no_thrombosis['ID'].nunique()

target = pd.DataFrame({'count_patients_abnormal_aptt_without_thrombosis': [int(result)]})

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
