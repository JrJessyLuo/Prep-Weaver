import pandas as pd
import numpy as np

# Tables mapping (already loaded in `tables`)
moira_list_detail = tables['table_1']  # MOIRA_LIST_DETAIL.pkl
mit_student_dir = tables['table_2']    # MIT_STUDENT_DIRECTORY.pkl
moira_list = tables['table_10']        # MOIRA_LIST.pkl
moira_owner = tables['table_3']        # MOIRA_LIST_OWNER.pkl

# 1) Reproduce the same "starts with e" filtering logic as reference (case-insensitive)
mask_e = moira_list["MOIRA_LIST_NAME"].astype(str).str.startswith("e", na=False, case=False)
moira_list_e = moira_list.loc[mask_e, ["MOIRA_LIST_KEY", "MOIRA_LIST_NAME"]]

# 2) Inner join to get member rows for only those lists
members = moira_list_e.merge(
    moira_list_detail,
    on="MOIRA_LIST_KEY",
    how="inner"
)

# 3) Determine which members are Computer Science students
#    We assume MIT_STUDENT_DIRECTORY has a major/department indicator we can use.
#    Use typical CS labels and do case-insensitive contains match on likely fields.
cs_like_patterns = [
    r'\b6\b', r'course\s*6', r'computer\s*science', r'cs', r'eecs', r'elec.*eng.*comp', r'6-'
]

# Build a helper series indicating CS for each person in student directory
# Try to combine likely columns; if missing, fill with empty strings.
student_dir = mit_student_dir.copy()
for col in student_dir.columns:
    if student_dir[col].dtype == 'O':
        student_dir[col] = student_dir[col].astype(str)

# Create a single searchable string per row from common academic fields
possible_fields = [c for c in student_dir.columns if any(k in c.lower() for k in [
    'major', 'dept', 'course', 'program', 'field', 'degree', 'school'
])]
if not possible_fields:
    # fallback to all object columns if none specifically academic found
    possible_fields = [c for c in student_dir.columns if student_dir[c].dtype == 'O']

student_dir['_SEARCH_TEXT_'] = student_dir[possible_fields].apply(lambda r: ' | '.join(r.values.astype(str)), axis=1).str.lower()

pattern = '(' + '|'.join(cs_like_patterns) + ')'
student_dir['_IS_CS_'] = student_dir['_SEARCH_TEXT_'].str.contains(pattern, case=False, regex=True, na=False)

# Map identifier to student directory rows. Common keys could be MIT_ID or KERBEROS/USERNAME.
# Try to join by MIT ID first, then by username if available.
# Standardize member identifiers from moira_list_detail
mld = members.copy()

# Heuristic: MOIRA_LIST_DETAIL likely has member identifiers such as MOIRA_LIST_MEMBER_MIT_ID and moira_list_member (kerberos)
id_cols_detail = [c for c in mld.columns if 'MIT_ID' in c.upper()]
kerb_cols_detail = [c for c in mld.columns if 'KERB' in c.lower() or 'USER' in c.lower() or 'moira_list_member' == c]

# Student directory potential join keys
id_cols_student = [c for c in student_dir.columns if 'MIT_ID' in c.upper()]
kerb_cols_student = [c for c in student_dir.columns if 'KERB' in c.lower() or 'USER' in c.lower() or 'EMAIL' in c.lower()]

# Prepare two left merges and coalesce CS flags
def left_merge_cs_flag(left_df, left_key, right_df, right_key):
    df = left_df.merge(
        right_df[[right_key, '_IS_CS_']].drop_duplicates(),
        left_on=left_key,
        right_on=right_key,
        how='left'
    )
    return df

m = mld.copy()
m['_IS_CS_FLAG_1'] = np.nan
m['_IS_CS_FLAG_2'] = np.nan

# Join by MIT ID if available
if id_cols_detail and id_cols_student:
    m = m.merge(
        student_dir[[id_cols_student[0], '_IS_CS_']].drop_duplicates(),
        left_on=id_cols_detail[0],
        right_on=id_cols_student[0],
        how='left'
    ).rename(columns={'_IS_CS_':'_IS_CS_FLAG_1'})

# Join by kerberos/username if available
if kerb_cols_detail and kerb_cols_student:
    m = m.merge(
        student_dir[[kerb_cols_student[0], '_IS_CS_']].drop_duplicates(),
        left_on=kerb_cols_detail[0],
        right_on=kerb_cols_student[0],
        how='left'
    ).rename(columns={'_IS_CS_':'_IS_CS_FLAG_2'})

# Coalesce flags
if '_IS_CS_FLAG_1' not in m.columns:
    m['_IS_CS_FLAG_1'] = np.nan
if '_IS_CS_FLAG_2' not in m.columns:
    m['_IS_CS_FLAG_2'] = np.nan

m['_IS_CS_FINAL_'] = m[['_IS_CS_FLAG_1', '_IS_CS_FLAG_2']].any(axis=1)

# 4) Compute per-list member counts and CS proportions
grp = m.groupby(['MOIRA_LIST_KEY', 'MOIRA_LIST_NAME'], dropna=False)
counts = grp['_IS_CS_FINAL_'].agg(
    total_members='size',
    cs_members='sum'
).reset_index()
counts['cs_ratio'] = counts['cs_members'] / counts['total_members']

# 5) Filter: member count between 10 and 20 inclusive, and cs_ratio > 0.75
filtered = counts[(counts['total_members'].between(10, 20, inclusive='both')) & (counts['cs_ratio'] > 0.75)]

# 6) Attach owner information: MOIRA_LIST_OWNER provides owner by MOIRA_LIST_KEY
# Expect columns like MOIRA_LIST_KEY and MOIRA_LIST_OWNER_KEY or owner name/email columns
owner_cols_keep = [c for c in moira_owner.columns if 'MOIRA_LIST_KEY' in c or 'OWNER' in c.upper() or 'NAME' in c.upper() or 'EMAIL' in c.upper()]
owners = moira_owner[owner_cols_keep].drop_duplicates()

out = filtered.merge(owners, on='MOIRA_LIST_KEY', how='left')

# Select relevant output columns: list name, owner (best-effort), member count
# Try to pick a reasonable owner display column
owner_display_cols = [c for c in owners.columns if any(k in c.lower() for k in ['owner_name', 'owner_full_name', 'owner', 'contact', 'email'])]
owner_col = owner_display_cols[0] if owner_display_cols else ( [c for c in owners.columns if c != 'MOIRA_LIST_KEY'][0] if len(owners.columns) > 1 else 'MOIRA_LIST_KEY' )

final_cols = ['MOIRA_LIST_NAME', owner_col, 'total_members']
final = out[[c for c in final_cols if c in out.columns]].drop_duplicates().sort_values(['MOIRA_LIST_NAME', 'total_members'])

# Package final result
result = {
    "e_lists_cs_heavy_10_to_20": final.reset_index(drop=True)
}