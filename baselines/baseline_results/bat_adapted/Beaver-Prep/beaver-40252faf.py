import pandas as pd
import numpy as np

def _prep_1(table_1):
    cols = ['TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY','TERM_CODE','subject_id','ISBN']
    target = table_1[cols].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['TIP_MATERIAL_KEY','ISBN','TITLE','AUTHOR']].copy()
    df['ISBN'] = df['ISBN'].astype('string').str.strip()
    df.loc[df['ISBN'].str.lower().isin(['nan','none','']), 'ISBN'] = pd.NA
    df['TITLE'] = df['TITLE'].astype('string')
    df['AUTHOR'] = df['AUTHOR'].astype('string')
    target = df.groupby('TIP_MATERIAL_KEY', as_index=False).agg({'ISBN':'first','TITLE':'first','AUTHOR':'first'})
    target = target[['TIP_MATERIAL_KEY','ISBN','TITLE','AUTHOR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','OFFER_DEPT_CODE','OFFER_DEPT_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    target = table_1[['LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_SUBJECT_OFFERED_KEY','LIBRARY_MATERIAL_STATUS_KEY','TERM_CODE','SUBJECT_ID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_5(table_1):
    target = table_1[['library_reserve_catalog_key','CATALOG_TITLE','CATALOG_AUTHOR_NAME','CATALOG_ISBN']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_6(table_1):
    prepared = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME','DEPARTMENT']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['LIBRARY_COURSE_INSTRUCTOR_KEY','INSTRUCTOR_NAME','DEPARTMENT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_7(table_1):
    target = table_1[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']].copy()
    target['LIBRARY_MATERIAL_STATUS'] = target['LIBRARY_MATERIAL_STATUS'].replace('nan', pd.NA)
    target = target.dropna(subset=['LIBRARY_MATERIAL_STATUS'])
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_tip_material_link = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_tip_material_meta = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_subject_offered = prepared_table_3
prepared_table_4 = _prep_4(tables['table_2'])
prepared_library_reserve_links = prepared_table_4
prepared_table_5 = _prep_5(tables['table_3'])
prepared_library_catalog = prepared_table_5
prepared_table_6 = _prep_6(tables['table_7'])
prepared_library_instructors = prepared_table_6
prepared_table_7 = _prep_7(tables['table_9'])
prepared_library_material_status = prepared_table_7

# Assume the prepared tables are already materialized as dataframes with the target columns
so = prepared_subject_offered.copy()
tip_link = prepared_tip_material_link.copy()
tip_meta = prepared_tip_material_meta.copy()
lib_links = prepared_library_reserve_links.copy()
lib_cat = prepared_library_catalog.copy()
lib_status = prepared_library_material_status.copy()
lib_instr = prepared_library_instructors.copy()

# Join TIP subject offerings to material links and metadata
q = tip_link.merge(so, on='TIP_SUBJECT_OFFERED_KEY', how='left')\
        .merge(tip_meta, on='TIP_MATERIAL_KEY', how='left', suffixes=('', '_tipmeta'))

# Join to library reserves via SUBJECT_ID + TERM_CODE
q = q.merge(lib_links, how='left', left_on=['subject_id','TERM_CODE'], right_on=['SUBJECT_ID','TERM_CODE'], suffixes=('', '_lib'))

# Add library catalog details and material status text
q = q.merge(lib_cat, how='left', left_on='LIBRARY_RESERVE_CATALOG_KEY', right_on='library_reserve_catalog_key')\
     .merge(lib_status, how='left', on='LIBRARY_MATERIAL_STATUS_KEY')

# Derive availability flag text
q['Library Availability'] = q['LIBRARY_RESERVE_CATALOG_KEY'].notna().map(lambda x: 'Available in Library' if x else 'Not Available in Library')

# Compute instructors per library book: link instructors via LIBRARY_SUBJECT_OFFERED_KEY = LIBRARY_COURSE_INSTRUCTOR_KEY
# First, count distinct instructors per LIBRARY_RESERVE_CATALOG_KEY
instr_counts = lib_links.merge(lib_instr, left_on='LIBRARY_SUBJECT_OFFERED_KEY', right_on='LIBRARY_COURSE_INSTRUCTOR_KEY', how='left')\
    .groupby('LIBRARY_RESERVE_CATALOG_KEY', dropna=False)['INSTRUCTOR_NAME'].nunique().rename('Instructors per Library Book').reset_index()

q = q.merge(instr_counts, on='LIBRARY_RESERVE_CATALOG_KEY', how='left')

# Aggregate metrics per department
# Total number of materials available in the library per department
dept_lib_materials = lib_links.merge(so[['SUBJECT_ID','TERM_CODE','OFFER_DEPT_CODE','OFFER_DEPT_NAME']], on=['SUBJECT_ID','TERM_CODE'], how='left')\
    .groupby(['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], dropna=False)['LIBRARY_RESERVE_CATALOG_KEY'].nunique().rename('Total Dept Library Materials').reset_index()

# Total number of available materials across all departments (same unique catalog keys overall)
total_available_all_depts = lib_links['LIBRARY_RESERVE_CATALOG_KEY'].nunique()

# Prepare final per-row fields: department, TIP title/author/ISBN, term code, availability, instructors per book, totals
result = q[
    ['OFFER_DEPT_CODE','OFFER_DEPT_NAME','TITLE','AUTHOR','ISBN','TERM_CODE','Library Availability','LIBRARY_RESERVE_CATALOG_KEY','Instructors per Library Book']
].copy()

# Merge department totals
result = result.merge(dept_lib_materials, on=['OFFER_DEPT_CODE','OFFER_DEPT_NAME'], how='left')

# Fill instructors per book with 0 where missing (no library reserve entry)
result['Instructors per Library Book'] = result['Instructors per Library Book'].fillna(0).astype(int)

# Add global total as a constant column
result['Total Available Materials Across All Departments'] = total_available_all_depts

# Rename columns to match the question wording
result = result.rename(columns={
    'OFFER_DEPT_NAME': 'Department Name',
    'TITLE': 'TIP Material Title',
    'AUTHOR': 'Author',
    'ISBN': 'ISBN',
    'TERM_CODE': 'Library Term Code',
    'Instructors per Library Book': 'Total Instructors per Library Book (Dept)',
    'Total Dept Library Materials': 'Total Materials Available in Library (Dept)'
})

# Select and order output columns
final_columns = [
    'Department Name',
    'TIP Material Title',
    'Author',
    'ISBN',
    'Library Term Code',
    'Library Availability',
    'Total Instructors per Library Book (Dept)',
    'Total Materials Available in Library (Dept)',
    'Total Available Materials Across All Departments'
]

answer = result[final_columns].drop_duplicates()

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
