import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['pilot','age']].drop_duplicates()
    df = df.sort_values(['pilot','age']).reset_index(drop=True)
    df['hangar_location'] = pd.NA
    target = df[['pilot','age','hangar_location']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
pilots = prepared_table_1

# Assume prepared table 'pilots' includes columns: pilot, age, hangar_location
# Group by hangar location to compute pilot counts and average ages
result = pilots.groupby('hangar_location', dropna=False).agg(
    pilots_count=('pilot', pd.Series.nunique),
    average_age=('age', 'mean')
).reset_index().sort_values('hangar_location')

target = result

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
