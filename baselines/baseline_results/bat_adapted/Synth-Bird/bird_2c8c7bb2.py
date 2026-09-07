import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['ID','xb']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.loc[:, ['ID', 'Date', 'HGB']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date', 'HGB']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_demographics = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_labs = prepared_table_2

target = prepared_demographics.merge(prepared_labs, on='ID', how='inner')
# Define a generic low hemoglobin threshold if not otherwise specified; thresholds can be sex-specific if desired.
# Example using a common clinical cutoff: HGB < 12.0 g/dL
low_hgb = target[target['HGB'].astype(float) < 12.0]
# Select unique outpatients with low HGB and their sex; keep Date as optional evidence if needed per occurrence.
answer = low_hgb[['ID', 'xb']].drop_duplicates().rename(columns={'xb': 'Sex'})

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
