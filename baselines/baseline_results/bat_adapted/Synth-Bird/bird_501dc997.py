import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['id', 'superhero_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['hero_id','attribute_id','attribute_value']].copy()
    target['hero_id'] = pd.to_numeric(target['hero_id'], errors='coerce').astype('Int64')
    target['attribute_id'] = pd.to_numeric(target['attribute_id'], errors='coerce').astype('Int64')
    target['attribute_value'] = target['attribute_value'].astype('string')
    target = target.dropna(subset=['hero_id','attribute_id']).astype({'hero_id':'int64','attribute_id':'int64'})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['id','attribute_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
hero_attributes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
attribute_names = prepared_table_3

target = heroes.merge(hero_attributes, left_on='id', right_on='hero_id', how='inner').merge(attribute_names, left_on='attribute_id', right_on='id', how='inner')
result = target[target['superhero_name'] == 'Abomination'][['attribute_name','attribute_value']].sort_values('attribute_name')

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
