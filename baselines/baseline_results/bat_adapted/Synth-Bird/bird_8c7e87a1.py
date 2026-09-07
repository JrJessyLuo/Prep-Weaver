import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','superhero_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['id','attribute_name']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.loc[:, ['hero_id','attribute_id','attribute_value']].drop_duplicates()
    target = target.groupby(['hero_id','attribute_id'], as_index=False).agg({'attribute_value':'max'})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_attributes = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_hero_attributes = prepared_table_3

# prepared_heroes, prepared_attributes, prepared_hero_attributes are provided by BAT after per-table preparation
# NOTE: The source tables provided do not contain an alignment/affiliation field. If a neutral alignment is encoded as an attribute,
# replace the placeholder filter below with the correct attribute_name/value check. Otherwise, this will yield an empty result.

# Example placeholder: suppose there is an attribute named 'Alignment' whose numeric value codes Neutral (e.g., 1=Good, 2=Neutral, 3=Evil)
# Set the expected neutral code here if applicable; if unknown, this filter will not match anything.
NEUTRAL_CODE = None  # replace with the correct code if known

merged = prepared_heroes.merge(prepared_hero_attributes, left_on='id', right_on='hero_id', how='left')\
                     .merge(prepared_attributes, left_on='attribute_id', right_on='id', how='left', suffixes=('_attrval','_attrdict'))

if NEUTRAL_CODE is not None:
    neutral_mask = (merged['attribute_name'] == 'Alignment') & (merged['attribute_value'] == NEUTRAL_CODE)
    target = merged.loc[neutral_mask, ['superhero_name']].drop_duplicates().sort_values('superhero_name')
else:
    # No alignment data available in the provided schemas; return empty result with the expected column
    target = pd.DataFrame(columns=['superhero_name'])

answer = target

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
