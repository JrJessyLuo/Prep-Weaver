import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1.loc[:, ['ID', 'Date']].copy()
    prepared['Date'] = pd.to_datetime(prepared['Date'], errors='coerce')
    target = prepared[['ID', 'Date']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared_exams = table_1.loc[:, ['ID', 'Examination Date']].copy()
    prepared_exams['Examination Date'] = pd.to_datetime(prepared_exams['Examination Date'], errors='coerce')
    target = prepared_exams
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_lab_tests = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_exams = prepared_table_2

# Assume prepared tables are provided as DataFrames: prepared_lab_tests, prepared_exams
# 1) Filter lab tests to October 1991
lab = prepared_lab_tests.copy()
lab['Date'] = pd.to_datetime(lab['Date'], errors='coerce')
lab_oct91 = lab[(lab['Date'].dt.year == 1991) & (lab['Date'].dt.month == 10)]

# 2) If multiple lab rows per patient in Oct 1991, pick the first date per patient (arbitrary but consistent)
lab_oct91_first = lab_oct91.sort_values('Date').groupby('ID', as_index=False).first()

# 3) We do not have birth dates in the selected tables; age as of 1999 cannot be computed from these tables alone.
# Return indication of missing required data (e.g., date of birth). If there were a demographics table with DOB,
# we would join on ID, compute age in 1999, and then average across patients identified in lab_oct91_first.

result = pd.DataFrame({
    'error': ['Missing required data to compute ages (e.g., Date of Birth). Add a demographics table with DOB joined on ID).']
})

target = result

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
