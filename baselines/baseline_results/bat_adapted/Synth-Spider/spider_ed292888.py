import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['user_id','user_address_id','first_name','middle_name','last_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['property_id','property_address_id','owner_user_id','property_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['address_id','line_1_number_building','line_2_number_street','line_3_area_locality','town_city','zip_postcode','county_state_province','country']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_users = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_properties = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_addresses = prepared_table_3

owned = prepared_users.merge(prepared_properties, left_on='user_id', right_on='owner_user_id', how='inner')
residents = owned[owned['user_address_id'] == owned['property_address_id']]
# Optional: enrich with address details (not required to form names)
residents = residents.merge(prepared_addresses, left_on='user_address_id', right_on='address_id', how='left')
residents['full_name'] = residents[['first_name','middle_name','last_name']].fillna('').agg(' '.join, axis=1).str.replace('  +',' ', regex=True).str.strip()
answer = residents[['full_name']].drop_duplicates().sort_values('full_name')

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
