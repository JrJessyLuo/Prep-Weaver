import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','superhero_name','eid','hid']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['id','attribute_name']].drop_duplicates(subset=['id','attribute_name']).dropna(subset=['id','attribute_name']).sort_values(['id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[:, ['hero_id','attribute_id','attribute_value']].dropna(subset=['hero_id','attribute_id','attribute_value']).astype({'hero_id':'int64','attribute_id':'int64','attribute_value':'int64'}).drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
attribute_lookup = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
hero_attributes = prepared_table_3

target = heroes.copy()
# Eye/hair color dimensions are not provided among selected tables; eid/hid are preserved to allow downstream join if those lookup tables are available.
# For now, select only the superhero names; final filtering by eye/hair requires joining eid/hid to their respective lookup tables (not selected).
answer = target[['superhero_name', 'eid', 'hid']]
# Downstream step (outside current scope) should join eid to eye_color_lookup(id->color_name) and hid to hair_color_lookup(id->color_name), then filter where eye_color == 'Blue' and hair_color == 'Blond' and project superhero_name.

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
