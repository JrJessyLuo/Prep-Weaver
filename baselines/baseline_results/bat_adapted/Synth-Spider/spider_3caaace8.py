import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['kehu_id','kehu_xinxi']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Customer_Interaction_ID','Customer_ID','Service_ID','xiangxi']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['Service_ID','Service_Type','Details']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['Customer_ID','Service_ID']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
customers = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
interactions = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
services = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
customer_services = prepared_table_4

# Assume prepared tables: customers, interactions, services, customer_services

# Filter to the target customer by name
cust = customers[customers['kehu_xinxi'] == 'Hardy Kutch']

# Services used by the customer via direct mapping
cust_used = (
    cust.merge(customer_services, left_on='kehu_id', right_on='Customer_ID', how='inner')
        .merge(services, on='Service_ID', how='inner')
        [['Service_ID','Service_Type','Details']]
        .drop_duplicates()
)

# Services from interactions that are rated as 'good'
inter_good = (
    interactions[interactions['xiangxi'].str.lower() == 'good']
        .merge(services, on='Service_ID', how='inner')
        [['Service_ID','Service_Type','Details']]
        .drop_duplicates()
)

# Union of both criteria
result = pd.concat([cust_used, inter_good], ignore_index=True).drop_duplicates().reset_index(drop=True)

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
