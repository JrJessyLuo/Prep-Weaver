import pandas as pd
import numpy as np

def _prep_1(table_1):
    df = table_1.copy()
    df['RECORD_COUNT'] = pd.to_numeric(df['RECORD_COUNT'], errors='coerce')
    target = df[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','subject_id','TIP_MATERIAL_STATUS_KEY','RECORD_COUNT']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['tip_material_status_key','TIP_MATERIAL_STATUS_CODE','TIP_MATERIAL_STATUS']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','OFFER_DEPT_CODE','OFFER_DEPT_NAME']].copy()
    prepared = prepared.drop_duplicates(subset=['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID'])
    target = prepared[['TIP_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','OFFER_DEPT_CODE','OFFER_DEPT_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_4(table_1):
    prepared = table_1[['LIBRARY_SUBJECT_OFFERED_KEY','TERM_CODE','SUBJECT_ID','LIBRARY_MATERIAL_STATUS_KEY']]
    target = prepared.drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_5(table_1):
    target = table_1[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS_CODE','LIBRARY_MATERIAL_STATUS']].drop_duplicates().reset_index(drop=True)
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_6(table_1):
    target = table_1.copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_tip_materials = prepared_table_1
prepared_table_2 = _prep_2(tables['table_2'])
prepared_tip_status_dim = prepared_table_2
prepared_table_3 = _prep_3(tables['table_6'])
prepared_offerings = prepared_table_3
prepared_table_4 = _prep_4(tables['table_4'])
prepared_library_materials = prepared_table_4
prepared_table_5 = _prep_5(tables['table_3'])
prepared_library_status_dim = prepared_table_5
prepared_table_6 = _prep_6(tables['table_7'])

## Assumes the prepared_* DataFrames are already materialized as per table_targets.
# Join TIP to offerings to get department
_tip = prepared_tip_materials.merge(prepared_offerings[['TIP_SUBJECT_OFFERED_KEY','OFFER_DEPT_NAME']], on='TIP_SUBJECT_OFFERED_KEY', how='left')
# Attach readable TIP status
_tip = _tip.merge(prepared_tip_status_dim[['tip_material_status_key','TIP_MATERIAL_STATUS']], left_on='TIP_MATERIAL_STATUS_KEY', right_on='tip_material_status_key', how='left')
_tip['material_status'] = _tip['TIP_MATERIAL_STATUS_KEY']
# Count TIP materials per department and status (RECORD_COUNT treated as weight if present numeric)
if 'RECORD_COUNT' in _tip.columns and _tip['RECORD_COUNT'].notna().all():
    _tip_counts = _tip.groupby(['OFFER_DEPT_NAME','material_status'], dropna=False)['RECORD_COUNT'].sum().reset_index(name='tip_count')
else:
    _tip_counts = _tip.groupby(['OFFER_DEPT_NAME','material_status'], dropna=False).size().reset_index(name='tip_count')

# Join Library to offerings to get department (via subject offered key)
_lib = prepared_library_materials.merge(prepared_offerings[['TIP_SUBJECT_OFFERED_KEY','OFFER_DEPT_NAME']], left_on='LIBRARY_SUBJECT_OFFERED_KEY', right_on='TIP_SUBJECT_OFFERED_KEY', how='left')
# Attach readable Library status
_lib = _lib.merge(prepared_library_status_dim[['LIBRARY_MATERIAL_STATUS_KEY','LIBRARY_MATERIAL_STATUS']], on='LIBRARY_MATERIAL_STATUS_KEY', how='left')
_lib['material_status'] = _lib['LIBRARY_MATERIAL_STATUS_KEY']
# Count Library materials per department and status
_lib_counts = _lib.groupby(['OFFER_DEPT_NAME','material_status'], dropna=False).size().reset_index(name='library_count')

# Combine TIP and Library counts by department and material status
_counts = merge(_tip_counts, _lib_counts, on=['OFFER_DEPT_NAME','material_status'], how='outer').fillna(0)
_counts['tip_count'] = _counts['tip_count'].astype(int)
_counts['library_count'] = _counts['library_count'].astype(int)
_counts['total_count'] = _counts['tip_count'] + _counts['library_count']
_counts = _counts.rename(columns={'OFFER_DEPT_NAME':'department_name'})

# Build subtotals per department
_dept_subtotals = _counts.groupby('department_name', dropna=False)[['tip_count','library_count','total_count']].sum().reset_index()
_dept_subtotals.insert(1, 'material_status', 'Subtotal')

# Grand total across all departments
_grand_total = _counts[['tip_count','library_count','total_count']].sum().to_frame().T
_grand_total.insert(0, 'department_name', 'Grand Total')
_grand_total.insert(1, 'material_status', '')

# Final result: detail rows + department subtotals + grand total
result = (
    _counts[['department_name','material_status','tip_count','library_count','total_count']]
    .sort_values(['department_name','material_status'])
)
result = (
    pandas.concat([result, _dept_subtotals[['department_name','material_status','tip_count','library_count','total_count']], _grand_total[['department_name','material_status','tip_count','library_count','total_count']]], ignore_index=True)
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
