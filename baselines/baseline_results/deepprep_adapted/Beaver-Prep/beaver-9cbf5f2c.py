import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'new_name': 'BLDG_ASSIGNABLE_SF'}])
    # Rename
    table_1 = table_1.rename(columns={'BLDG_ASSIGNABLE_SQUARE_FOOTAGE': 'BLDG_ASSIGNABLE_SF'})

    # ---------------- Step 2 ----------------
    # Original operator:
    # Rename(table_name="table_1", rename_map=[{'old_name': 'BLDG_ASSIGNABLE_SF', 'new_name': 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE'}])
    # Rename
    table_1 = table_1.rename(columns={'BLDG_ASSIGNABLE_SF': 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE'})

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_KEY"] = table_1["BUILDING_KEY"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NUMBER"] = table_1["BUILDING_NUMBER"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_NAME", func="""
    # def transform_func(s):
    #     return s.strip() if isinstance(s, str) else s
    # """)
    # StandardizeString
    def transform_func(s):
        return s.strip() if isinstance(s, str) else s
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_NAME"] = table_1["BUILDING_NAME"].apply(_std_apply)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BLDG_GROSS_SQUARE_FOOTAGE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BLDG_GROSS_SQUARE_FOOTAGE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BLDG_GROSS_SQUARE_FOOTAGE']
    if _dtype == "datetime64":
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BLDG_GROSS_SQUARE_FOOTAGE'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BLDG_ASSIGNABLE_SQUARE_FOOTAGE", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE']
    if _dtype == "datetime64":
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BLDG_ASSIGNABLE_SQUARE_FOOTAGE'] = _series.astype(str)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY'], keep='last').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_NUMBER'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE', 'BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'BUILDING_NUMBER'] if c in table_1.columns]
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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # DropColumn(table_name="table_1", drop_columns=['SPACE_UNIT_CODE', 'ACCESS_LEVEL'])
    # DropColumn
    table_1 = table_1.drop(columns=['SPACE_UNIT_CODE', 'ACCESS_LEVEL'], errors='ignore')

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_ROOM", func="""
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
    table_1["BUILDING_ROOM"] = table_1["BUILDING_ROOM"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_COMPONENT", func="""
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
    table_1["BUILDING_COMPONENT"] = table_1["BUILDING_COMPONENT"].apply(_std_apply)

    # ---------------- Step 4 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="SPACE_USAGE", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return str(s).strip().upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return str(s).strip().upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["SPACE_USAGE"] = table_1["SPACE_USAGE"].apply(_std_apply)

    # ---------------- Step 5 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FLOOR", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FLOOR'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FLOOR']
    if _dtype == "datetime64":
        table_1['FLOOR'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FLOOR'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FLOOR'] = _series.astype(str)

    # ---------------- Step 6 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="HR_ORG_UNIT_ID", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['HR_ORG_UNIT_ID'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['HR_ORG_UNIT_ID']
    if _dtype == "datetime64":
        table_1['HR_ORG_UNIT_ID'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['HR_ORG_UNIT_ID'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['HR_ORG_UNIT_ID'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['HR_ORG_UNIT_ID'] = _series.astype(str)

    # ---------------- Step 7 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['BUILDING_COMPONENT', 'BUILDING_ROOM', 'HR_ORG_UNIT_ID', 'SPACE_USAGE', 'FLOOR'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_COMPONENT', 'BUILDING_ROOM', 'HR_ORG_UNIT_ID', 'SPACE_USAGE', 'FLOOR'], how='any').reset_index(drop=True)

    # ---------------- Step 8 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_COMPONENT', 'BUILDING_ROOM', 'FLOOR', 'HR_ORG_UNIT_ID', 'SPACE_USAGE'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_COMPONENT', 'BUILDING_ROOM', 'FLOOR', 'HR_ORG_UNIT_ID', 'SPACE_USAGE'], keep='first').reset_index(drop=True)

    # ---------------- Step 9 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_COMPONENT', 'BUILDING_ROOM', 'HR_ORG_UNIT_ID', 'SPACE_USAGE', 'FLOOR'])
    # SelectCol
    _cols = [c for c in ['BUILDING_COMPONENT', 'BUILDING_ROOM', 'HR_ORG_UNIT_ID', 'SPACE_USAGE', 'FLOOR'] if c in table_1.columns]
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
    # MissingValueImputation(table_name="table_1", column_name="HR_ORG_UNIT_TITLE", mode="mode")
    # MissingValueImputation
    table_1["HR_ORG_UNIT_TITLE"] = table_1["HR_ORG_UNIT_TITLE"].fillna(table_1["HR_ORG_UNIT_TITLE"].mode().iloc[0])

    # ---------------- Step 2 ----------------
    # Original operator:
    # MissingValueImputation(table_name="table_1", column_name="HR_DEPARTMENT_NAME", mode="mode")
    # MissingValueImputation
    table_1["HR_DEPARTMENT_NAME"] = table_1["HR_DEPARTMENT_NAME"].fillna(table_1["HR_DEPARTMENT_NAME"].mode().iloc[0])

    # ---------------- Step 3 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['HR_ORG_UNIT_ID', 'HR_ORG_UNIT_TITLE', 'HR_DEPARTMENT_NAME'])
    # SelectCol
    _cols = [c for c in ['HR_ORG_UNIT_ID', 'HR_ORG_UNIT_TITLE', 'HR_DEPARTMENT_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['HR_ORG_UNIT_ID'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['HR_ORG_UNIT_ID'], keep='last').reset_index(drop=True)

    # ---------------- Step 5 ----------------
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

prepared_table_1 = _prep_1(tables['table_1'])
prepared_buildings = prepared_table_1
prepared_table_2 = _prep_2(tables['table_10'])
prepared_rooms = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_hr_orgs = prepared_table_3

# Start from prepared tables
rooms_hr = prepared_rooms.merge(prepared_hr_orgs, on='HR_ORG_UNIT_ID', how='left')

# Join rooms to buildings by mapping building component/number
bldg_rooms = prepared_buildings.merge(rooms_hr, left_on='BUILDING_NUMBER', right_on='BUILDING_COMPONENT', how='left')

# Identify HR departments occupying each building (distinct names per building)
hr_names_per_building = (
    bldg_rooms.groupby('BUILDING_KEY')['HR_DEPARTMENT_NAME']
    .apply(lambda s: sorted(set([x for x in s.dropna() if str(x).strip() != ''])))
    .reset_index(name='HR_DEPARTMENTS')
)

# Aggregate assignable square footage metrics per building
sqft_agg = (
    prepared_buildings
    .groupby(['BUILDING_KEY', 'BUILDING_NAME', 'BLDG_GROSS_SQUARE_FOOTAGE'], as_index=False)
    .agg(total_assignable_sqft=('BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'sum'),
         avg_assignable_sqft=('BLDG_ASSIGNABLE_SQUARE_FOOTAGE', 'mean'))
)

# Combine HR department lists back to building aggregates
result = sqft_agg.merge(hr_names_per_building, on='BUILDING_KEY', how='left')

# Add built year if available (not present in provided schemas). If a built year column exists in buildings, select it in prepared_buildings and include it here.
if 'BUILT_YEAR' in prepared_buildings.columns:
    built_year = prepared_buildings[['BUILDING_KEY', 'BUILT_YEAR']].drop_duplicates()
    result = result.merge(built_year, on='BUILDING_KEY', how='left')
else:
    result['BUILT_YEAR'] = pd.NA

# Final projection per building key
target = result[['BUILDING_KEY', 'BUILDING_NAME', 'HR_DEPARTMENTS', 'BLDG_GROSS_SQUARE_FOOTAGE', 'total_assignable_sqft', 'avg_assignable_sqft', 'BUILT_YEAR']].sort_values('BUILDING_KEY')

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
