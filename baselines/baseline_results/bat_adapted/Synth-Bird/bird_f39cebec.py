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
    target = table_1[['id','power_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.groupby(['hero_id','attribute_id'], as_index=False).size().rename(columns={'size':'attribute_value'})
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['id','attribute_name']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
powers = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
hero_attributes = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
attribute_dictionary = prepared_table_4

# Assume prepared tables are provided as DataFrames: heroes, powers, hero_attributes, attribute_dictionary

# Join hero_attributes to heroes to get hero names
ha = hero_attributes.merge(heroes, left_on='hero_id', right_on='id', how='inner')

# Restrict attributes to those that are actual powers by joining to powers (ensures only power ids are counted)
ha_powers = ha.merge(powers, left_on='attribute_id', right_on='id', how='inner', suffixes=('', '_power'))

# Count distinct powers per hero (in case of duplicates)
power_counts = ha_powers.groupby(['hero_id', 'superhero_name'])['attribute_id'].nunique().reset_index(name='num_powers')

# Get the hero with the maximum number of powers
max_count = power_counts['num_powers'].max()
result = power_counts.loc[power_counts['num_powers'] == max_count].sort_values('superhero_name').head(1)

# Final answer: name of the superhero with the most powers
answer = result.iloc[0]['superhero_name']
answer

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
