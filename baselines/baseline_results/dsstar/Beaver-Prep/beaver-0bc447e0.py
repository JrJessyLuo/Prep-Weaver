import pandas as pd

# Access the SUBJECT_OFFERED table from the provided tables dict
df = tables['table_4'].copy()

# Ensure TERM_CODE is string
df['TERM_CODE'] = df['TERM_CODE'].astype(str)

# Filter rows where TERM_CODE ends with "SU" (summer terms)
summer_df = df[df['TERM_CODE'].str.endswith('SU', na=False)]

# Select desired columns
result_df = summer_df[['SUBJECT_TITLE', 'RESPONSIBLE_FACULTY_NAME']].copy()

# Prepare a length column treating NaN as 0
result_df['INSTRUCTOR_NAME_LEN'] = result_df['RESPONSIBLE_FACULTY_NAME'].fillna('').astype(str).str.len()

# Aggregate by SUBJECT_TITLE
agg_df = result_df.groupby('SUBJECT_TITLE', dropna=False).agg(
    number_of_instructors=('RESPONSIBLE_FACULTY_NAME', lambda s: s.dropna().nunique()),
    longest_instructor_name_length=('INSTRUCTOR_NAME_LEN', 'max')
).reset_index()

# Assign final answer to `result` dict as required
result = {
    "summer_subjects_instructors_summary": agg_df
}