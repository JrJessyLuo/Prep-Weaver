import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['Collection_Subset_ID','Collection_Subset_Name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['Collection_ID','Collection_Subset_ID']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[:, ['Document_Object_ID','Collection_ID']].drop_duplicates(subset=['Document_Object_ID','Collection_ID']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_subsets = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_collection_subsets = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_documents = prepared_table_3

tmp = prepared_collection_subsets.merge(prepared_documents, on='Collection_ID', how='left')
joined = tmp.merge(prepared_subsets, on='Collection_Subset_ID', how='right')
result = joined.groupby(['Collection_Subset_ID','Collection_Subset_Name'])['Document_Object_ID'].nunique().reset_index(name='num_distinct_documents')
result = result.sort_values(['Collection_Subset_ID'])
answer = result[['Collection_Subset_ID','Collection_Subset_Name','num_distinct_documents']]

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
