import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_NUMBER'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_NUMBER'], keep='first').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME'], how='any').reset_index(drop=True)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['fac_room_key', 'FLOOR_KEY', 'SPACE_ID', 'MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'USE_KEY', 'USE_DESC', 'MINOR_USE_KEY', 'MINOR_USE_DESC', 'ORGANIZATION_KEY', 'MINOR_ORGANIZATION_KEY', 'MINOR_ORGANIZATION', 'AREA', 'ROOM_FULL_NAME', 'ACCESS_LEVEL', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'NORTHING_SPCS', 'EASTING_SPCS', 'WAREHOUSE_LOAD_DATE'])
    # DropColumn
    table_1 = table_1.drop(columns=['fac_room_key', 'FLOOR_KEY', 'SPACE_ID', 'MAJOR_USE_KEY', 'MAJOR_USE_DESC', 'USE_KEY', 'USE_DESC', 'MINOR_USE_KEY', 'MINOR_USE_DESC', 'ORGANIZATION_KEY', 'MINOR_ORGANIZATION_KEY', 'MINOR_ORGANIZATION', 'AREA', 'ROOM_FULL_NAME', 'ACCESS_LEVEL', 'LATITUDE_WGS', 'LONGITUDE_WGS', 'NORTHING_SPCS', 'EASTING_SPCS', 'WAREHOUSE_LOAD_DATE'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR', 'ROOM', 'ORGANIZATION_NAME', 'DEPT_CODE'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR', 'ROOM', 'ORGANIZATION_NAME', 'DEPT_CODE'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR', 'ROOM'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY', 'FLOOR', 'ROOM'], keep='first').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Terminate(result=['table_1'])
    # Terminate
    result = {'table_1': table_1}
    if 'result' in locals() and isinstance(result, dict) and result:
        for _v in result.values():
            if isinstance(_v, pd.DataFrame):
                return _v
    for _name in ('result_table', 'target', 'table_1'):
        if _name in locals() and isinstance(locals()[_name], pd.DataFrame):
            return locals()[_name]
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_5'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_rooms = prepared_table_2

# Merge buildings with rooms on BUILDING_KEY
merged = prepared_buildings.merge(prepared_rooms, on='BUILDING_KEY', how='left')

# Coerce floor to numeric when possible to compute min/max, keeping NaN for non-numeric
floors_num = pd.to_numeric(merged['FLOOR'], errors='coerce')
merged = merged.assign(_FLOOR_NUM=floors_num)

# Aggregate per building
agg = (
    merged.groupby(['BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NUMBER'], dropna=False)
          .agg(
              highest_floor=('._FLOOR_NUM'.strip('.'), 'max'),
              lowest_floor=('._FLOOR_NUM'.strip('.'), 'min'),
              total_rooms=('ROOM', lambda s: s.notna().sum()),
              organizations=('ORGANIZATION_NAME', lambda s: ', '.join(sorted({str(x) for x in s.dropna()})) if s.notna().any() else None),
              departments=('DEPT_CODE', lambda s: ', '.join(sorted({str(x) for x in s.dropna()})) if s.notna().any() else None)
          )
          .reset_index()
)

# Final selection/rename
target = agg.rename(columns={
    'BUILDING_KEY': 'building_key',
    'BUILDING_NAME': 'building_name',
    'BUILDING_NUMBER': 'building_number',
    'highest_floor': 'highest_floor_number',
    'lowest_floor': 'lowest_floor_number',
    'total_rooms': 'total_number_of_rooms',
    'organizations': 'organizations',
    'departments': 'department_names'
})

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
