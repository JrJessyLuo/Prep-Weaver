import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','superhero_name','race_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['id','base_colour']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_superheroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_colours = prepared_table_2

# Assume prepared_superheroes and prepared_colours are produced from their respective source tables
# Ensure join key types align
prepared_superheroes = prepared_superheroes.copy()
prepared_colours = prepared_colours.copy()

# Coerce keys to numeric where possible (race_id is float-like strings in source; colours.id is int)
prepared_superheroes['race_id'] = pd.to_numeric(prepared_superheroes['race_id'], errors='coerce')
prepared_colours['id'] = pd.to_numeric(prepared_colours['id'], errors='coerce')

# Integrate on race/colour id
joined = prepared_superheroes.merge(prepared_colours, left_on='race_id', right_on='id', how='left')

# Filter superheroes with no skin colour (base_colour == 'No Colour')
no_colour = joined[joined['base_colour'].str.strip().str.lower() == 'no colour'.lower()]

# Compute the average (interpreting the question as the mean count per some unit is unclear;
# typically return the average number = mean of an indicator equals proportion). Here return the average value of the indicator of having no colour across all superheroes.
joined['has_no_colour'] = (joined['base_colour'].str.strip().str.lower() == 'no colour'.lower()).astype(float)
result = joined['has_no_colour'].mean()

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
