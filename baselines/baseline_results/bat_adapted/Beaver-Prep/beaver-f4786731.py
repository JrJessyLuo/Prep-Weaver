import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','COURSE_NAME','INSTRUCTOR_NAME','DEPARTMENT','UNIT_CODE','UNIT','WAREHOUSE_LOAD_DATE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY','LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_MATERIAL_STATUS_KEY','TERM_CODE','SUBJECT_ID','WAREHOUSE_LOAD_DATE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['LIBRARY_SUBJECT_OFFERED_KEY'] = df['LIBRARY_SUBJECT_OFFERED_KEY'].astype(str).str.strip()
    df['term_code'] = df['term_code'].astype(str).str.strip()
    df['SUBJECT_ID'] = df['SUBJECT_ID'].astype(str).str.strip()
    df['SUBJECT_TITLE'] = df['SUBJECT_TITLE'].astype(str).str.strip()
    df['OFFER_DEPT_CODE'] = df['OFFER_DEPT_CODE'].astype(str).str.strip()
    df['OFFER_DEPT_NAME'] = df['OFFER_DEPT_NAME'].astype(str).str.strip()
    df['WAREHOUSE_LOAD_DATE'] = pd.to_datetime(df['WAREHOUSE_LOAD_DATE'].astype(str).str.strip(), format='%d-%b-%y', errors='coerce').dt.strftime('%Y-%m-%d')
    target = df[['LIBRARY_SUBJECT_OFFERED_KEY','term_code','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','WAREHOUSE_LOAD_DATE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_instructors = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_materials = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_subject_offered = prepared_table_3

# Assume prepared_instructors, prepared_materials, prepared_subject_offered are provided

# 1) Join instructors to materials on LIBRARY_COURSE_INSTRUCTOR_KEY
im = prepared_instructors.merge(
    prepared_materials,
    on='LIBRARY_COURSE_INSTRUCTOR_KEY',
    how='inner'
)

# 2) Join to subject offered on LIBRARY_SUBJECT_OFFERED_KEY
ims = im.merge(
    prepared_subject_offered[['LIBRARY_SUBJECT_OFFERED_KEY','SUBJECT_ID','SUBJECT_TITLE','term_code']],
    on='LIBRARY_SUBJECT_OFFERED_KEY',
    how='left'
)

# 3) Compute amount of material per instructor key and subject offered key
# Use count of unique LIBRARY_RESERVE_CATALOG_KEY as the amount of material
agg = (
    ims.groupby(['LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY','INSTRUCTOR_NAME','COURSE_NAME'], dropna=False)
       .agg(amount_of_material=('LIBRARY_RESERVE_CATALOG_KEY','nunique'))
       .reset_index()
)

# 4) Select required columns and ensure uniqueness
result = agg[['INSTRUCTOR_NAME','COURSE_NAME','amount_of_material','LIBRARY_COURSE_INSTRUCTOR_KEY','LIBRARY_SUBJECT_OFFERED_KEY']].drop_duplicates()

# 'result' contains unique instructor names, course titles, amount of material, along with the instructor key and the key of subject offered.

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
