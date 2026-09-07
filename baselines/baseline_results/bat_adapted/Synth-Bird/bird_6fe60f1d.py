import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['ID'] = df['ID'].astype(str).str.strip().str.strip('"')
    target = df[['ID','Diagnosis','SEX','Birthday']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'PLT']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date', 'PLT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_patients = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_labs = prepared_table_2

target = prepared_patients.merge(prepared_labs, on='ID', how='inner')
# Filter to MCTD diagnosis (case-insensitive, allow variants)
mctd_mask = target['Diagnosis'].str.contains('MCTD', case=False, na=False)
ans = target[mctd_mask].copy()
# Define normal platelet range (e.g., 150-450 x10^9/L). Adjust if metadata provides reference intervals.
lower, upper = 150, 450
# Keep rows where PLT is numeric and within range
ans['PLT_numeric'] = pd.to_numeric(ans['PLT'], errors='coerce')
ans = ans[(ans['PLT_numeric'] >= lower) & (ans['PLT_numeric'] <= upper)]
# Select output columns (patient ID and platelet level, optionally date if needed for evidence)
answer = ans[['ID', 'Date', 'PLT_numeric']].rename(columns={'PLT_numeric': 'PLT'})

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
