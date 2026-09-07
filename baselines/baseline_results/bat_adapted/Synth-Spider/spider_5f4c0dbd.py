import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['PlanetID','Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['ShipmentID','Planet']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['Shipment','Weight']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_planets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_shipments = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_packages = prepared_table_3

tmp = prepared_packages.merge(prepared_shipments, left_on='Shipment', right_on='ShipmentID', how='inner')
res = tmp.merge(prepared_planets, left_on='Planet', right_on='PlanetID', how='inner')
answer = res.groupby('Name', as_index=False)['Weight'].sum().rename(columns={'Weight':'total_weight'})

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
