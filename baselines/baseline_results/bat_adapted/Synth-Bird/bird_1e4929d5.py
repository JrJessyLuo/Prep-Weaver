import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['income_id','date_received','amount','source','link_to_member']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    long_df = table_1.melt(id_vars=['member_id'], var_name='member_record_id', value_name='value')
    wide_df = long_df.pivot(index='member_record_id', columns='member_id', values='value').reset_index()
    target = wide_df[['member_record_id', 'first_name', 'last_name']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_income = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_members = prepared_table_2

# prepared_income already selected columns
income = prepared_income.copy()
# Keep only dues-related rows for identifying who paid dues
income_dues = income[income['source'].str.lower() == 'dues'].copy()
# Coerce date for ordering
income_dues['date_received'] = pd.to_datetime(income_dues['date_received'], errors='coerce')

# prepared_members is in long/narrow form with columns: member_record_id, first_name, last_name
members = prepared_members.copy()

# Join dues receipts to member names
df = income_dues.merge(members, left_on='link_to_member', right_on='member_record_id', how='left')

# Find the earliest dues payment
df_sorted = df.sort_values(['date_received', 'income_id'], ascending=[True, True])
first_row = df_sorted.iloc[0]

# Compose full name
target = first_row['first_name'] + ' ' + first_row['last_name']

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
