import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','superhero_name','full_name','height_cm','weight_kg']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['id','attribute_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['hero_id','attribute_id','attribute_value']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
attribute_lookup = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
hero_attributes = prepared_table_3

# Assume prepared tables: heroes, attribute_lookup, hero_attributes
# Filter by physical attributes to find the target hero(s)
matched = heroes[(heroes['height_cm'] == 188.0) & (heroes['weight_kg'] == 108.0)]

# If race is stored as an attribute, locate the attribute id/name for 'Race' or similar
# Join attributes to matched heroes and map attribute names
attrs = hero_attributes.merge(attribute_lookup, left_on='attribute_id', right_on='id', how='left')

# Filter to the matched hero ids and attribute_name indicating race
race_like = attrs[attrs['hero_id'].isin(matched['id'])]
# Common attribute names that can encode race
race_names = {'Race', 'race', 'Species', 'species'}
race_rows = race_like[race_like['attribute_name'].isin(race_names)]

# Prefer a single value; if multiple, return unique list
if not race_rows.empty:
    result = list(race_rows.sort_values(['hero_id','attribute_name'])['attribute_value'].unique())
else:
    # If race is actually a column in heroes (not shown), try to use it
    race_col = next((c for c in heroes.columns if c.lower() in ['race','species']), None)
    if race_col is not None and not matched.empty:
        result = list(matched[race_col].dropna().unique())
    else:
        result = []

answer = result

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
