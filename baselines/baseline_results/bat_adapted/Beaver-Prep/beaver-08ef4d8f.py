import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY','TERM_CODE','subject_id','ISBN','RECORD_COUNT']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','COURSE_NUMBER','SUBJECT_ID','SUBJECT_TITLE','OFFER_SCHOOL_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['TIP_MATERIAL_KEY','ISBN','NEW_SHELF_PRICE','USED_SHELF_PRICE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    df = table_1.copy()
    df = df[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']]
    df['tip_material_status_key'] = df['tip_material_status_key'].astype(str).str.strip()
    df['TIP_MATERIAL_STATUS_CODE'] = df['TIP_MATERIAL_STATUS_CODE'].astype(str).str.strip()
    df['TIP_MATERIAL_STATUS'] = df['TIP_MATERIAL_STATUS'].astype(str).str.strip()
    df = df.replace({'TIP_MATERIAL_STATUS': {'nan': pd.NA, '': pd.NA}})
    df = df[(df['tip_material_status_key'].notna()) & (df['tip_material_status_key'] != '') & (df['TIP_MATERIAL_STATUS_CODE'].notna()) & (df['TIP_MATERIAL_STATUS_CODE'] != '')]
    df = df[df['TIP_MATERIAL_STATUS'].notna()]
    df = df.drop_duplicates(subset=['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS'])
    target = df[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']].reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_subject_material_facts = prepared_table_1
prepared_table_2 = _prep_2(tables['table_3'])
prepared_subject_offerings = prepared_table_2
prepared_table_3 = _prep_3(tables['table_1'])
prepared_materials = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_material_status = prepared_table_4

# Merge facts with subject offerings
m1 = prepared_subject_material_facts.merge(
    prepared_subject_offerings,
    on=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE'],
    how='left'
)

# Merge facts with materials for pricing
m2 = m1.merge(
    prepared_materials,
    on='TIP_MATERIAL_KEY',
    how='left'
)

# Decode material status
m3 = m2.merge(
    prepared_material_status,
    left_on='TIP_MATERIAL_STATUS_KEY',
    right_on='tip_material_status_key',
    how='left'
)

# Ensure numeric types for aggregation
for col in ['NEW_SHELF_PRICE','USED_SHELF_PRICE']:
    m3[col] = pd.to_numeric(m3[col], errors='coerce')

# Define group keys: TIP subject (by SUBJECT_ID/TITLE) and material status
group_cols = ['COURSE_NUMBER','SUBJECT_TITLE','TIP_MATERIAL_STATUS']

agg_df = m3.groupby(group_cols).agg(
    total_new_shelf_price = ('NEW_SHELF_PRICE','sum'),
    min_new_shelf_price   = ('NEW_SHELF_PRICE','min'),
    max_new_shelf_price   = ('NEW_SHELF_PRICE','max'),
    total_used_shelf_price= ('USED_SHELF_PRICE','sum'),
    min_used_shelf_price  = ('USED_SHELF_PRICE','min'),
    max_used_shelf_price  = ('USED_SHELF_PRICE','max'),
    total_materials       = ('TIP_MATERIAL_KEY','nunique'),
    total_schools         = ('OFFER_SCHOOL_NAME','nunique')
).reset_index()

# Final result per TIP subject and material status with requested fields
target = agg_df[['COURSE_NUMBER','SUBJECT_TITLE','TIP_MATERIAL_STATUS',
                 'total_new_shelf_price','min_new_shelf_price','max_new_shelf_price',
                 'total_used_shelf_price','min_used_shelf_price','max_used_shelf_price',
                 'total_schools','total_materials']]

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
