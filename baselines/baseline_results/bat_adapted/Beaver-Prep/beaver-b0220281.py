import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['term_code','TERM_DESCRIPTION','IS_CURRENT_TERM']].copy()
    df['IS_CURRENT_TERM'] = df['IS_CURRENT_TERM'].astype(str).str.strip()
    df = df.groupby(['term_code','TERM_DESCRIPTION'], as_index=False)['IS_CURRENT_TERM'].max()
    target = df[['term_code','TERM_DESCRIPTION','IS_CURRENT_TERM']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1.loc[:, ['TERM_CODE', 'COURSE_NUMBER']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_3'])
terms = prepared_table_1
prepared_table_2 = _prep_2(tables['table_7'])
subject_offerings = prepared_table_2

# Assume prepared tables are provided as DataFrames: terms, subject_offerings
# 1) Join terms to offerings by term
joined = terms.merge(subject_offerings, left_on='term_code', right_on='TERM_CODE', how='left')

# 2) Filter to CIS course offerings (COURSE_NUMBER equals 'CIS')
cis = joined[joined['COURSE_NUMBER'].fillna('') == 'CIS']

# 3) Count distinct CIS course "types" per term. Interpret "types" as distinct COURSE_NUMBER values within CIS; since COURSE_NUMBER is constant 'CIS', use distinct SUBJECT_ID if available; but with current targets we only have COURSE_NUMBER, so count distinct SUBJECT_ID is not possible. Instead, count distinct SUBJECT_ID would be preferable; if available in source, add it to target_columns. Fallback: count distinct SUBJECT_ID via original table if present.
# If SUBJECT_ID exists in subject_offerings (it does in source), better target included it. Let's adjust using available column if present at runtime.
if 'SUBJECT_ID' in subject_offerings.columns:
    # Recompute with SUBJECT_ID
    joined2 = terms.merge(subject_offerings[['TERM_CODE','COURSE_NUMBER','SUBJECT_ID']], left_on='term_code', right_on='TERM_CODE', how='left')
    cis2 = joined2[joined2['COURSE_NUMBER'].fillna('') == 'CIS']
    counts = cis2.groupby('term_code', dropna=False)['SUBJECT_ID'].nunique().reset_index(name='total_cis_types')
else:
    counts = cis.groupby('term_code', dropna=False)['COURSE_NUMBER'].nunique().reset_index(name='total_cis_types')

# 4) Attach term description and current flag
result = terms.merge(counts, on='term_code', how='left')
result['total_cis_types'] = result['total_cis_types'].fillna(0).astype(int)

# 5) Final selection/renaming
final = result[['term_code', 'TERM_DESCRIPTION', 'IS_CURRENT_TERM', 'total_cis_types']]

final

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
