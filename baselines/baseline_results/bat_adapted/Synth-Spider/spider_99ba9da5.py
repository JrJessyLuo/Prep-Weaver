import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['Location','Capacity']].copy()
    df['capacity'] = pd.to_numeric(df['Capacity'], errors='coerce').astype('Int64')
    df['wh'] = pd.factorize(df['Location'])[0] + 1
    agg = df.groupby(['wh','Location'], as_index=False).agg({'capacity':'max'})
    target = agg[['wh','capacity']].astype({'wh':'int64','capacity':'int64'})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Code','wh']].copy()
    target['wh'] = target['wh'].astype('int64')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_warehouses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_inventory = prepared_table_2

tmp = prepared_inventory.merge(prepared_warehouses, on='wh', how='inner')
# Count items per warehouse
counts = tmp.groupby('wh', as_index=False).size().rename(columns={'size':'current_load'})
# Join back to capacities
with_cap = counts.merge(prepared_warehouses, on='wh', how='left')
# Select warehouses above capacity and return their item Codes
over = with_cap[with_cap['current_load'] > with_cap['capacity']]
result = tmp.merge(over[['wh']], on='wh', how='inner')[['Code']].drop_duplicates()
answer = result['Code'].tolist()

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
