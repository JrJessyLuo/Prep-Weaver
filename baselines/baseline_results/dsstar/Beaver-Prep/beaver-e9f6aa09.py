import pandas as pd

# Access pre-loaded tables
df = tables['table_1']  # SIS_SUBJECT_CODE.pkl
dept = tables['table_6']  # SIS_DEPARTMENT.pkl

# Identify degree-granting schools from SIS_DEPARTMENT
deg_mask = (dept['IS_DEGREE_GRANTING'].astype(str).str.upper() == 'Y')
degree_granting_schools = (
    dept.loc[deg_mask, 'SCHOOL_NAME']
        .dropna()
        .drop_duplicates()
        .tolist()
)

# Compute total unique courses by SCHOOL_NAME
total_courses_by_school = (
    df.groupby('SCHOOL_NAME', dropna=False)['COURSE_NUMBER']
      .nunique()
      .rename('total_courses')
)

# Compute degree_granting_courses by SCHOOL_NAME
def count_deg_courses(group):
    if group.name in degree_granting_schools:
        return group['COURSE_NUMBER'].nunique()
    return 0

degree_granting_courses_by_school = (
    df.groupby('SCHOOL_NAME', dropna=False)
      .apply(count_deg_courses)
      .rename('degree_granting_courses')
)

# Combine results and sort
final_df = (
    pd.concat([total_courses_by_school, degree_granting_courses_by_school], axis=1)
      .sort_values(by=['degree_granting_courses', 'total_courses'], ascending=False)
      .reset_index()
)

# Package final answer
result = {
    'school_course_counts': final_df
}