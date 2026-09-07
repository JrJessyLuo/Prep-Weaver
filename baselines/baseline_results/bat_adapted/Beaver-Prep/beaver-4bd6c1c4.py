import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['BUILDING_KEY','FLOOR']].copy()
    prepared = prepared.dropna(subset=['BUILDING_KEY','FLOOR'])
    prepared = prepared.drop_duplicates(subset=['BUILDING_KEY','FLOOR'])
    target = prepared[['BUILDING_KEY','FLOOR']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['BUILDING_KEY','BUILDING_NAME']].drop_duplicates(subset=['BUILDING_KEY']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_floors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2

# Assume prepared_floors and prepared_buildings are provided as per targets
# Count floors per building (ensure unique floors if duplicates exist)
floor_counts = (prepared_floors
                .dropna(subset=["BUILDING_KEY", "FLOOR"]) 
                .drop_duplicates(subset=["BUILDING_KEY", "FLOOR"]) 
                .groupby("BUILDING_KEY", as_index=False)["FLOOR"].count()
                .rename(columns={"FLOOR": "NUM_FLOORS"}))

# Join to building names
with_names = floor_counts.merge(prepared_buildings[["BUILDING_KEY", "BUILDING_NAME"]], on="BUILDING_KEY", how="left")

# Find max number of floors and filter
max_floors = with_names["NUM_FLOORS"].max()
result = with_names.loc[with_names["NUM_FLOORS"] == max_floors, ["BUILDING_NAME"]]

# Final output: list the names (ties included)
answer = result.sort_values(by=["BUILDING_NAME"]).reset_index(drop=True)

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
