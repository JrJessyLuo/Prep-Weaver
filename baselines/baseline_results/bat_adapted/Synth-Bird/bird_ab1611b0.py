import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['driverId','fastestLapSpeed']].copy()
    prepared = prepared.dropna(subset=['fastestLapSpeed'])
    target = prepared.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['driverId','nationality']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_results = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_drivers = prepared_table_2

# Assume prepared_results and prepared_drivers are already synthesized from table_1 and table_2 respectively.
# Select the row with the maximum fastestLapSpeed, then get the driver's nationality.
merged = prepared_results.merge(prepared_drivers, on='driverId', how='inner')
# Drop rows without a valid fastestLapSpeed
merged_valid = merged.dropna(subset=['fastestLapSpeed'])
# Identify the driver with the global fastest lap speed
idx = merged_valid['fastestLapSpeed'].astype(float).idxmax()
answer_row = merged_valid.loc[idx]
answer = answer_row['nationality']

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
