import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['ID','Admission']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    labs = table_1.loc[:, ['ID', 'Date', 'RBC']].copy()
    labs['Date'] = pd.to_datetime(labs['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    target = labs[['ID', 'Date', 'RBC']]
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
# 1) Join patients with labs on patient ID
joined = labs.merge(patients, on='ID', how='inner')

# 2) Identify outpatient follow-up. Here, we assume Admission == '-' indicates outpatient clinic
outpatient = joined[joined['Admission'] == '-']

# 3) Determine abnormal RBC. Without reference ranges, use a generic adult threshold example or mark non-null extremes; here we flag RBC outside [3.8, 5.8] (x10^6/µL)
# If units differ, adjust outside this code.
abnormal = outpatient[(outpatient['RBC'].notna()) & ((outpatient['RBC'] < 3.8) | (outpatient['RBC'] > 5.8))]

# 4) List unique patient IDs meeting both conditions
answer = abnormal[['ID']].drop_duplicates().sort_values('ID').reset_index(drop=True)
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
