import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['raceId','year']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['raceId','fastestLapSpeed']].copy()
    target['fastestLapSpeed'] = pd.to_numeric(target['fastestLapSpeed'], errors='coerce')
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_races = prepared_table_1
prepared_table_2 = _prep_2(tables['table_11'])
prepared_results = prepared_table_2

# Merge results with races on raceId to bring in year
merged = prepared_results.merge(prepared_races, on='raceId', how='inner')

# Coerce fastestLapSpeed to numeric, ignore non-numeric
merged['fastestLapSpeed'] = pd.to_numeric(merged['fastestLapSpeed'], errors='coerce')

# Compute the minimum fastest lap speed per year (lowest speed)
yearly_min = merged.dropna(subset=['fastestLapSpeed']).groupby('year', as_index=False)['fastestLapSpeed'].min()

# Identify the year with the overall lowest speed
answer_row = yearly_min.sort_values('fastestLapSpeed', ascending=True).head(1)

# Final answer: year with the lowest fastest lap speed
answer = int(answer_row.iloc[0]['year'])

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
