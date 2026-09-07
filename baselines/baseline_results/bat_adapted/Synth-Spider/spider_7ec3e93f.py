import pandas as pd
import numpy as np

def _prep_1(table_1):
    df_long = table_1.melt(id_vars=['student_address_id'], var_name='record_id', value_name='value')
    df_wide = df_long.pivot(index='record_id', columns='student_address_id', values='value').reset_index()
    target = df_wide[['student_id', 'address_type_code']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.copy()
    target['address_type_description'] = target['address_type_description'].astype(str).str.strip()
    target = target[['address_type_code','address_type_description']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_student_addresses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_address_types = prepared_table_2

# prepared_student_addresses construction from table_1 (pivot-like source)
# Assume df1 is table_1 with first column as row header names and remaining columns as student-specific values.
row_names = df1.iloc[:, 0]
value_cols = df1.columns[1:]
long = (
    df1.iloc[:, 1:]
      .copy()
      .assign(_row=row_names.values)
      .melt(id_vars=['_row'], var_name='col', value_name='val')
)
# Keep only rows where _row identifies the fields we need and val is non-null
student_ids = long[long['_row'].eq('student_id')][['col', 'val']].rename(columns={'val': 'student_id'})
addr_types = long[long['_row'].eq('address_type_code')][['col', 'val']].rename(columns={'val': 'address_type_code'})
prepared_student_addresses = (
    student_ids.merge(addr_types, on='col', how='inner')
               .drop(columns=['col'])
)

# prepared_address_types from table_2
prepared_address_types = df2.copy()
prepared_address_types['address_type_description'] = prepared_address_types['address_type_description'].astype(str).str.strip()

# Integrate to compute most common address type
joined = prepared_student_addresses.merge(
    prepared_address_types,
    on='address_type_code',
    how='left'
)
counts = joined.groupby(['address_type_code', 'address_type_description'], dropna=False).size().reset_index(name='n')
# Select the most common (break ties by code lexicographically for determinism)
answer = counts.sort_values(['n', 'address_type_code'], ascending=[False, True]).head(1)
# answer has columns: address_type_code, address_type_description, n

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
