import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df[['staff_id','conference_id']] = df['conference_staff'].astype(str).str.split('-', n=1, expand=True)
    df['staff_id'] = pd.to_numeric(df['staff_id'], errors='coerce').astype('Int64')
    df['conference_id'] = pd.to_numeric(df['conference_id'], errors='coerce').astype('Int64')
    target = df[['staff_id','conference_id','role']].dropna(subset=['staff_id','conference_id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df_long = table_1.melt(id_vars=['staff_ID'], var_name='staff_id', value_name='value')
    df_wide = df_long.pivot(index='staff_id', columns='staff_ID', values='value').reset_index()
    df_wide = df_wide.rename(columns={'Age': 'age', 'Nationality': 'nationality'})
    df_wide['staff_id'] = pd.to_numeric(df_wide['staff_id'], errors='coerce').astype('Int64')
    df_wide['name'] = df_wide['name'].astype(str)
    df_wide['age'] = df_wide['age'].astype(str)
    df_wide['nationality'] = df_wide['nationality'].astype(str)
    target = df_wide[['staff_id', 'name', 'age', 'nationality']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
prepared_staff_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_staff = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])

# prepared_staff_assignments has columns: staff_id(int), conference_id(int), role(str)
# prepared_staff has columns: staff_id(int), name(str), age(str/int), nationality(str)

merged = prepared_staff_assignments.merge(prepared_staff, on='staff_id', how='inner')

# Filter for Canadian staff
canadian = merged[merged['nationality'].str.strip().str.casefold() == 'canada']

# Get conference IDs with Canadian staff
conf_ids = canadian['conference_id'].dropna().astype(int).unique()

# If conference names are not available in the selected tables, return IDs as names surrogate
# Deduplicate and sort for deterministic output
result = pd.Series(conf_ids).sort_values().astype(str).tolist()

answer = result

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
