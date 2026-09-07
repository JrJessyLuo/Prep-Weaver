import pandas as pd
import numpy as np

def _prep_1(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="UNIT", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     return " ".join(str(s).split()).strip()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        return " ".join(str(s).split()).strip()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["UNIT"] = table_1["UNIT"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeDatetime(table_name="table_1", column_name="DATE_FROM", date_format="%Y-%m-%d")
    # StandardizeDatetime
    def _sd_parse(x):
        if pd.isna(x):
            return pd.NaT
        try:
            if isinstance(x, str):
                return _date_parse(x, fuzzy=True)
            return pd.to_datetime(x, errors='coerce')
        except Exception:
            return pd.NaT
    table_1['DATE_FROM'] = table_1['DATE_FROM'].apply(_sd_parse)
    if '%Y-%m-%d':
        table_1['DATE_FROM'] = table_1['DATE_FROM'].dt.strftime('%Y-%m-%d')

    # ---------------- Step 3 ----------------
    # Original operator:
    # DropNulls(table_name="table_1", subset=['COURSE_NAME', 'DATE_FROM', 'UNIT_CODE', 'UNIT'], how="any")
    # DropNulls
    table_1 = table_1.dropna(subset=['COURSE_NAME', 'DATE_FROM', 'UNIT_CODE', 'UNIT'], how='any').reset_index(drop=True)

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['COURSE_NAME', 'DATE_FROM', 'UNIT_CODE', 'UNIT'], keep="first")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['COURSE_NAME', 'DATE_FROM', 'UNIT_CODE', 'UNIT'], keep='first').reset_index(drop=True)

    # ---------------- Step 5 ----------------
    # Original operator:
    # Sort(table_name="table_1", by=['DATE_FROM', 'COURSE_NAME'], ascending=[True, True])
    # Sort
    table_1 = table_1.sort_values(by=['DATE_FROM', 'COURSE_NAME'], ascending=[True, True])

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['COURSE_NAME', 'DATE_FROM', 'UNIT_CODE', 'UNIT'])
    # SelectCol
    _cols = [c for c in ['COURSE_NAME', 'DATE_FROM', 'UNIT_CODE', 'UNIT'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_2(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="BUILDING_ROOM", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     s = str(s).strip()
    #     s = ' '.join(s.split())
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        s = str(s).strip()
        s = ' '.join(s.split())
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["BUILDING_ROOM"] = table_1["BUILDING_ROOM"].apply(_std_apply)

    # ---------------- Step 2 ----------------
    # Original operator:
    # StandardizeString(table_name="table_1", column_name="ROOM_FULL_NAME", func="""
    # def transform_func(s: str):
    #     if s is None:
    #         return s
    #     # Treat common missing tokens as null
    #     if str(s).strip().lower() in ["nan", "none", "null", ""]:
    #         return None
    #     s = str(s).strip()
    #     s = ' '.join(s.split())
    #     return s.upper()
    # """)
    # StandardizeString
    def transform_func(s: str):
        if s is None:
            return s
        # Treat common missing tokens as null
        if str(s).strip().lower() in ["nan", "none", "null", ""]:
            return None
        s = str(s).strip()
        s = ' '.join(s.split())
        return s.upper()
    def _std_apply(s):
        if pd.isna(s):
            return s
        try:
            return transform_func(s)
        except Exception:
            return s
    table_1["ROOM_FULL_NAME"] = table_1["ROOM_FULL_NAME"].apply(_std_apply)

    # ---------------- Step 3 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="AREA", dtype="float")
    # CastType
    _dtype = 'float'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['AREA'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['AREA']
    if _dtype == "datetime64":
        table_1['AREA'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['AREA'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['AREA'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['AREA'] = _series.astype(str)

    # ---------------- Step 4 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="ACCESS_LEVEL", dtype="int")
    # CastType
    _dtype = 'int'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['ACCESS_LEVEL'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['ACCESS_LEVEL']
    if _dtype == "datetime64":
        table_1['ACCESS_LEVEL'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['ACCESS_LEVEL'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['ACCESS_LEVEL'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['ACCESS_LEVEL'] = _series.astype(str)

    # ---------------- Step 5 ----------------
    # Original operator:
    # AddNewColumn(table_name="table_1", new_column_name="ROOM_FULL_NAME", func="""
    # import pandas as pd
    # def compute(row: pd.Series):
    #     v = row.get('ROOM_FULL_NAME', None)
    #     # If missing, fall back to BUILDING_ROOM for a usable room identifier
    #     if v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip().lower() in ['nan', 'none', 'null', '']:
    #         return row.get('BUILDING_ROOM', None)
    #     return v
    # """)
    # AddNewColumn
    def compute(row: pd.Series):
        v = row.get('ROOM_FULL_NAME', None)
        # If missing, fall back to BUILDING_ROOM for a usable room identifier
        if v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip().lower() in ['nan', 'none', 'null', '']:
            return row.get('BUILDING_ROOM', None)
        return v
    def _anc_apply(row):
        try:
            return compute(row)
        except Exception:
            return None
    table_1["ROOM_FULL_NAME"] = table_1.apply(_anc_apply, axis=1)

    # ---------------- Step 6 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'ROOM_FULL_NAME', 'AREA', 'ACCESS_LEVEL'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_ROOM', 'ROOM_FULL_NAME', 'AREA', 'ACCESS_LEVEL'] if c in table_1.columns]
    table_1 = table_1[_cols]

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
def _prep_3(table_1):
    input_tables = {'table_1': table_1}
    table_1 = input_tables['table_1'].copy()


    # ---------------- Step 1 ----------------
    # Original operator:
    # CastType(table_name="table_1", column="FCLT_BUILDING_KEY", dtype="string")
    # CastType
    _dtype = 'string'
    if _dtype.startswith("int") or _dtype.startswith("float"):
        _series = table_1['FCLT_BUILDING_KEY'].apply(lambda x: str(x).strip('"').strip("'"))
    else:
        _series = table_1['FCLT_BUILDING_KEY']
    if _dtype == "datetime64":
        table_1['FCLT_BUILDING_KEY'] = pd.to_datetime(_series, errors="coerce")
    elif _dtype.startswith("int"):
        table_1['FCLT_BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").fillna(0).astype(int)
    elif _dtype.startswith("float"):
        table_1['FCLT_BUILDING_KEY'] = pd.to_numeric(_series, errors="coerce").astype(float)
    else:
        table_1['FCLT_BUILDING_KEY'] = _series.astype(str)

    # ---------------- Step 2 ----------------
    # Original operator:
    # SelectCol(table_name="table_1", columns=['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ACCESS_LEVEL_CODE', 'ASSIGNABLE_AREA'])
    # SelectCol
    _cols = [c for c in ['FCLT_BUILDING_KEY', 'BUILDING_NAME', 'BUILDING_NAME_LONG', 'ACCESS_LEVEL_CODE', 'ASSIGNABLE_AREA'] if c in table_1.columns]
    table_1 = table_1[_cols]

    # ---------------- Step 3 ----------------
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

    # ---------------- Step 4 ----------------
    # Original operator:
    # Deduplicate(table_name="table_1", subset=['FCLT_BUILDING_KEY'], keep="last")
    # Deduplicate
    table_1 = table_1.drop_duplicates(subset=['FCLT_BUILDING_KEY'], keep='last').reset_index(drop=True)

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

prepared_table_1 = _prep_1(tables['table_2'])
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_rooms = prepared_table_2
prepared_table_3 = _prep_3(tables['table_9'])
prepared_buildings = prepared_table_3

# Assume prepared tables already loaded as dataframes: prepared_courses, prepared_rooms, prepared_buildings

# Join rooms to buildings to get building names and confirm/access levels
rooms_with_bldg = prepared_rooms.merge(prepared_buildings, on='FCLT_BUILDING_KEY', how='left', suffixes=('', '_BLDG'))

# Heuristic link from course location to building:
# Map common library/unit names to building numbers/keys when possible.
# Example mapping (extend as needed based on data dictionary):
unit_to_building_key = {
    'Barker': '10',    # example building number for Barker (placeholder; adjust if known)
    'Hayden': '14',    # example placeholder
    'Dewey': 'E53'     # example placeholder
}

# Derive candidate building key for each course from UNIT/UNIT_CODE text
courses_enriched = prepared_courses.copy()
courses_enriched['candidate_bldg_key'] = courses_enriched['UNIT'].map(unit_to_building_key).fillna(courses_enriched['UNIT_CODE'])

# Join courses to building-level info via candidate building key
courses_with_bldg = courses_enriched.merge(prepared_buildings, left_on='candidate_bldg_key', right_on='FCLT_BUILDING_KEY', how='left', suffixes=('', '_BLDG'))

# Optionally, if room-level detail is needed for area, try to select a representative room in that building whose ROOM_FULL_NAME or BUILDING_ROOM matches UNIT when available; else fall back to building assignable area
# Attempt text match between UNIT and ROOM_FULL_NAME or BUILDING_ROOM
rooms_with_bldg['UNIT_MATCH'] = rooms_with_bldg['ROOM_FULL_NAME'].fillna('').str.contains('|'.join(pd.Series(courses_enriched['UNIT'].dropna().unique()).astype(str).str.replace(r'[\\^$.*+?{}\[\]\\|()\-]', '.', regex=True)), case=False, regex=True)

# Build a per-building aggregate for room-level fields we need (e.g., choose max AREA as a proxy when exact room not known)
room_agg = rooms_with_bldg.groupby('FCLT_BUILDING_KEY', as_index=False).agg({
    'ACCESS_LEVEL': 'max',
    'AREA': 'max'  # proxy for assignable area of a used room if exact room unknown
})

# Merge aggregates to courses via candidate building key
courses_final = courses_with_bldg.merge(room_agg, left_on='candidate_bldg_key', right_on='FCLT_BUILDING_KEY', how='left', suffixes=('', '_ROOMAGG'))

# Prepare columns for sequencing previous/next course names by date then course name
courses_final['DATE_SORT'] = pd.to_datetime(courses_final['DATE_FROM'], errors='coerce')

# Sort and compute previous/next course within the entire set (as question requests sequencing by start date then course name, not grouped)
courses_final = courses_final.sort_values(['DATE_SORT', 'COURSE_NAME'], kind='mergesort')
courses_final['PREV_COURSE_NAME'] = courses_final['COURSE_NAME'].shift(1)
courses_final['NEXT_COURSE_NAME'] = courses_final['COURSE_NAME'].shift(-1)

# Select output columns
result = courses_final[[
    'COURSE_NAME',
    'BUILDING_NAME',
    'DATE_FROM',
    'PREV_COURSE_NAME',
    'NEXT_COURSE_NAME',
    'ACCESS_LEVEL',
    'AREA'
]].rename(columns={
    'BUILDING_NAME': 'BUILDING_OF_COURSE_LOCATION',
    'AREA': 'ROOM_ASSIGNABLE_AREA'
})

# Final sort as required
result = result.sort_values(['DATE_FROM', 'COURSE_NAME'], kind='mergesort')

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
