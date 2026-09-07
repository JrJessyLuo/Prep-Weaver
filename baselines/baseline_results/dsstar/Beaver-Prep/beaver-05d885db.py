import pandas as pd

# Source tables from the provided `tables` dict
students = tables['table_1']           # MIT_STUDENT_DIRECTORY.pkl
moira_detail = tables['table_3']       # MOIRA_LIST_DETAIL.pkl
moira = tables['table_4']              # MOIRA_LIST.pkl
student_dept = tables['table_5']       # STUDENT_DEPARTMENT.pkl

# 1) Reproduce the same logic as the reference code to locate the target list and its members
target_name = 'beacon-date-date'

# Filter MOIRA_LIST to the target list
moira_target = moira.loc[moira['MOIRA_LIST_NAME'] == target_name].copy()

# Inner join with MOIRA_LIST_DETAIL to get members of the target list
members = moira_target.merge(
    moira_detail,
    on='MOIRA_LIST_KEY',
    how='inner',
    suffixes=('_LIST', '_DETAIL')
)

# 2) Compute the size of the mailing list
list_size = len(members)

# 3) Students with last names starting with H
# MIT_STUDENT_DIRECTORY has FULL_NAME and OFFICE_PHONE; last name is in LAST_NAME
students_h = students.loc[students['LAST_NAME'].str.startswith('H', na=False)].copy()

# 4) Determine "the phone numbers of departments they belong to"
# We assume STUDENT_DEPARTMENT links a student's EMAIL_ADDRESS or MIT_ID to DEPARTMENT and DEPARTMENT_PHONE (or similar).
# Infer reasonable join keys/columns by common fields:
# - MIT_STUDENT_DIRECTORY has EMAIL_ADDRESS and DEPARTMENT
# - STUDENT_DEPARTMENT is expected to have EMAIL_ADDRESS or DEPARTMENT / DEPARTMENT_PHONE columns
# We'll left-join by DEPARTMENT where possible, and prefer a department phone column if present.

# Identify likely department phone column
dept_phone_cols = [c for c in student_dept.columns if 'PHONE' in c.upper()]
dept_key_cols = []
# Prefer DEPARTMENT as the join key if present
if 'DEPARTMENT' in students_h.columns and 'DEPARTMENT' in student_dept.columns:
    dept_key_cols = ['DEPARTMENT']
elif 'EMAIL_ADDRESS' in students_h.columns and 'EMAIL_ADDRESS' in student_dept.columns:
    dept_key_cols = ['EMAIL_ADDRESS']

# Prepare a slim dept table to avoid duplicate columns
dept_cols_keep = []
if dept_key_cols:
    dept_cols_keep.extend(dept_key_cols)
if dept_phone_cols:
    # keep only one phone column if multiple; choose the first
    dept_phone_col = dept_phone_cols[0]
    dept_cols_keep.append(dept_phone_col)
else:
    # If no phone column exists, create a placeholder
    dept_phone_col = 'DEPARTMENT_PHONE'
    student_dept = student_dept.copy()
    student_dept[dept_phone_col] = pd.NA
    dept_cols_keep = list(set(dept_key_cols + [dept_phone_col]))

dept_slim = student_dept[dept_cols_keep].drop_duplicates()

# Join students with department phone
if dept_key_cols:
    students_h_dept = students_h.merge(dept_slim, on=dept_key_cols, how='left')
else:
    # If no reasonable join key, just attach NA phone
    students_h_dept = students_h.copy()
    students_h_dept[dept_phone_col] = pd.NA

# 5) Link mailing list members to students.
# MOIRA_LIST_DETAIL typically has member identifiers; try matching by EMAIL_ADDRESS if present in moira_detail
member_key_candidates = []
if 'moira_list_member' in members.columns:
    member_key_candidates.append('moira_list_member')
if 'MOIRA_LIST_MEMBER_MIT_ID' in members.columns and 'MIT_ID' in students_h_dept.columns:
    # This dataset doesn't show MIT_ID in students; fallback if available
    member_key_candidates.append('MOIRA_LIST_MEMBER_MIT_ID')

# Build a key in students to match members by email if possible
merge_on_email = False
if 'EMAIL_ADDRESS' in students_h_dept.columns and 'moira_list_member' in members.columns:
    # Often moira_list_member stores email or username; try exact email match first
    merge_on_email = True

if merge_on_email:
    merged = members.merge(
        students_h_dept,
        left_on='moira_list_member',
        right_on='EMAIL_ADDRESS',
        how='inner'
    )
else:
    # If we cannot match by email, produce empty merge (no reliable join key)
    merged = members.iloc[0:0].copy()
    # Add needed columns so downstream selection works
    for col in ['FULL_NAME', 'OFFICE_PHONE', 'DEPARTMENT', dept_phone_col]:
        if col not in merged.columns:
            merged[col] = pd.Series(dtype='object')

# 6) Keep only students whose last name starts with H (already filtered), and assemble final columns
final_cols = []
name_col = 'FULL_NAME' if 'FULL_NAME' in merged.columns else 'FULL_NAME_UPPERCASE' if 'FULL_NAME_UPPERCASE' in merged.columns else None
if name_col:
    final_cols.append(name_col)
if 'OFFICE_PHONE' in merged.columns:
    final_cols.append('OFFICE_PHONE')
if 'DEPARTMENT' in merged.columns:
    final_cols.append('DEPARTMENT')
if dept_phone_col in merged.columns:
    final_cols.append(dept_phone_col)

answer = merged[final_cols].drop_duplicates().copy()

# Add the mailing list size as a constant column
answer['MAILING_LIST_NAME'] = target_name
answer['MAILING_LIST_SIZE'] = list_size

# Rename columns to match the question phrasing
rename_map = {}
if name_col:
    rename_map[name_col] = 'STUDENT_NAME'
if 'OFFICE_PHONE' in answer.columns:
    rename_map['OFFICE_PHONE'] = 'STUDENT_OFFICE_PHONE'
if 'DEPARTMENT' in answer.columns:
    rename_map['DEPARTMENT'] = 'DEPARTMENT'
if dept_phone_col in answer.columns:
    rename_map[dept_phone_col] = 'DEPARTMENT_PHONE'

answer = answer.rename(columns=rename_map)

# Order columns
ordered_cols = [c for c in ['STUDENT_NAME', 'STUDENT_OFFICE_PHONE', 'DEPARTMENT', 'DEPARTMENT_PHONE', 'MAILING_LIST_NAME', 'MAILING_LIST_SIZE'] if c in answer.columns]
answer = answer[ordered_cols]

# Package final result
result = {
    "students_H_in_beacon_date_date": answer
}