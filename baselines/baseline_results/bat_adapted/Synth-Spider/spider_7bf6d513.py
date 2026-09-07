import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['pn','pln']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    melted = table_1.melt(id_vars=['plane_name'], var_name='plane_name', value_name='location')
    target = melted[['plane_name', 'location']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_pilot_planes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_plane_locations = prepared_table_2

# prepared_pilot_planes has columns: pn, pln
# prepared_plane_locations has columns: plane_name, location
merged = prepared_pilot_planes.merge(prepared_plane_locations, left_on='pln', right_on='plane_name', how='inner')
# Find pilots who have at least one plane located in Austin and at least one plane located in Boston
locs_by_pilot = merged.groupby('pn')['location'].apply(set).reset_index(name='locset')
eligible = locs_by_pilot[locs_by_pilot['locset'].apply(lambda s: 'Austin' in s and 'Boston' in s)]
answer = eligible['pn'].drop_duplicates().sort_values().tolist()

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
