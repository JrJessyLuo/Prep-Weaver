import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['LIBRARY_RESERVE_CATALOG_KEY','LIBRARY_MATERIAL_STATUS_KEY','SUBJECT_ID','TERM_CODE']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['library_reserve_catalog_key','CATALOG_TITLE','CATALOG_YEAR']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    df = table_1[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']].copy()
    df['LIBRARY_MATERIAL_STATUS'] = df['LIBRARY_MATERIAL_STATUS'].replace('nan', pd.NA)
    target = df.drop_duplicates(subset=['LIBRARY_MATERIAL_STATUS_KEY'])[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_reserve_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_catalog = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_status_dim = prepared_table_3

# Assume prepared_reserve_assignments, prepared_catalog, prepared_status_dim are dataframes created per targets
# 1) Join reserves to catalog on catalog key
joined = prepared_reserve_assignments.merge(
    prepared_catalog,
    left_on='LIBRARY_RESERVE_CATALOG_KEY',
    right_on='library_reserve_catalog_key',
    how='inner'
)

# 2) Optionally join status descriptions (not required for counts but keeps evidence available)
joined = joined.merge(
    prepared_status_dim,
    on='LIBRARY_MATERIAL_STATUS_KEY',
    how='left'
)

# 3) Prepare features
# Compute title length (treat missing as empty string)
joined['title_len'] = joined['CATALOG_TITLE'].fillna('').astype(str).str.len()

# Normalize year: keep as integer where > 0; drop 0 or null years for grouping if considered unknown
# If 0 represents unknown, exclude from year-based aggregation
joined['CATALOG_YEAR'] = pd.to_numeric(joined['CATALOG_YEAR'], errors='coerce')
joined_valid = joined[joined['CATALOG_YEAR'].notna() & (joined['CATALOG_YEAR'] > 0)]

# 4) Derive a course identifier to count distinct courses; SUBJECT_ID alone may represent a course, optionally include TERM_CODE if courses are term-specific
joined_valid['course_id'] = joined_valid['SUBJECT_ID']

# 5) Aggregate by publication year
agg = joined_valid.groupby('CATALOG_YEAR').agg(
    total_reserved=('LIBRARY_RESERVE_CATALOG_KEY', 'count'),
    avg_title_length=('title_len', 'mean'),
    distinct_status=('LIBRARY_MATERIAL_STATUS_KEY', 'nunique'),
    num_courses=('course_id', 'nunique')
).reset_index()

# 6) Sort by year descending and select columns
result = agg.sort_values('CATALOG_YEAR', ascending=False)
result = result.rename(columns={'CATALOG_YEAR': 'publication_year'})

# Final output dataframe: columns [publication_year, total_reserved, avg_title_length, distinct_status, num_courses]
output = result[['publication_year', 'total_reserved', 'avg_title_length', 'distinct_status', 'num_courses']]

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
