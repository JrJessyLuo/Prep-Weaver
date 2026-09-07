import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['TIP_SUBJECT_OFFERED_KEY','TIP_MATERIAL_KEY','ISBN','TERM_CODE','subject_id']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    target = table_1[['TIP_MATERIAL_KEY','ISBN','TITLE','NEW_SHELF_PRICE']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_3(table_1):
    prepared = table_1[['TIP_SUBJECT_OFFERED_KEY','SUBJECT_TITLE']].copy()
    prepared['SUBJECT_TITLE'] = prepared['SUBJECT_TITLE'].where(prepared['SUBJECT_TITLE'].notna(), None)
    prepared = prepared.groupby('TIP_SUBJECT_OFFERED_KEY', as_index=False).agg({'SUBJECT_TITLE': lambda s: s.dropna().iloc[0] if len(s.dropna()) else None})
    target = prepared[['TIP_SUBJECT_OFFERED_KEY','SUBJECT_TITLE']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_2'])
prepared_material_assignments = prepared_table_1
prepared_table_2 = _prep_2(tables['table_1'])
prepared_material_details = prepared_table_2
prepared_table_3 = _prep_3(tables['table_4'])
prepared_subjects = prepared_table_3

# Merge subject titles into assignments
sa = prepared_material_assignments.merge(
    prepared_subjects, on='TIP_SUBJECT_OFFERED_KEY', how='left'
)

# Merge material details
sam = sa.merge(
    prepared_material_details, on=['TIP_MATERIAL_KEY', 'ISBN'], how='left'
)

# Compute per-subject total cost of new materials (sum of NEW_SHELF_PRICE per subject)
# Keep individual item rows for sorting by item price
sam['NEW_SHELF_PRICE'] = pd.to_numeric(sam['NEW_SHELF_PRICE'], errors='coerce')

subject_totals = sam.groupby('SUBJECT_TITLE', dropna=False)['NEW_SHELF_PRICE'].sum(min_count=1).rename('TOTAL_NEW_MATERIAL_COST').reset_index()

# Attach totals back to each item row
result = sam.merge(subject_totals, on='SUBJECT_TITLE', how='left')

# Select and rename columns for final output
result = result[['SUBJECT_TITLE', 'TITLE', 'ISBN', 'NEW_SHELF_PRICE', 'TOTAL_NEW_MATERIAL_COST']]

# Sort by individual item price ascending
result = result.sort_values(by=['NEW_SHELF_PRICE', 'SUBJECT_TITLE', 'TITLE'], ascending=[True, True, True])

# 'result' now contains: subject title, material title, ISBN, new shelf price (item-level), and total cost per subject
answer = result

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
