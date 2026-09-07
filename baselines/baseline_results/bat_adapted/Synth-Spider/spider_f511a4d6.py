import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','name','nation_result']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['cyclist_id', 'bike_purchase_combined']].dropna(subset=['cyclist_id', 'bike_purchase_combined']).drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['id','product_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_cyclists = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_purchases = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_bikes = prepared_table_3

# prepared_cyclists: columns ['id','name','nation_result']
# prepared_purchases: columns ['cyclist_id','bike_purchase_combined'] where bike_purchase_combined like 'productId_year'
# prepared_bikes: columns ['id','product_name']

# Decompose purchase into product id to validate against bikes
pp = prepared_purchases.copy()
pp[['bike_id_str','year_str']] = pp['bike_purchase_combined'].str.split('_', n=1, expand=True)
pp['bike_id'] = pd.to_numeric(pp['bike_id_str'], errors='coerce')

# Validate bike_id exists in bike catalog (treat those as racing bikes)
pp_valid = pp.merge(prepared_bikes.rename(columns={'id':'bike_id'}), on='bike_id', how='inner')

# Find cyclists with no purchases (anti-join)
purchased_cyclist_ids = pp_valid['cyclist_id'].dropna().unique()
no_purchase = prepared_cyclists[~prepared_cyclists['id'].isin(purchased_cyclist_ids)].copy()

# Split nation and result from nation_result for output
no_purchase[['nation','result']] = no_purchase['nation_result'].str.split('|', n=1, expand=True)

answer = no_purchase[['name','nation','result']].reset_index(drop=True)

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
