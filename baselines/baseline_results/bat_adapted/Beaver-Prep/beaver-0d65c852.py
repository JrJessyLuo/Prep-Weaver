import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['ACADEMIC_YEAR','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','DEPARTMENT_CODE','DEPARTMENT_NAME','TOTAL_UNITS','HGN_DESC']].copy()
    df = df.drop_duplicates(subset=['TERM_CODE','SUBJECT_ID'])
    target = df[['ACADEMIC_YEAR','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','DEPARTMENT_CODE','DEPARTMENT_NAME','TOTAL_UNITS','HGN_DESC']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    prepared = table_1[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME','RESPONSIBLE_FACULTY_NAME','SECTION_ID','IS_MASTER_SECTION','IS_LECTURE_SECTION','IS_LAB_SECTION','IS_RECITATION_SECTION']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME','RESPONSIBLE_FACULTY_NAME','SECTION_ID','IS_MASTER_SECTION','IS_LECTURE_SECTION','IS_LAB_SECTION','IS_RECITATION_SECTION']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subject_catalog = prepared_table_1
prepared_table_2 = _prep_2(tables['table_5'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_8'])

# Assume prepared_subject_catalog (psc) and prepared_subject_offerings (pso) are created from table_1 and table_2 respectively

# Determine current academic year from the data (latest ACADEMIC_YEAR available)
current_year = psc['ACADEMIC_YEAR'].max()

# Keep only this year's subjects in catalog
psc_year = psc[psc['ACADEMIC_YEAR'] == current_year].copy()

# Keep only Fall or Spring term offerings for this year
# Identify Fall/Spring by TERM_CODE suffixes commonly used (e.g., 'FA' for Fall, 'SP' for Spring)
pso_year = pso[pso['TERM_CODE'].str.contains(str(current_year))].copy()

# Map term label and description
def term_label(tc):
    return 'Fall' if tc.endswith('FA') else ('Spring' if tc.endswith('SP') else None)

def term_desc(tc):
    return 'Fall Term' if tc.endswith('FA') else ('Spring Term' if tc.endswith('SP') else None)

pso_year['term_label'] = pso_year['TERM_CODE'].apply(term_label)
pso_year['term_description'] = pso_year['TERM_CODE'].apply(term_desc)

# Filter to Fall/Spring only
pso_fs = pso_year[pso_year['term_label'].notna()].copy()

# Count distinct instructors by SUBJECT_ID and term_label
# Use RESPONSIBLE_FACULTY_NAME, excluding nulls
inst = pso_fs.dropna(subset=['RESPONSIBLE_FACULTY_NAME']).copy()
inst_counts = (inst.groupby(['SUBJECT_ID', 'term_label'])['RESPONSIBLE_FACULTY_NAME']
                  .nunique()
                  .reset_index(name='distinct_instructors'))

# Pivot to separate Fall and Spring counts
inst_pivot = (inst_counts.pivot(index='SUBJECT_ID', columns='term_label', values='distinct_instructors')
                          .reset_index()
                          .rename_axis(None, axis=1))
inst_pivot['Fall'] = inst_pivot.get('Fall').fillna(0).astype(int)
inst_pivot['Spring'] = inst_pivot.get('Spring').fillna(0).astype(int)

# Join catalog with offerings (to get school and per-term presence), then deduplicate per subject-term
merged = psc_year.merge(pso_fs[['SUBJECT_ID','TERM_CODE','term_label','term_description','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME']].drop_duplicates(),
                        on=['SUBJECT_ID','TERM_CODE'], how='inner')

# For subjects offered in either term this year, create output rows per (subject, term)
# Join instructor counts back by SUBJECT_ID (term counts are split into Fall/Spring columns)
result = merged.merge(inst_pivot, on='SUBJECT_ID', how='left')

# Prepare final columns
result['Fall'] = result['Fall'].fillna(0).astype(int)
result['Spring'] = result['Spring'].fillna(0).astype(int)

# Course level from catalog HGN_DESC, total units from TOTAL_UNITS
final = result[['DEPARTMENT_NAME', 'OFFER_SCHOOL_NAME', 'SUBJECT_ID', 'SUBJECT_TITLE', 'HGN_DESC', 'TOTAL_UNITS', 'term_label', 'term_description', 'Fall', 'Spring']].drop_duplicates()
final = final.rename(columns={
    'DEPARTMENT_NAME': 'department_name',
    'OFFER_SCHOOL_NAME': 'school_name',
    'SUBJECT_ID': 'subject_id',
    'SUBJECT_TITLE': 'subject_title',
    'HGN_DESC': 'course_level',
    'TOTAL_UNITS': 'total_units',
    'term_label': 'term',
    'term_description': 'term_description',
    'Fall': 'num_distinct_instructors_fall',
    'Spring': 'num_distinct_instructors_spring'
})

# Keep only terms Fall or Spring (already ensured), and only this year (ensured by filters)
answer = final.sort_values(['department_name','subject_id','term'])

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
