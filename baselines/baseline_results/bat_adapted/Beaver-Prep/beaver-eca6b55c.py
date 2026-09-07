import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_MATERIAL_STATUS_KEY']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','COURSE_NAME']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['library_reserve_catalog_key','CATALOG_YEAR']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']].copy()
    df['LIBRARY_MATERIAL_STATUS'] = df['LIBRARY_MATERIAL_STATUS'].replace('nan', pd.NA)
    df = df.groupby('LIBRARY_MATERIAL_STATUS_KEY', as_index=False).agg(LIBRARY_MATERIAL_STATUS=('LIBRARY_MATERIAL_STATUS', lambda s: s.dropna().iloc[0] if s.notna().any() else s.iloc[0]))
    target = df[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']].drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY']).reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_course_material_links = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_course_info = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_catalog = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_material_status = prepared_table_4

# Assume prepared_* DataFrames are available
links = prepared_course_material_links.copy()
course = prepared_course_info.copy()
catalog = prepared_catalog.copy()
status = prepared_material_status.copy()

# Ensure compatible dtypes for joins where numeric strings may appear
if catalog['library_reserve_catalog_key'].dtype != links['LIBRARY_RESERVE_CATALOG_KEY'].dtype:
    catalog['library_reserve_catalog_key'] = catalog['library_reserve_catalog_key'].astype(str)
    links['LIBRARY_RESERVE_CATALOG_KEY'] = links['LIBRARY_RESERVE_CATALOG_KEY'].astype(str)

# Join links -> course to get COURSE_NAME
lc = links.merge(course, on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')

# Join catalog to get publication year
lc = lc.merge(catalog[['library_reserve_catalog_key','CATALOG_YEAR']], left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key', how='left')

# Join status to get status text
lc = lc.merge(status, on='LIBRARY_MATERIAL_STATUS_KEY', how='left')

# Clean year: treat non-positive or null as NaN for min/max
year = pd.to_numeric(lc['CATALOG_YEAR'], errors='coerce')
year = year.where(year > 0)
lc['CATALOG_YEAR_CLEAN'] = year

# Total number of library materials per course
agg_base = lc.groupby('COURSE_NAME', dropna=False).agg(
    total_materials=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    min_publication_year=('CATALOG_YEAR_CLEAN', 'min'),
    max_publication_year=('CATALOG_YEAR_CLEAN', 'max')
).reset_index()

# Count of materials per status per course
status_counts = (
    lc.groupby(['COURSE_NAME','LIBRARY_MATERIAL_STATUS'], dropna=False)
      .size()
      .reset_index(name='materials_per_status')
)

# If a single table output is desired with status counts pivoted per course, pivot:
status_pivot = status_counts.pivot_table(index='COURSE_NAME', columns='LIBRARY_MATERIAL_STATUS', values='materials_per_status', fill_value=0, aggfunc='sum')
status_pivot = status_pivot.reset_index()

# Merge totals/min/max with per-status counts
target = agg_base.merge(status_pivot, on='COURSE_NAME', how='left')

# target now has: COURSE_NAME, total_materials, min_publication_year, max_publication_year, and one column per material status with counts

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
