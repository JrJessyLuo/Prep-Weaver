import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Region_ID','Building_ID']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Region_ID','Name_Part1','Name_Part2']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_regions = prepared_table_2

regions = prepared_regions.copy()
regions['Region_Name'] = regions[['Name_Part1','Name_Part2']].apply(lambda r: r['Name_Part1'] if (pd.isna(r['Name_Part2']) or str(r['Name_Part2']).lower()=='none' or str(r['Name_Part2']).strip()=='') else f"{r['Name_Part1']} {r['Name_Part2']}", axis=1)
joined = regions.merge(prepared_buildings[['Region_ID','Building_ID']].drop_duplicates(), on='Region_ID', how='left')
no_building_regions = joined[joined['Building_ID'].isna()]
answer = no_building_regions['Region_Name'].dropna().drop_duplicates().sort_values().tolist()

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
