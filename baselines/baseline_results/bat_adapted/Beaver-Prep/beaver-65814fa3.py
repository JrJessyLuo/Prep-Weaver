import pandas as pd
import numpy as np

def _prep_1(table_1):
    prepared = table_1[['CIP_PROGRAM_CODE','COURSE_LEVEL','IS_DEGREE_GRANTING','DEPARTMENT_NAME','SCHOOL_NAME']].copy()
    prepared = prepared.replace({'nan': pd.NA, 'NaN': pd.NA, 'None': pd.NA, '': pd.NA})
    prepared['CIP_PROGRAM_CODE'] = prepared['CIP_PROGRAM_CODE'].astype('Int64')
    target = prepared.drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['PROGRAM_CODE','CATEGORY_CODE','CATEGORY_TITLE','VERSION']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_courses = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_cip_lookup = prepared_table_2

# Assume prepared tables are provided as dataframes: prepared_courses, prepared_cip_lookup
# Ensure join key types match
prepared_courses = prepared_courses.copy()
prepared_cip_lookup = prepared_cip_lookup.copy()
prepared_courses['CIP_PROGRAM_CODE'] = prepared_courses['CIP_PROGRAM_CODE'].astype(str).str.strip()
prepared_cip_lookup['PROGRAM_CODE'] = prepared_cip_lookup['PROGRAM_CODE'].astype(str).str.strip()

# Join courses to CIP lookup to bring in category/title/version
courses_cip = prepared_courses.merge(
    prepared_cip_lookup,
    left_on='CIP_PROGRAM_CODE',
    right_on='PROGRAM_CODE',
    how='left'
)

# Total number of courses for each course level per CIP category code
total_by_level = (
    courses_cip
    .groupby(['CATEGORY_CODE', 'COURSE_LEVEL'], dropna=False)
    .size()
    .reset_index(name='total_courses_for_level')
)

# Total number of degree-granting courses per CIP category code
deg_mask = courses_cip['IS_DEGREE_GRANTING'].astype(str).str.upper().str.strip() == 'Y'
degree_totals = (
    courses_cip.loc[deg_mask]
    .groupby(['CATEGORY_CODE'], dropna=False)
    .size()
    .reset_index(name='total_degree_granting_courses')
)

# Bring in representative category title and version (per category code). If multiple versions exist, pick the max version as string-numeric.
cip_meta = (
    courses_cip
    .assign(VERSION_num=pd.to_numeric(courses_cip['VERSION'], errors='coerce'))
    .sort_values(['CATEGORY_CODE', 'VERSION_num'], ascending=[True, False])
    .drop_duplicates(['CATEGORY_CODE'])
    [['CATEGORY_CODE', 'CATEGORY_TITLE', 'VERSION']]
)

# For department and school name, there can be many within a category; aggregate as unique lists
dept_school_agg = (
    courses_cip
    .groupby('CATEGORY_CODE', dropna=False)
    .agg({
        'DEPARTMENT_NAME': lambda s: sorted(pd.unique(s.dropna().astype(str))),
        'SCHOOL_NAME': lambda s: sorted(pd.unique(s.dropna().astype(str)))
    })
    .reset_index()
)

# Combine metadata and degree totals
category_summary = (
    cip_meta
    .merge(dept_school_agg, on='CATEGORY_CODE', how='left')
    .merge(degree_totals, on='CATEGORY_CODE', how='left')
)

# Final output per category and course level with totals
result = (
    total_by_level
    .merge(category_summary, on='CATEGORY_CODE', how='left')
    .rename(columns={
        'CATEGORY_TITLE': 'category_title',
        'VERSION': 'version',
        'DEPARTMENT_NAME': 'department_name_list',
        'SCHOOL_NAME': 'school_name_list'
    })
    [['CATEGORY_CODE', 'category_title', 'version', 'department_name_list', 'school_name_list', 'COURSE_LEVEL', 'total_courses_for_level', 'total_degree_granting_courses']]
    .sort_values(['CATEGORY_CODE', 'COURSE_LEVEL'])
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
