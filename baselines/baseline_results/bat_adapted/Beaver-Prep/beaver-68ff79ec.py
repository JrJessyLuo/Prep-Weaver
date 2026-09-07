import pandas as pd
import numpy as np

def _prep_1(table_1):
    target = table_1[['FIRST_NAME','MIDDLE_NAME','LAST_NAME','FULL_NAME','EMAIL_ADDRESS','DEPARTMENT','DEPARTMENT_NAME']].copy()
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()
def _prep_2(table_1):
    df = table_1[['DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']].copy()
    df = df.drop_duplicates(subset=['DEPARTMENT_CODE'])
    target = df[['DEPARTMENT_CODE','DEPARTMENT_NAME','SCHOOL_NAME']]
    if 'target' in locals() and isinstance(target, pd.DataFrame):
        return target
    if 'result' in locals() and isinstance(result, pd.DataFrame):
        return result
    return table_1.copy()

prepared_table_1 = _prep_1(tables['table_1'])
prepared_students = prepared_table_1
prepared_table_2 = _prep_2(tables['table_4'])
prepared_departments = prepared_table_2

# Assume prepared_students and prepared_departments are already synthesized from table_1 and table_2 respectively.

# Inner join students to departments on department code
joined = prepared_students.merge(
    prepared_departments,
    left_on='DEPARTMENT',
    right_on='DEPARTMENT_CODE',
    how='inner'
)

# Filter to first name Kevin (case-insensitive, robust to whitespace)
mask_kevin = joined['FIRST_NAME'].astype(str).str.strip().str.casefold() == 'kevin'
kevin_rows = joined[mask_kevin].copy()

# Build full name (prefer existing FULL_NAME; if missing, compose Last, First Middle)
# Keep the provided FULL_NAME as-is and also ensure a fallback
fallback_full = (
    kevin_rows['LAST_NAME'].fillna('').str.strip() + ', ' +
    kevin_rows['FIRST_NAME'].fillna('').str.strip() +
    kevin_rows.apply(lambda r: (' ' + r['MIDDLE_NAME'].strip() + '.') if isinstance(r['MIDDLE_NAME'], str) and r['MIDDLE_NAME'].strip() else '', axis=1)
)
kevin_rows['FULL_NAME_OUT'] = kevin_rows['FULL_NAME'].where(kevin_rows['FULL_NAME'].notna() & (kevin_rows['FULL_NAME'].astype(str).str.strip()!=''), fallback_full)

# Compute total student counts per department and per school (across all students, not just Kevins)
# Use the same join base for global counts
all_joined = joined.copy()

dept_counts = all_joined.groupby(['DEPARTMENT_CODE', 'DEPARTMENT_NAME'], dropna=False).size().reset_index(name='TOTAL_STUDENTS_IN_DEPARTMENT')
school_counts = all_joined.groupby(['SCHOOL_NAME'], dropna=False).size().reset_index(name='TOTAL_STUDENTS_IN_SCHOOL')

# Attach counts to Kevin rows
kevin_with_dept = kevin_rows.merge(dept_counts, on=['DEPARTMENT_CODE', 'DEPARTMENT_NAME'], how='left')
kevin_final = kevin_with_dept.merge(school_counts, on='SCHOOL_NAME', how='left')

# Select and rename output columns; one row per department affiliation
result = kevin_final[[
    'FIRST_NAME',
    'FULL_NAME_OUT',
    'EMAIL_ADDRESS',
    'DEPARTMENT_NAME',
    # Department phone number not available in provided tables; set as None/NaN placeholder
    'SCHOOL_NAME',
    'TOTAL_STUDENTS_IN_DEPARTMENT',
    'TOTAL_STUDENTS_IN_SCHOOL'
]].rename(columns={
    'FULL_NAME_OUT': 'FULL_NAME'
})

# Add department phone placeholder if required by downstream consumers
if 'DEPARTMENT_PHONE' not in result.columns:
    result.insert(result.columns.get_loc('SCHOOL_NAME'), 'DEPARTMENT_PHONE', pd.NA)

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
