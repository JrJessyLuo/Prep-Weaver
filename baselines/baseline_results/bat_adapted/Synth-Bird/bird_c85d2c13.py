import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.loc[:, ['hero_id','attribute_id','attribute_value']].copy()
    target = target.astype({'hero_id':'int64','attribute_id':'int64','attribute_value':'int64'})
    target = target.dropna(subset=['hero_id','attribute_id','attribute_value'])
    target = target.drop_duplicates(subset=['hero_id','attribute_id'])
    target = target.sort_values(['hero_id','attribute_id']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['id','attribute_name']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_7'])
hero_attributes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
attribute_lookup = prepared_table_2

# Assume prepared tables are provided as dataframes: hero_attributes, attribute_lookup
# 1) Map attribute_id to attribute_name
attrs = hero_attributes.merge(attribute_lookup, left_on='attribute_id', right_on='id', how='left')

# 2) Identify heroes that have an attribute signaling 'vampire'. This step depends on the schema; 
# if an attribute named 'Species' or 'Race' or 'Type' exists and its attribute_value equals 'Vampire', filter accordingly.
# Try common candidates in order of preference.
candidate_attr_names = ['Species', 'Race', 'Type', 'Category', 'Alignment']
mask = pd.Series(False, index=attrs.index)
for name in candidate_attr_names:
    mask = mask | ((attrs['attribute_name'] == name) & (attrs['attribute_value'].astype(str).str.lower() == 'vampire'))

vamp_heroes = attrs.loc[mask, 'hero_id'].drop_duplicates()

# 3) Obtain full names for these heroes.
# NOTE: No hero-name table is provided among selected tables. If hero names are in another table
# (e.g., heroes with columns hero_id, full_name), fetch/prepare and join here.
# Placeholder to indicate missing dependency:
raise ValueError('Missing hero identity table with full names to answer the question. Join required on hero_id to a heroes table containing full_name.')

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
