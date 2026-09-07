import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Collection_Subset_ID','Collection_Subset_Name']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    filtered = table_1.loc[table_1['subset_type'].eq('Collection_Subset_ID'), ['subset_id']]
    target = filtered.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_collection_subsets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_collection_subset_links = prepared_table_2

target = prepared_collection_subsets.merge(prepared_collection_subset_links, left_on='Collection_Subset_ID', right_on='subset_id', how='left'); result = target.groupby(['Collection_Subset_ID','Collection_Subset_Name'], dropna=False).size().reset_index(name='num_collections'); result = result[['Collection_Subset_ID','Collection_Subset_Name','num_collections']].sort_values(['Collection_Subset_ID'])

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
