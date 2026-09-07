import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1.drop(columns=['WAREHOUSE_LOAD_DATE'])
    target = target[['TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY','TERM_CODE','subject_id','ISBN','RECORD_COUNT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    import numpy as np
    material = table_1[['TIP_MATERIAL_KEY','ISBN','AUTHOR','TITLE','EDITION','PUBLISHER','YEAR']].copy()
    material = material.replace({'nan': np.nan, 'NaN': np.nan, 'NAN': np.nan, '': np.nan, ' ': np.nan})
    material['TIP_MATERIAL_KEY'] = material['TIP_MATERIAL_KEY'].astype(str).str.strip()
    material = material.replace({r'^\s*$': np.nan}, regex=True)
    material = material.groupby('TIP_MATERIAL_KEY', as_index=False).agg(lambda s: s.dropna().iloc[0] if s.dropna().shape[0] > 0 else np.nan)
    target = material[['TIP_MATERIAL_KEY','ISBN','AUTHOR','TITLE','EDITION','PUBLISHER','YEAR']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME']].copy()
    prepared = prepared.drop_duplicates()
    target = prepared[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','SUBJECT_TITLE','OFFER_DEPT_CODE','OFFER_DEPT_NAME','OFFER_SCHOOL_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_material_fact = prepared_table_1
prepared_table_2 = _prep_2(tables['table_6'])
prepared_material_dim = prepared_table_2
prepared_table_3 = _prep_3(tables['table_3'])
prepared_subject_offered = prepared_table_3

# Start from prepared tables
fact = prepared_material_fact.copy()
mat = prepared_material_dim.copy()
off = prepared_subject_offered.copy()

# Join fact to material dimension to get author
fm = fact.merge(mat, how='left', on='TIP_MATERIAL_KEY')

# Join to offerings to get school
fmo = fm.merge(off[['TIP_SUBJECT_OFFERED_KEY','OFFER_SCHOOL_NAME','SUBJECT_ID']], how='left', on='TIP_SUBJECT_OFFERED_KEY')

# Normalize types and clean
fmo['RECORD_COUNT'] = pd.to_numeric(fmo['RECORD_COUNT'], errors='coerce').fillna(0).astype(int)
# Treat missing/placeholder authors consistently
fmo['AUTHOR'] = fmo['AUTHOR'].fillna('Unknown')
# Material status as-is from fact
fmo['TIP_MATERIAL_STATUS_KEY'] = fmo['TIP_MATERIAL_STATUS_KEY'].fillna('Unknown')

# Compute aggregations per author, school, material status
group_cols = ['AUTHOR','OFFER_SCHOOL_NAME','TIP_MATERIAL_STATUS_KEY']
agg = fmo.groupby(group_cols).agg(
    total_record_counts=('RECORD_COUNT','sum'),
    total_number_of_types_of_courses=('SUBJECT_ID', pd.Series.nunique)
).reset_index()

# Final output per author and school with material status, totals and distinct course types
target = agg

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
