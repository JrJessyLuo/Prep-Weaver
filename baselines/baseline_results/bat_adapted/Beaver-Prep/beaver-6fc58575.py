import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['FCLT_ROOM_KEY','SPACE_ID','FCLT_BUILDING_KEY','FCLT_FLOOR_KEY','FLOOR','ROOM','ROOM_FULL_NAME','ORGANIZATION_NAME','DEPT_CODE','AREA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['FCLT_BUILDING_KEY','BUILDING_NAME','BUILDING_NAME_LONG','ASSIGNABLE_AREA']].copy()
    target = prepared[['FCLT_BUILDING_KEY','BUILDING_NAME','BUILDING_NAME_LONG','ASSIGNABLE_AREA']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['FCLT_FLOOR_KEY','FCLT_BUILDING_KEY','FLOOR','ASSIGNABLE_AREA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_10'])
prepared_floors = prepared_table_3

# Assume prepared_rooms, prepared_buildings, prepared_floors are pre-synthesized per targets above

# Ensure numeric types for area fields
for col in ["AREA"]:
    prepared_rooms[col] = pd.to_numeric(prepared_rooms[col], errors="coerce")
prepared_buildings["ASSIGNABLE_AREA"] = pd.to_numeric(prepared_buildings["ASSIGNABLE_AREA"], errors="coerce")
prepared_floors["ASSIGNABLE_AREA"] = pd.to_numeric(prepared_floors["ASSIGNABLE_AREA"], errors="coerce")

# Join rooms -> buildings
rb = prepared_rooms.merge(
    prepared_buildings[["FCLT_BUILDING_KEY", "BUILDING_NAME", "BUILDING_NAME_LONG", "ASSIGNABLE_AREA"]],
    on="FCLT_BUILDING_KEY",
    how="left",
    suffixes=("", "_BUILDING")
)

# Join rooms -> floors
rbf = rb.merge(
    prepared_floors[["FCLT_FLOOR_KEY", "ASSIGNABLE_AREA"]],
    on="FCLT_FLOOR_KEY",
    how="left",
    suffixes=("", "_FLOOR")
)

# Compute percentages
rbf["pct_of_floor"] = (rbf["AREA"] / rbf["ASSIGNABLE_AREA_FLOOR"]) * 100
rbf["pct_of_building"] = (rbf["AREA"] / rbf["ASSIGNABLE_AREA_BUILDING"]) * 100

# Prepare final fields
target = rbf[[
    "ROOM_FULL_NAME",
    "BUILDING_NAME",
    "BUILDING_NAME_LONG",
    "FLOOR",
    "ORGANIZATION_NAME",
    "DEPT_CODE",
    "AREA",
    "pct_of_floor",
    "pct_of_building",
    "SPACE_ID",
    "FCLT_BUILDING_KEY",
    "FCLT_FLOOR_KEY"
]].rename(columns={
    "FLOOR": "FLOOR_NUMBER",
    "BUILDING_NAME_LONG": "BUILDING_NAME_LONG_FORMAL"
})

# Note: Any sorting/filtering for presentation can be applied after 'target' is produced.

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
