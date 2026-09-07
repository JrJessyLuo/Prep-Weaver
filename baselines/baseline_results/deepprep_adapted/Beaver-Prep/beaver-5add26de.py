import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="BUILDING_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['BUILDING_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['BUILDING_KEY']
    if _dtype == "datetime64":
        table_1['BUILDING_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['BUILDING_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'MAJOR_USE_DESC', 'USE_DESC', 'ROOM', 'ROOM_FULL_NAME'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'MAJOR_USE_DESC', 'USE_DESC', 'ROOM', 'ROOM_FULL_NAME'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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
    # DropNulls(table_name="table_1", subset=['BUILDING_KEY'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['BUILDING_KEY'], how='any').reset_index(drop=True)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_KEY", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
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
    # StandardizeString(table_name="table_1", column_name="BUILDING_NUMBER", func="""
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        s = str(s).strip()
        return s.upper()
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
    # def transform_func(s):
    #     if s is None:
    #         return s
    #     # normalize internal whitespace, preserve original capitalization as much as possible
    #     s = " ".join(str(s).strip().split())
    #     return s
    # """)
    # StandardizeString
    def transform_func(s):
        if s is None:
            return s
        # normalize internal whitespace, preserve original capitalization as much as possible
        s = " ".join(str(s).strip().split())
        return s
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
    # SelectCol(table_name="table_1", columns=['BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NUMBER'])
    # SelectCol
    _cols = [c for c in ['BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NUMBER'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 6 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['BUILDING_KEY'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['BUILDING_KEY'], keep='first').reset_index(drop=True)

    # ---------------- Step 7 ----------------
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

prepared_table_1 = _prep_1(tables['table_9'])
prepared_rooms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
prepared_buildings = prepared_table_2

# Assume prepared_rooms and prepared_buildings are already synthesized from their respective sources
# Join rooms to buildings
rooms_bldg = prepared_rooms.merge(prepared_buildings, on='BUILDING_KEY', how='left')

# Heuristic: identify rooms that accommodate students. Adjust the keyword set as needed based on data dictionary.
# We consider MAJOR_USE_DESC/USE_DESC/ROOM_FULL_NAME text for hints like 'DORM', 'RESIDENCE', 'HOUSING', 'STUDENT', 'BED', 'ROOM', 'SUITE'.
text_cols = ['MAJOR_USE_DESC', 'USE_DESC', 'ROOM_FULL_NAME']
for c in text_cols:
    if c not in rooms_bldg.columns:
        rooms_bldg[c] = None

def contains_student_hint(s):
    if pd.isna(s):
        return False
    s = str(s).upper()
    hints = ['DORM', 'RESIDENCE', 'HOUS', 'STUDENT', 'BED', 'SUITE']
    return any(h in s for h in hints)

rooms_bldg['is_student_accom'] = rooms_bldg[text_cols].apply(lambda r: any(contains_student_hint(v) for v in r.values), axis=1)

# Count student-accommodating rooms per building as a proxy for capacity (actual bed counts not provided).
building_counts = (
    rooms_bldg[rooms_bldg['is_student_accom']]
    .groupby(['BUILDING_KEY', 'BUILDING_NAME'], dropna=False, as_index=False)
    .size()
    .rename(columns={'size': 'student_room_count'})
)

# Find building with maximum count
if not building_counts.empty:
    top = building_counts.sort_values(['student_room_count', 'BUILDING_NAME'], ascending=[False, True]).head(1)
    answer_building = top['BUILDING_NAME'].iloc[0]
    answer_count = int(top['student_room_count'].iloc[0])
else:
    answer_building = None
    answer_count = 0

result = {'building_name': answer_building, 'students_accommodated_proxy': answer_count}

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
