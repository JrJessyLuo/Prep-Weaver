import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['BUILDING_KEY','BUILDING_NUMBER','BUILDING_NAME','BUILDING_STREET_ADDRESS','BLDG_GROSS_SQUARE_FOOTAGE','BLDG_ASSIGNABLE_SQUARE_FOOTAGE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1.copy()
    prepared['BUILDING_NUMBER'] = prepared['BUILDING_NUMBER'].astype(str).str.strip()
    prepared['BUILDING_NUMBER'] = prepared['BUILDING_NUMBER'].replace({'nan': pd.NA, 'None': pd.NA, '': pd.NA})
    prepared['BUILDING_HEIGHT'] = pd.to_numeric(prepared['BUILDING_HEIGHT'], errors='coerce')
    prepared = prepared.dropna(subset=['BUILDING_NUMBER'])
    prepared = prepared[['BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_HEIGHT']]
    prepared = prepared.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first')
    target = prepared.reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['BUILDING_KEY','LEVEL_ID']].copy()
    prepared['LEVEL_ID'] = pd.to_numeric(prepared['LEVEL_ID'], errors='coerce')
    target = prepared.dropna(subset=['BUILDING_KEY','LEVEL_ID']).drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['BUILDING_KEY','ROOM_SQUARE_FOOTAGE']].copy()
    df['ROOM_SQUARE_FOOTAGE'] = pd.to_numeric(df['ROOM_SQUARE_FOOTAGE'], errors='coerce')
    target = df[['BUILDING_KEY','ROOM_SQUARE_FOOTAGE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_building_directory = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_building_characteristics = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prepared_floors = prepared_table_3
prepared_table_4 = _prep_4(tables['table_9'])
prepared_rooms = prepared_table_4

# Assume the following DataFrames exist from the per-table targets:
# prepared_building_directory, prepared_building_characteristics, prepared_floors, prepared_rooms

# 1) Merge directory with characteristics on BUILDING_NUMBER to get height
dir_char = prepared_building_directory.merge(
    prepared_building_characteristics[["BUILDING_NUMBER","BUILDING_HEIGHT"]],
    on="BUILDING_NUMBER",
    how="left"
)

# 2) Aggregate floors to get smallest and largest level per building
floors_agg = prepared_floors.groupby("BUILDING_KEY", as_index=False).agg(
    SMALLEST_LEVEL=("LEVEL_ID", "min"),
    LARGEST_LEVEL=("LEVEL_ID", "max")
)

# 3) Aggregate rooms to get total room area per building
rooms_agg = prepared_rooms.groupby("BUILDING_KEY", as_index=False).agg(
    TOTAL_ROOM_AREA=("ROOM_SQUARE_FOOTAGE", "sum")
)

# 4) Combine all by BUILDING_KEY
result = dir_char.merge(floors_agg, on="BUILDING_KEY", how="left") \
                 .merge(rooms_agg, on="BUILDING_KEY", how="left")

# 5) Select and rename columns for the final answer
final_columns = [
    "BUILDING_KEY",
    "BUILDING_NAME",
    "BUILDING_HEIGHT",
    "BUILDING_STREET_ADDRESS",
    # City, State, Postal Code are not present in provided schemas; keep placeholders if needed
    # If available in extended data, they should be included in prepared_building_directory
    "BLDG_GROSS_SQUARE_FOOTAGE",
    "BLDG_ASSIGNABLE_SQUARE_FOOTAGE",
    "SMALLEST_LEVEL",
    "LARGEST_LEVEL",
    "TOTAL_ROOM_AREA"
]

# Ensure presence of the columns even if some are missing due to upstream data
for c in final_columns:
    if c not in result.columns:
        result[c] = pd.NA

target = result[final_columns]

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
