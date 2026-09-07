import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['age'])
    # DropColumn
    table_1 = table_1.drop(columns=['age'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['pn', 'pln'])
    # SelectCol
    _cols = [c for c in ['pn', 'pln'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Stack(table_name="table_1", id_vars=[], value_vars=['B-1 Bomber', 'B-52 Bomber', 'F-14 Fighter', 'Piper Cub'], var_name="plane_name", value_name="location")
    # Stack
    table_1 = table_1.melt(id_vars=[], value_vars=['B-1 Bomber', 'B-52 Bomber', 'F-14 Fighter', 'Piper Cub'], var_name='plane_name', value_name='location')
    table_1 = table_1.dropna(subset=['location'])

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['plane_name', 'location'])
    # SelectCol
    _cols = [c for c in ['plane_name', 'location'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
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
