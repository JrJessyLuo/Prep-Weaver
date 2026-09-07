import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['driverId', 'statusId']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1.copy()
    parts = df['status_combined'].astype(str).str.split('-', n=1, expand=True)
    df['statusId'] = pd.to_numeric(parts[0], errors='coerce').astype('Int64')
    df['status'] = parts[1].astype(str).str.strip()
    target = df[['statusId', 'status']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df_long = table_1.melt(id_vars=['driverId'], var_name='driverId_melt', value_name='value')
    df_nat = df_long[df_long['driverId'].astype(str).str.lower().eq('nationality')].copy()
    df_nat['driverId_melt'] = df_nat['driverId_melt'].astype(str)
    target = df_nat.rename(columns={'driverId_melt': 'driverId', 'value': 'nationality'})[['driverId', 'nationality']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_results = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_status_lookup = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_drivers = prepared_table_3

# prepared_results has columns: driverId (int or str), statusId (int)
# prepared_status_lookup has columns: statusId (int), status (str)
# prepared_drivers has columns: driverId (int or str), nationality (str)

# Ensure compatible dtypes for joins
prepared_results['driverId'] = prepared_results['driverId'].astype(str)
prepared_drivers['driverId'] = prepared_drivers['driverId'].astype(str)
prepared_results['statusId'] = pd.to_numeric(prepared_results['statusId'], errors='coerce')
prepared_status_lookup['statusId'] = pd.to_numeric(prepared_status_lookup['statusId'], errors='coerce')

# Join results with status labels
res_status = prepared_results.merge(prepared_status_lookup, on='statusId', how='left')

# Join with drivers to get nationality
res_full = res_status.merge(prepared_drivers, on='driverId', how='left')

# Count how many American drivers have puncture status
# Match status text case-insensitively and allowing variants like 'Puncture'
mask_puncture = res_full['status'].fillna('').str.contains('puncture', case=True, regex=True)
mask_american = res_full['nationality'].fillna('').str.lower().eq('american')

answer = int(res_full.loc[mask_puncture & mask_american, 'driverId'].nunique())

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
