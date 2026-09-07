import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['id','superhero_name','xb','yc','hc','sc']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[table_1['id'].eq('colour'), ['variable', 'colour']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
heroes = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
colour_lookup = prepared_table_2

# Assume prepared tables are provided as DataFrames: heroes, colour_lookup
# Join to decode eye colour code (hc)
merged = heroes.merge(colour_lookup, how='left', left_on='hc', right_on='variable')
# Filter for the requested hero name (case-insensitive match on exact name)
result = merged[merged['superhero_name'].str.lower() == 'blackwulf']
# Select the eye colour
answer = result[['superhero_name', 'colour']].rename(columns={'colour': 'eye_colour'})
# If multiple rows, keep unique
answer = answer.drop_duplicates()

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
