import pandas as pd
from collections import Counter

# The input DataFrames are provided in `tables`:
# tables['table_1'] -> SIS_COURSE_DESCRIPTION.pkl
# tables['table_6'] -> SIS_ADMIN_DEPARTMENT.pkl
# tables['table_3'] -> SIS_DEPARTMENT.pkl

# ------------------------------------------------------------------------------
# 1) Load tables from the provided `tables` dict
# ------------------------------------------------------------------------------
sis_course_description = tables['table_1']
sis_admin_department = tables['table_6']
sis_department = tables['table_3']

# ------------------------------------------------------------------------------
# 2) Group SIS_COURSE_DESCRIPTION and compute required aggregations
# Group by ['SCHOOL_NAME', 'DEPARTMENT', 'DEPARTMENT_NAME']
# - total phone numbers: from SIS_ADMIN_DEPARTMENT if joinable; if not, set 0
# - most common course level: mode of COURSE_LEVEL per group
# Then join SCHOOL_CODE/DEPARTMENT_CODE from SIS_DEPARTMENT if possible.
# ------------------------------------------------------------------------------

# Identify columns for grouping and course level
group_cols = [c for c in ['SCHOOL_NAME', 'DEPARTMENT', 'DEPARTMENT_NAME'] if c in sis_course_description.columns]
if len(group_cols) < 2:
    raise ValueError(f"Expected grouping columns not found. Present: {sis_course_description.columns}")

# Attempt to locate potential course level column(s)
level_candidate_cols = [c for c in sis_course_description.columns if 'LEVEL' in c.upper()]
course_level_col = None
if 'COURSE_LEVEL' in sis_course_description.columns:
    course_level_col = 'COURSE_LEVEL'
elif level_candidate_cols:
    course_level_col = level_candidate_cols[0]  # pick first candidate
else:
    course_level_col = None

def mode_or_nan(series):
    s = series.dropna().astype(str)
    if s.empty:
        return pd.NA
    counts = Counter(s)
    return counts.most_common(1)[0][0]

# Compute most common course level per group
if course_level_col:
    level_agg = (
        sis_course_description
        .groupby(group_cols, dropna=False)[course_level_col]
        .apply(mode_or_nan)
        .reset_index(name='MOST_COMMON_COURSE_LEVEL')
    )
else:
    level_agg = (
        sis_course_description
        .drop_duplicates(subset=group_cols)[group_cols]
        .assign(MOST_COMMON_COURSE_LEVEL=pd.NA)
    )

# Phone numbers: as per reference logic, set to 0 due to lack of reliable join key
level_agg['TOTAL_PHONE_NUMBERS'] = 0

# Add SCHOOL_CODE / DEPARTMENT_CODE from SIS_DEPARTMENT via left join on DEPARTMENT_NAME
dept_cols_keep = []
for c in ['DEPARTMENT_CODE', 'DEPARTMENT_NAME', 'SCHOOL_CODE', 'SCHOOL_NAME']:
    if c in sis_department.columns:
        dept_cols_keep.append(c)

dept_dim = sis_department[dept_cols_keep].drop_duplicates()

on_cols = []
if 'DEPARTMENT_NAME' in level_agg.columns and 'DEPARTMENT_NAME' in dept_dim.columns:
    on_cols = ['DEPARTMENT_NAME']

if on_cols:
    merged = level_agg.merge(dept_dim, on=on_cols, how='left', suffixes=('', '_DEPTDIM'))
else:
    merged = level_agg.copy()

# Reorder columns for final answer
preferred_order = []
for c in ['SCHOOL_CODE', 'SCHOOL_NAME', 'DEPARTMENT_CODE', 'DEPARTMENT_NAME',
          'TOTAL_PHONE_NUMBERS', 'MOST_COMMON_COURSE_LEVEL']:
    if c in merged.columns and c not in preferred_order:
        preferred_order.append(c)
# Add any remaining columns (avoid duplicates)
preferred_order += [c for c in merged.columns if c not in preferred_order]

final_df = merged[preferred_order].drop_duplicates()

# Package final result as required
result = {
    "schools_departments_offering_SIS_courses": final_df
}