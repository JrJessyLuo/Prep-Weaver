import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_SUBJECT_OFFERED_KEY','LIBRARY_MATERIAL_STATUS_KEY']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['library_reserve_catalog_key','CATALOG_TITLE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1.copy()
    df['LIBRARY_SUBJECT_OFFERED_KEY'] = df['LIBRARY_SUBJECT_OFFERED_KEY'].astype(str).str.strip()
    target = df[['LIBRARY_SUBJECT_OFFERED_KEY','SUBJECT_TITLE','term_code','SUBJECT_ID']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_reserve_links = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_catalog = prepared_table_2
prepared_table_3 = _prep_3(tables['table_7'])
prepared_subject_offered = prepared_table_3

# Merge reserve links to catalog to get material titles (sometimes used as course title)
rl_cat = prepared_reserve_links.merge(
    prepared_catalog,
    left_on='LIBRARY_RESERVE_CATALOG_KEY',
    right_on='library_reserve_catalog_key',
    how='left'
)

# Merge to subject offered to get course titles
rl_full = rl_cat.merge(
    prepared_subject_offered[['LIBRARY_SUBJECT_OFFERED_KEY','SUBJECT_TITLE']],
    on='LIBRARY_SUBJECT_OFFERED_KEY',
    how='left'
)

# Define course title preference: use SUBJECT_TITLE when available; otherwise fall back to CATALOG_TITLE
rl_full['COURSE_TITLE'] = rl_full['SUBJECT_TITLE'].where(rl_full['SUBJECT_TITLE'].notna() & (rl_full['SUBJECT_TITLE'].astype(str).str.strip() != ''), rl_full['CATALOG_TITLE'])

# Aggregate per course title
result = (
    rl_full.groupby('COURSE_TITLE', dropna=False)
           .agg(total_reserved_materials=('LIBRARY_RESERVE_CATALOG_KEY','count'),
                distinct_material_status=('LIBRARY_MATERIAL_STATUS_KEY', lambda s: s.dropna().nunique()))
           .reset_index()
)

# Sort by total number of reserved materials descending
result = result.sort_values(['total_reserved_materials','COURSE_TITLE'], ascending=[False, True]).reset_index(drop=True)

target = result[['COURSE_TITLE','total_reserved_materials','distinct_material_status']]

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
