import pandas as pd

# The input tables are provided in a dict named `tables`
# Mapping:
# tables['table_1'] -> MOIRA_LIST.pkl
# tables['table_2'] -> HR_FACULTY_ROSTER.pkl
# tables['table_6'] -> DRUPAL_EMPLOYEE_DIRECTORY.pkl
# tables['table_9'] -> MOIRA_LIST_DETAIL.pkl

# 1) Load tables from the provided `tables` dict
moira_list = tables['table_1'].copy()
hr_faculty = tables['table_2'].copy()
drupal = tables['table_6'].copy()
moira_detail = tables['table_9'].copy()

# 2) Prepare faculty IDs from HR_FACULTY_ROSTER (same logic as reference)
faculty_ids = (
    hr_faculty
    .loc[~hr_faculty['MIT_ID'].isna(), 'MIT_ID']
    .astype('int64')
    .drop_duplicates()
)

# 3) Identify support staff from DRUPAL (same heuristic as reference)
drupal_tmp = drupal.copy()
for col in ['EMPLOYEE_GROUP', 'EMPLOYEE_TYPE']:
    if col in drupal_tmp.columns:
        drupal_tmp[col] = drupal_tmp[col].astype(str).str.strip().str.lower()
    else:
        drupal_tmp[col] = ""

staff_mask = (
    drupal_tmp['EMPLOYEE_TYPE'].str.contains('staff', na=False)
    | drupal_tmp['EMPLOYEE_GROUP'].str.contains('staff', na=False)
)

staff_ids = (
    drupal_tmp.loc[staff_mask, 'MIT_ID']
    .dropna()
    .astype('int64')
    .drop_duplicates()
)

# 4) Prepare member-level dataframe from MOIRA_LIST_DETAIL
members = moira_detail[['MOIRA_LIST_KEY', 'MOIRA_LIST_MEMBER_MIT_ID']].copy()
members = members.rename(columns={'MOIRA_LIST_MEMBER_MIT_ID': 'MIT_ID'})
members = members.dropna(subset=['MIT_ID'])
members['MIT_ID'] = members['MIT_ID'].astype('int64')

# 5) Create boolean flags per MIT_ID: is_faculty, is_staff (same logic)
faculty_set = set(faculty_ids.tolist())
staff_set = set(staff_ids.tolist())

members['is_faculty'] = members['MIT_ID'].isin(faculty_set)
members['is_staff'] = members['MIT_ID'].isin(staff_set)

# 6) Summarize per list: counts of unique members flagged as faculty/staff
member_flags_per_list = (
    members
    .drop_duplicates(subset=['MOIRA_LIST_KEY', 'MIT_ID'])
    .groupby('MOIRA_LIST_KEY', as_index=False)
    .agg(
        faculty_members=('is_faculty', 'sum'),
        staff_members=('is_staff', 'sum'),
    )
)

# 7) Filter to lists that have at least one staff or faculty subscriber
member_flags_per_list = member_flags_per_list[
    (member_flags_per_list['faculty_members'] > 0) | (member_flags_per_list['staff_members'] > 0)
]

# 8) Attach list names and active status from MOIRA_LIST
moira_list_merge = moira_list[['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME', 'IS_ACTIVE']].copy()
moira_list_merge['MOIRA_LIST_KEY'] = moira_list_merge['MOIRA_LIST_KEY'].astype(str)
member_flags_per_list['MOIRA_LIST_KEY'] = member_flags_per_list['MOIRA_LIST_KEY'].astype(str)

final_df = (
    member_flags_per_list
    .merge(moira_list_merge, on='MOIRA_LIST_KEY', how='left')
    [['MOIRA_LIST_NAME', 'staff_members', 'faculty_members', 'IS_ACTIVE']]
    .rename(columns={
        'MOIRA_LIST_NAME': 'list_name',
        'staff_members': 'num_support_staff',
        'faculty_members': 'num_faculty',
        'IS_ACTIVE': 'is_active'
    })
    .sort_values(['num_support_staff', 'num_faculty', 'list_name'], ascending=[False, False, True])
    .reset_index(drop=True)
)

# 9) Package final result as required
result = {
    'email_lists_with_staff_or_faculty_counts': final_df
}