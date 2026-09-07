import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['ID', 'SEX', 'Birthday']].drop_duplicates(subset=['ID']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df[df['Date'].dt.year == 1994]
    target = df[['ID', 'Date', 'GOT']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
patients_prepared = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
labs_prepared = prepared_table_2

# Assume patients_prepared and labs_prepared are the synthesized per-table outputs

# 1) Integrate on patient ID
merged = patients_prepared.merge(labs_prepared, on='ID', how='inner')

# 2) Keep exams from calendar year 1994
merged['Date'] = pd.to_datetime(merged['Date'], errors='coerce')
merged_1994 = merged[merged['Date'].dt.year == 1994]

# 3) Determine normal range for GOT (AST). If the dataset has no explicit reference ranges,
#    use a common clinical reference range for AST (GOT): 10–40 U/L inclusive.
#    Adjust if local reference is known elsewhere.
merged_1994['GOT'] = pd.to_numeric(merged_1994['GOT'], errors='coerce')
normal = merged_1994[(merged_1994['GOT'] >= 10) & (merged_1994['GOT'] <= 40)]

# 4) List unique patients meeting the criterion with required fields
answer = normal[['ID', 'SEX', 'Birthday']].drop_duplicates().sort_values(['ID'])

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
