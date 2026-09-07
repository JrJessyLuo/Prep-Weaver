import pandas as pd
import re

# Access input tables from the provided `tables` dict
hr_faculty = tables['table_1']              # HR_FACULTY_ROSTER.pkl
moira = tables['table_5']                   # MOIRA_LIST_DETAIL.pkl
subject_offered = tables['table_9']         # SUBJECT_OFFERED.pkl

# 1) Filter HR_FACULTY_ROSTER to LAST_NAME starting with 'Y'
faculty_y = hr_faculty[hr_faculty['LAST_NAME'].astype(str).str.startswith('Y', na=False)].copy()

# 2) Cast MOIRA_LIST_MEMBER_MIT_ID to string for matching
moira_cast = moira.copy()

def mitid_to_str(x):
    if pd.isna(x):
        return None
    as_int = int(float(x))
    return str(as_int)

moira_cast['MOIRA_LIST_MEMBER_MIT_ID_STR'] = moira_cast['MOIRA_LIST_MEMBER_MIT_ID'].apply(mitid_to_str)

# 3) Prepare faculty MIT_ID as string for exact ID matching
# Convert to pandas nullable Int to avoid issues, then to string
faculty_y['MIT_ID_STR'] = faculty_y['MIT_ID'].astype('Int64').astype(str)

# 4) Exact MIT_ID string match
moira_id_matched = moira_cast.merge(
    faculty_y[['MIT_ID_STR', 'MIT_ID', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'JOB_TITLE', 'HR_ORG_UNIT_TITLE']],
    left_on='MOIRA_LIST_MEMBER_MIT_ID_STR',
    right_on='MIT_ID_STR',
    how='inner'
)

# 5) Fuzzy name match: MOIRA_LIST_MEMBER_FULL_NAME contains faculty LAST_NAME (case-insensitive)
moira_names = moira.copy()
moira_names['MOIRA_LIST_MEMBER_FULL_NAME'] = moira_names['MOIRA_LIST_MEMBER_FULL_NAME'].astype(str)

unique_y_last_names = (
    faculty_y['LAST_NAME']
    .dropna()
    .astype(str)
    .str.strip()
    .str.upper()
    .unique()
    .tolist()
)

moira_names['_FULL_UP'] = moira_names['MOIRA_LIST_MEMBER_FULL_NAME'].str.upper()

name_mask = pd.Series(False, index=moira_names.index)
for ln in unique_y_last_names:
    if not ln:
        continue
    name_mask = name_mask | moira_names['_FULL_UP'].str.contains(re.escape(ln), na=False)

moira_name_candidates = moira_names[name_mask].copy()
moira_name_candidates['_LAST_UP_FROM_FULL'] = moira_name_candidates['_FULL_UP'].str.split(',').str[0].str.strip()

faculty_y['_LAST_UP'] = faculty_y['LAST_NAME'].astype(str).str.upper().str.strip()

moira_name_matched = moira_name_candidates.merge(
    faculty_y[['MIT_ID', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'JOB_TITLE', 'HR_ORG_UNIT_TITLE', '_LAST_UP']],
    left_on='_LAST_UP_FROM_FULL',
    right_on='_LAST_UP',
    how='inner'
)

# 6) Combine matches (ID-based and name-based)
common_cols = [
    'MOIRA_LIST_KEY', 'MOIRA_LIST_OWNER_KEY', 'moira_list_member', 'MOIRA_LIST_MEMBER_FULL_NAME',
    'MOIRA_LIST_MEMBER_MIT_ID', 'LAST_UPDATE_DATE', 'COUNTER', 'WAREHOUSE_LOAD_DATE',
    'MIT_ID', 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'JOB_TITLE', 'HR_ORG_UNIT_TITLE'
]

moira_id_matched_sel = moira_id_matched[[c for c in common_cols if c in moira_id_matched.columns]].copy()
moira_name_matched_sel = moira_name_matched[[c for c in common_cols if c in moira_name_matched.columns]].copy()

combined = pd.concat([moira_id_matched_sel, moira_name_matched_sel], ignore_index=True).drop_duplicates()

# 7) Extract distinct MOIRA_LIST_KEY for those matches
distinct_keys = combined['MOIRA_LIST_KEY'].dropna().drop_duplicates()

# Prepare subject counts per MOIRA list if possible
# Assumptions:
# - subject_offered may contain a column that links subjects to mailing lists by MOIRA_LIST_KEY or similar.
# Since schema is unknown, we will count subjects per MOIRA_LIST_KEY only if such a column exists.
subject_counts = pd.Series(dtype='int')
if 'MOIRA_LIST_KEY' in subject_offered.columns:
    subject_counts = (
        subject_offered[subject_offered['MOIRA_LIST_KEY'].isin(distinct_keys)]
        .groupby('MOIRA_LIST_KEY', dropna=True)
        .size()
        .rename('total_subjects_managed_by_faculty_in_list')
    )

# 8) Compute number of faculty in each list (distinct MIT_ID per list within combined)
faculty_in_list = (
    combined.dropna(subset=['MOIRA_LIST_KEY'])
    .groupby('MOIRA_LIST_KEY')['MIT_ID']
    .nunique()
    .rename('num_faculty_in_list')
)

# 9) Build final answer table: list name, total subjects (if available), and number of such faculty
# Determine list name column (commonly 'moira_list_member' or another)
list_name_col = 'moira_list_member' if 'moira_list_member' in combined.columns else None

final_df = (
    combined[['MOIRA_LIST_KEY'] + ([list_name_col] if list_name_col else [])]
    .drop_duplicates(subset=['MOIRA_LIST_KEY'])
    .set_index('MOIRA_LIST_KEY')
)

final_df = final_df.join(faculty_in_list, how='left')

if not subject_counts.empty:
    final_df = final_df.join(subject_counts, how='left')
else:
    final_df['total_subjects_managed_by_faculty_in_list'] = pd.NA

# Order columns: list name, subjects, faculty count
cols = []
if list_name_col:
    cols.append(list_name_col)
cols += ['total_subjects_managed_by_faculty_in_list', 'num_faculty_in_list']
final_df = final_df[cols].reset_index().rename(columns={'MOIRA_LIST_KEY': 'list_key'})

# Assign final result as required
result = {
    'mailing_lists_for_Y_faculty': final_df
}