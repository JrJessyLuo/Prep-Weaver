import pandas as pd

# Inputs are provided in a dict named `tables`
students = tables['table_2'].copy()
sis_admin = tables['table_4'].copy()
sis_dept = tables['table_5'].copy()

def norm_series(s):
    return (
        s.astype(str)
         .str.strip()
         .str.lower()
         .str.replace(r'\s+', ' ', regex=True)
    )

# Prepare normalized join keys
stud = students.copy()
stud['DEPT_CODE_STUD'] = norm_series(stud['DEPARTMENT'])
stud['DEPT_NAME_STUD'] = norm_series(stud['DEPARTMENT_NAME'])

sis_d = sis_dept.copy()
sis_d['DEPT_CODE_SIS'] = norm_series(sis_d['DEPARTMENT_CODE'])
sis_d['DEPT_NAME_SIS'] = norm_series(sis_d['DEPARTMENT_NAME'])

sis_a = sis_admin.copy()
sis_a['ADMIN_DEPT_CODE'] = norm_series(sis_a['SIS_ADMIN_DEPARTMENT_CODE'])

# Determine best join path from students to SIS_DEPARTMENT
join_on_code = stud.merge(
    sis_d[['DEPT_CODE_SIS','DEPARTMENT_CODE','DEPARTMENT_NAME','department_full_name']],
    left_on='DEPT_CODE_STUD',
    right_on='DEPT_CODE_SIS',
    how='left'
)
code_match_rate = join_on_code['DEPARTMENT_CODE'].notna().mean()

join_on_name = stud.merge(
    sis_d[['DEPT_NAME_SIS','DEPARTMENT_CODE','DEPARTMENT_NAME','department_full_name']],
    left_on='DEPT_NAME_STUD',
    right_on='DEPT_NAME_SIS',
    how='left'
)
name_match_rate = join_on_name['DEPARTMENT_CODE'].notna().mean()

use_code = code_match_rate >= name_match_rate
stud_sis = join_on_code if use_code else join_on_name

# Aggregate by department code - count students and max full name length
stud_sis['DEPT_CODE_FOR_GRP'] = stud_sis['DEPARTMENT_CODE'].astype(str)
full_name_len = stud_sis['FULL_NAME'].astype(str).where(stud_sis['FULL_NAME'].notna(), "")
stud_sis['FULL_NAME_LEN'] = full_name_len.str.len()

dept_agg = (
    stud_sis
    .groupby('DEPT_CODE_FOR_GRP', dropna=False)
    .agg(
        STUDENT_COUNT=('FULL_NAME', 'size'),
        MAX_FULL_NAME_LEN=('FULL_NAME_LEN', 'max')
    )
    .reset_index()
    .rename(columns={'DEPT_CODE_FOR_GRP': 'DEPARTMENT_CODE'})
)

# Join department attributes
dept_agg = dept_agg.merge(
    sis_d[['DEPARTMENT_CODE','DEPARTMENT_NAME','department_full_name']].drop_duplicates(),
    on='DEPARTMENT_CODE',
    how='left'
)

# Left-join to SIS_ADMIN_DEPARTMENT on department code to bring phone numbers
dept_agg['DEPT_CODE_NORM'] = norm_series(dept_agg['DEPARTMENT_CODE'])
sis_a_subset = sis_a[['ADMIN_DEPT_CODE','SIS_ADMIN_DEPARTMENT_CODE','SIS_ADMIN_DEPARTMENT_NAME',
                      'DEPARTMENT_PHONE_AREA_CODE','department_phone_number']].drop_duplicates()

dept_agg_phone = dept_agg.merge(
    sis_a_subset,
    left_on='DEPT_CODE_NORM',
    right_on='ADMIN_DEPT_CODE',
    how='left'
)

# Build the final answer table: department name, phone number, number of students, and longest name length
answer_cols = [
    'DEPARTMENT_NAME',
    'department_phone_number',
    'STUDENT_COUNT',
    'MAX_FULL_NAME_LEN'
]
final_answer = (
    dept_agg_phone[answer_cols]
    .rename(columns={
        'DEPARTMENT_NAME': 'department_name',
        'department_phone_number': 'department_phone_number',
        'STUDENT_COUNT': 'student_count',
        'MAX_FULL_NAME_LEN': 'longest_full_name_length'
    })
)

# Assign to result dict as required
result = {
    'department_student_counts_with_phone': final_answer
}