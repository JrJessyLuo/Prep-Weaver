import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['COURSE_NAME','DATE_FROM','UNIT_CODE','UNIT']].copy()
    df['DATE_FROM'] = pd.to_datetime(df['DATE_FROM'], format='%d-%b-%y', errors='coerce')
    df = df.drop_duplicates(subset=['COURSE_NAME','DATE_FROM','UNIT_CODE','UNIT'])
    target = df[['COURSE_NAME','DATE_FROM','UNIT_CODE','UNIT']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    source = table_1.copy()
    source['AREA'] = pd.to_numeric(source['AREA'], errors='coerce')
    source['ACCESS_LEVEL'] = pd.to_numeric(source['ACCESS_LEVEL'], errors='coerce').astype('Int64')
    target = source[['FCLT_BUILDING_KEY','BUILDING_ROOM','ROOM_FULL_NAME','AREA','ACCESS_LEVEL']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['FCLT_BUILDING_KEY','BUILDING_NAME','BUILDING_NAME_LONG','ACCESS_LEVEL_CODE','ASSIGNABLE_AREA']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
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
