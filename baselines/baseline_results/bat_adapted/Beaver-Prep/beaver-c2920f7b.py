import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_SUBJECT_OFFERED_KEY']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['library_reserve_catalog_key','CATALOG_YEAR']].drop_duplicates()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['LIBRARY_SUBJECT_OFFERED_KEY','NUM_ENROLLED_STUDENTS']].copy()
    df['LIBRARY_SUBJECT_OFFERED_KEY'] = df['LIBRARY_SUBJECT_OFFERED_KEY'].astype(str).str.strip()
    df['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(df['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0).astype(int)
    target = df.groupby('LIBRARY_SUBJECT_OFFERED_KEY', as_index=False)['NUM_ENROLLED_STUDENTS'].sum()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
reserves_by_instructor = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
instructor_lookup = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
catalog_metadata = prepared_table_3
prepared_table_4 = _prep_4(tables['table_3'])
subject_offerings = prepared_table_4

# Start from prepared tables
r = reserves_by_instructor.copy()
i = instructor_lookup.copy()
c = catalog_metadata.copy()
s = subject_offerings.copy()

# Join reserves to instructor names
ri = r.merge(i, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')

# Join catalog years to each reserve item
ric = ri.merge(c, left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key', how='left')

# Join enrollment via subject offering key
rics = ric.merge(s, on='LIBRARY_SUBJECT_OFFERED_KEY', how='left')

# Compute aggregates per instructor
# Treat CATALOG_YEAR==0 or null as missing for min/max calculations
years = rics['CATALOG_YEAR'].where(rics['CATALOG_YEAR'].notna() & (rics['CATALOG_YEAR'] != 0))
rics = rics.assign(_year=years)

# Enrollment may repeat across multiple reserve rows for the same offering; to sum students per instructor
# we first compute total enrolled per instructor by distinct subject offering keys, then combine with reserves count and year stats
# 1) total reserves and year stats per instructor
agg_reserves = rics.groupby(['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME'], dropna=False).agg(
    total_reserve_materials=('LIBRARY_RESERVE_CATALOG_KEY','count'),
    min_publication_year=('_year','min'),
    max_publication_year=('_year','max')
).reset_index()

# 2) total enrolled students per instructor = sum of NUM_ENROLLED_STUDENTS over distinct subject offerings for that instructor
distinct_offerings = rics[['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME','LIBRARY_SUBJECT_OFFERED_KEY','NUM_ENROLLED_STUDENTS']].drop_duplicates(subset=['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY'])
agg_enroll = distinct_offerings.groupby(['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME'], dropna=False).agg(
    total_enrolled_students=('NUM_ENROLLED_STUDENTS','sum')
).reset_index()

# Final result per instructor
target = agg_reserves.merge(agg_enroll, on=['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME'], how='left')

# Optional: sort by instructor name
target = target.sort_values(['INSTRUCTOR_NAME']).reset_index(drop=True)

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
