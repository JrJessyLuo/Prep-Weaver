import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['owner_user_id','property_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['user_id','first_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_properties = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_users = prepared_table_2

props_per_owner = prepared_properties.groupby('owner_user_id', as_index=False).agg(property_count=('property_id','count'))
max_count = props_per_owner['property_count'].max()
top_owners = props_per_owner[props_per_owner['property_count'] == max_count]
joined = top_owners.merge(prepared_users, left_on='owner_user_id', right_on='user_id', how='left')
# If multiple owners tie, choose one deterministically (e.g., smallest user_id)
joined = joined.sort_values('user_id').head(1)
answer = joined['first_name'].iloc[0]

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
