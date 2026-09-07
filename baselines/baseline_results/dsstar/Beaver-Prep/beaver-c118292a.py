import pandas as pd

# Source the SUBJECT_OFFERED table from the provided tables dict
df = tables['table_7'].copy()

# Ensure TERM_CODE is string and filter for fall terms (ending with 'FA')
df['TERM_CODE'] = df['TERM_CODE'].astype(str)
fall_df = df[df['TERM_CODE'].str.endswith('FA', na=False)].copy()

# Normalize possible column name variants for responsible faculty id/email
if 'RESPONSIBLE_FACULTY_MIT_ID' in fall_df.columns and 'responsible_faculty_mit_id' not in fall_df.columns:
    fall_df = fall_df.rename(columns={'RESPONSIBLE_FACULTY_MIT_ID': 'responsible_faculty_mit_id'})
if 'RESPONSIBLE_FACULTY_EMAIL' in fall_df.columns and 'responsible_faculty_email' not in fall_df.columns:
    fall_df = fall_df.rename(columns={'RESPONSIBLE_FACULTY_EMAIL': 'responsible_faculty_email'})

# Columns we will use
cols_present = [c for c in ['SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_mit_id', 'responsible_faculty_email'] if c in fall_df.columns]
result_base = fall_df[cols_present].copy()

# Deduplicate based on SUBJECT_TITLE and RESPONSIBLE_FACULTY_NAME, keeping first occurrence (as in reference code)
deduped = result_base.drop_duplicates(subset=['SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME'], keep='first').copy()

# Compute total number of types of subjects per instructor (interpreted as count of unique SUBJECT_TITLE per RESPONSIBLE_FACULTY_NAME)
counts = deduped.groupby('RESPONSIBLE_FACULTY_NAME', dropna=False)['SUBJECT_TITLE'].nunique().reset_index(name='total_unique_subject_titles_per_instructor')

# Merge counts back to deduped
final_df = deduped.merge(counts, on='RESPONSIBLE_FACULTY_NAME', how='left')

# Reorder columns for clarity: title, instructor, email, id, count
ordered_cols = [c for c in ['SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME', 'responsible_faculty_email', 'responsible_faculty_mit_id', 'total_unique_subject_titles_per_instructor'] if c in final_df.columns]
final_df = final_df[ordered_cols]

# Assign to result dict as required
result = {
    'fall_unique_title_instructor_with_email_and_counts': final_df
}