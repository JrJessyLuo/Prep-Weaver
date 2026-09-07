import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','FLOOR','FLOOR_SORT_SEQUENCE']].copy()
    prepared = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY','FLOOR','FLOOR_SORT_SEQUENCE'])
    target = prepared[['FCLT_BUILDING_KEY','FLOOR','FLOOR_SORT_SEQUENCE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','BUILDING_NAME']].copy()
    prepared = prepared.dropna(subset=['FCLT_BUILDING_KEY'])
    prepared['FCLT_BUILDING_KEY'] = prepared['FCLT_BUILDING_KEY'].astype(str)
    prepared = prepared.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='first')
    target = prepared[['FCLT_BUILDING_KEY','BUILDING_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_floors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_buildings = prepared_table_2

# prepared_floors and prepared_buildings are the synthesized per-table outputs
# Convert FLOOR_SORT_SEQUENCE to numeric if needed
pf = prepared_floors.copy()
pf['FLOOR_SORT_SEQUENCE'] = pd.to_numeric(pf['FLOOR_SORT_SEQUENCE'], errors='coerce')

# For each building, find the maximum floor number (by sort sequence). Keep the corresponding FLOOR label.
idx = pf.groupby('FCLT_BUILDING_KEY')['FLOOR_SORT_SEQUENCE'].idxmax()
max_floor_per_bldg = pf.loc[idx, ['FCLT_BUILDING_KEY', 'FLOOR', 'FLOOR_SORT_SEQUENCE']]

# Join to building names
result = max_floor_per_bldg.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left')

# Select the building with the overall largest floor number
max_seq = result['FLOOR_SORT_SEQUENCE'].max()
final = result[result['FLOOR_SORT_SEQUENCE'] == max_seq][['BUILDING_NAME', 'FLOOR']]

# If multiple tie, list them all
answer = final.rename(columns={'BUILDING_NAME': 'name', 'FLOOR': 'floor'})

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
