import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','attribute_name']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['hero_id','attribute_id','attribute_value']].copy()
    target = target.dropna(subset=['hero_id','attribute_id','attribute_value'])
    target[['hero_id','attribute_id','attribute_value']] = target[['hero_id','attribute_id','attribute_value']].astype('int64')
    target = target.drop_duplicates(subset=['hero_id','attribute_id'], keep='first').reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['id','superhero_name','hair_colour_id','xb','yc']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_4'])
prepared_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_hero_attributes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_2'])
prepared_heroes = prepared_table_3

# Assume prepared tables are provided as DataFrames: prepared_heroes, prepared_attributes, prepared_hero_attributes
# For this question, hair and eye colours are not present in the given tables (no eye colour columns or lookup provided).
# Therefore, no cross-table integration can determine eye colour. If an eye colour lookup table (e.g., eye_colour_id) existed,
# we would join heroes to that table and filter for 'Black' on both hair and eye colour.

# Since only hair_colour_id is available, and no mapping to color names or eye color field is present,
# the result must be an empty set under current schema.

target = prepared_heroes.iloc[0:0][["superhero_name"]]

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
