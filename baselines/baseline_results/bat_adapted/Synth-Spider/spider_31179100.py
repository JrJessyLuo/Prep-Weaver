import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Driver_ID','First_Name','Last_Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    df = df.drop(columns=['Driver_ID'])
    df.columns = [f"{c}_{i}" for i, c in enumerate(df.columns)]
    long_df = df.melt(var_name='Driver_col', value_name='Vehicle_ID')
    long_df['Driver_ID'] = long_df['Driver_col'].astype(str).str.extract(r'^(\d+)')[0]
    long_df = long_df.drop(columns=['Driver_col'])
    long_df['Vehicle_ID'] = pd.to_numeric(long_df['Vehicle_ID'], errors='coerce')
    long_df['Driver_ID'] = pd.to_numeric(long_df['Driver_ID'], errors='coerce')
    long_df = long_df.dropna(subset=['Driver_ID','Vehicle_ID'])
    long_df['Driver_ID'] = long_df['Driver_ID'].astype(int)
    long_df['Vehicle_ID'] = long_df['Vehicle_ID'].astype(int)
    target = long_df[['Driver_ID','Vehicle_ID']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_drivers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_driver_vehicle_pairs = prepared_table_2

# prepared_drivers: columns [Driver_ID (int), First_Name, Last_Name]
# prepared_driver_vehicle_pairs: columns [Driver_ID (int), Vehicle_ID]

# Left-join drivers to driven pairs and find drivers with no matches
merged = prepared_drivers.merge(prepared_driver_vehicle_pairs, on='Driver_ID', how='left')
no_cars = merged[merged['Vehicle_ID'].isna()]
# Count unique drivers with no cars
answer = no_cars['Driver_ID'].nunique()

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
