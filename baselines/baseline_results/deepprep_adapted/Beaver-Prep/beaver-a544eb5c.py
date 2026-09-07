import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ASSIGNABLE_AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ASSIGNABLE_AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ASSIGNABLE_AREA']
    if _dtype == "datetime64":
        table_1['ASSIGNABLE_AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ASSIGNABLE_AREA'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NON_ASSIGNABLE_AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NON_ASSIGNABLE_AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NON_ASSIGNABLE_AREA']
    if _dtype == "datetime64":
        table_1['NON_ASSIGNABLE_AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NON_ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NON_ASSIGNABLE_AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NON_ASSIGNABLE_AREA'] = _series.astype(str)

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ASSIGNABLE_AREA', 'NON_ASSIGNABLE_AREA'] if c in table_1.columns]
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
    # SelectCol(table_name="table_1", columns=['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'NUM_OF_ROOMS'])
    # SelectCol
    _cols = [c for c in ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'NUM_OF_ROOMS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FAC_BUILDING_KEY", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FAC_BUILDING_KEY"] = table_1["FAC_BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME_LONG", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME_LONG"] = table_1["BUILDING_NAME_LONG"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="NUM_OF_ROOMS", mode="median")
    # MissingValueImputation
    table_1["NUM_OF_ROOMS"] = table_1["NUM_OF_ROOMS"].fillna(table_1["NUM_OF_ROOMS"].median())

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="NUM_OF_ROOMS", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['NUM_OF_ROOMS'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['NUM_OF_ROOMS']
    if _dtype == "datetime64":
        table_1['NUM_OF_ROOMS'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['NUM_OF_ROOMS'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['NUM_OF_ROOMS'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FAC_BUILDING_KEY', 'BUILDING_NUMBER'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FAC_BUILDING_KEY', 'BUILDING_NUMBER'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'NUM_OF_ROOMS'])
    # SelectCol
    _cols = [c for c in ['FAC_BUILDING_KEY', 'BUILDING_NUMBER', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'NUM_OF_ROOMS'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 10 ----------------
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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR_KEY", func="""def transform_func(s):
    #     return '' if s is None else str(s).strip()""")
    # StandardizeString
    def transform_func(s):
        return '' if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FLOOR_KEY"] = table_1["FLOOR_KEY"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""def transform_func(s):
    #     return '' if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        return '' if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_KEY"] = table_1["BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="FLOOR", func="""def transform_func(s):
    #     return '' if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        return '' if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["FLOOR"] = table_1["FLOOR"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ROOM", func="""def transform_func(s):
    #     return '' if s is None else str(s).strip()
    # """)
    # StandardizeString
    def transform_func(s):
        return '' if s is None else str(s).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ROOM"] = table_1["ROOM"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Filter(table_name="table_1", func="""def filter_func(row):
    #     return (row.get('BUILDING_KEY') not in [None, '', 'nan']) and            (row.get('FLOOR') not in [None, '', 'nan']) and            (row.get('FLOOR_KEY') not in [None, '', 'nan']) and            (row.get('ROOM') not in [None, '', 'nan'])
    # """)
    # Filter
    def filter_func(row):
        return (row.get('BUILDING_KEY') not in [None, '', 'nan']) and            (row.get('FLOOR') not in [None, '', 'nan']) and            (row.get('FLOOR_KEY') not in [None, '', 'nan']) and            (row.get('ROOM') not in [None, '', 'nan'])
    def _filter_apply(row):
        try:
            return bool(filter_func(row))
        except Exception:
            return False
    table_1 = table_1[table_1.apply(_filter_apply, axis=1)]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM'], keep='first').reset_index(drop=True)

    # ---------------- Step 7 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'FLOOR', 'FLOOR_KEY', 'ROOM'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 8 ----------------
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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_floors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_buildings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_rooms = prepared_table_3

# Assume prepared_floors, prepared_buildings, prepared_rooms are dataframes created from the respective table_targets

# 1) Aggregate floor areas per building
floor_agg = (
    prepared_floors
    .groupby('BUILDING_KEY', as_index=False)
    .agg(total_assignable_area=('ASSIGNABLE_AREA', 'sum'),
         total_non_assignable_area=('NON_ASSIGNABLE_AREA', 'sum'))
)

# 2) Integrate with buildings on BUILDING_KEY == FAC_BUILDING_KEY
merged = floor_agg.merge(
    prepared_buildings,
    left_on='BUILDING_KEY',
    right_on='FAC_BUILDING_KEY',
    how='left'
)

# 3) Prefer BUILDING_NAME if present, else BUILDING_NAME_LONG
merged['building_name'] = merged['BUILDING_NAME'].where(merged['BUILDING_NAME'].notna(), merged['BUILDING_NAME_LONG'])

# 4) Select and rename columns; NUM_OF_ROOMS is already per building
result = (
    merged
    .assign(total_room_count=merged['NUM_OF_ROOMS'])
    [[
        'building_name',
        'BUILDING_NUMBER',
        'total_assignable_area',
        'total_non_assignable_area',
        'total_room_count'
    ]]
    .sort_values('total_assignable_area', ascending=False)
)

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
