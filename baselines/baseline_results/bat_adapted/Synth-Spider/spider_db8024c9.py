import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Building_ID','Address','Number_of_Stories']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Region_ID','Name_Part1','Name_Part2','Capital']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_regions = prepared_table_2

# prepared_buildings and prepared_regions are synthesized from table_1 and table_2 respectively as per table_targets.
# There is no explicit join key between buildings and regions in the provided schemas (no region field in buildings).
# Therefore, we cannot integrate across tables to associate buildings with the 'Abruzzo' region.
# If an address-to-region mapping were available, we would join on a region or locality field.

# As a placeholder, filter regions to 'Abruzzo' to demonstrate region selection logic.
regions = prepared_regions.copy()
regions['region_name'] = regions[['Name_Part1', 'Name_Part2']].apply(lambda x: ' '.join([p for p in x if p and str(p).lower() != 'none']).strip(), axis=1)
region_abruzzo = regions[regions['region_name'].str.lower() == 'abruzzo']

# Without a join path to buildings, we cannot return buildings-in-Abruzzo story counts.
# Expected logic if a join key existed (e.g., buildings['Region_ID']):
# target = prepared_buildings.merge(region_abruzzo[['Region_ID']], on='Region_ID', how='inner')[['Building_ID','Number_of_Stories']]
# For now, return an empty result with the intended schema.
target = prepared_buildings.iloc[0:0][['Building_ID', 'Number_of_Stories']]

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
