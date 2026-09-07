import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY','RECORD_COUNT']].copy()
    df['RECORD_COUNT'] = pd.to_numeric(df['RECORD_COUNT'], errors='coerce').fillna(0).astype('int64')
    target = df.groupby(['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY'], as_index=False, dropna=False)['RECORD_COUNT'].sum()
    target = target[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','TIP_MATERIAL_KEY','TIP_MATERIAL_STATUS_KEY','RECORD_COUNT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']].copy()
    df[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']] = df[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']].apply(lambda s: s.astype(str).str.strip())
    df = df.replace({'': pd.NA, 'nan': pd.NA, 'NaN': pd.NA, 'None': pd.NA})
    df = df[df['tip_material_status_key'].notna() & df['TIP_MATERIAL_STATUS_CODE'].notna()]
    df = df.drop_duplicates(subset=['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']).reset_index(drop=True)
    target = df[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','NUM_ENROLLED_STUDENTS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prep_material_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prep_material_status_dim = prepared_table_2
prepared_table_3 = _prep_3(tables['table_5'])
prep_enrollment = prepared_table_3

# Assume prepared tables exist: prep_material_assignments, prep_material_status_dim, prep_enrollment

# Join material assignments to status dim for label
assign_with_status = prep_material_assignments.merge(
    prep_material_status_dim,
    how='left',
    left_on='TIP_MATERIAL_STATUS_KEY',
    right_on='tip_material_status_key'
)

# Normalize status label: treat null/blank as 'No material status'
status_label = assign_with_status['TIP_MATERIAL_STATUS'].where(
    assign_with_status['TIP_MATERIAL_STATUS'].notna() & (assign_with_status['TIP_MATERIAL_STATUS'].astype(str).str.strip() != ''),
    'No material status'
)
assign_with_status['material_status_label'] = status_label

# Join to enrollment by subject offering and term
assign_with_enroll = assign_with_status.merge(
    prep_enrollment,
    how='left',
    on=['TIP_SUBJECT_OFFERED_KEY', 'TERM_CODE']
)

# Coerce numeric fields
assign_with_enroll['RECORD_COUNT'] = pd.to_numeric(assign_with_enroll['RECORD_COUNT'], errors='coerce').fillna(0)
assign_with_enroll['NUM_ENROLLED_STUDENTS'] = pd.to_numeric(assign_with_enroll['NUM_ENROLLED_STUDENTS'], errors='coerce').fillna(0)

# Aggregate per material status label
per_status = assign_with_enroll.groupby('material_status_label').agg(
    total_unique_materials=('TIP_MATERIAL_KEY', lambda s: s.astype(str).nunique()),
    total_records=('RECORD_COUNT', 'sum'),
    total_student_enrollment=('NUM_ENROLLED_STUDENTS', 'sum')
).reset_index()

# Grand total row across all statuses
grand = pd.DataFrame({
    'material_status_label': ['Grand Total'],
    'total_unique_materials': [assign_with_enroll['TIP_MATERIAL_KEY'].astype(str).nunique()],
    'total_records': [assign_with_enroll['RECORD_COUNT'].sum()],
    'total_student_enrollment': [assign_with_enroll['NUM_ENROLLED_STUDENTS'].sum()]
})

# Combine
result = pd.concat([per_status, grand], ignore_index=True)

# Final output
target = result[['material_status_label', 'total_unique_materials', 'total_records', 'total_student_enrollment']]

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
