import pandas as pd
import re

# 1) Load DataFrames from provided `tables` dict
sis_dept = tables['table_1'].copy()                 # SIS_DEPARTMENT.pkl
stu_deg = tables['table_4'].copy()                  # STUDENT_DEGREE_PROGRAM.pkl
cis_catalog = tables['table_7'].copy()              # CIS_COURSE_CATALOG.pkl

# 2) Build mapping from STUDENT_DEGREE_PROGRAM.COURSE -> COURSE_LEVEL via SUBJECT_CODE extracted from COURSE
def extract_subject_code_from_course(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    m = re.match(r"^([A-Za-z0-9]+)", s)
    if m:
        return m.group(1).upper()
    return s.split()[0].upper() if s else None

def norm_level(x):
    if pd.isna(x):
        return None
    s = str(x).strip()
    return s

stu_deg_map = (
    stu_deg.assign(
        SUBJECT_CODE=lambda d: d["COURSE"].map(extract_subject_code_from_course),
        COURSE_LEVEL=lambda d: d["COURSE_LEVEL"].map(norm_level),
    )
    .dropna(subset=["SUBJECT_CODE"])
)

# Build a mapping at the subject level: SUBJECT_CODE -> most frequent COURSE_LEVEL
level_counts = (
    stu_deg_map
    .dropna(subset=["COURSE_LEVEL"])
    .groupby(["SUBJECT_CODE", "COURSE_LEVEL"])
    .size()
    .reset_index(name="n")
)
level_mode = (
    level_counts
    .sort_values(["SUBJECT_CODE", "n"], ascending=[True, False])
    .drop_duplicates(subset=["SUBJECT_CODE"])
    .rename(columns={"COURSE_LEVEL": "COURSE_LEVEL_FROM_STU"})
)[["SUBJECT_CODE", "COURSE_LEVEL_FROM_STU"]]

# 3) Tag CIS_COURSE_CATALOG with COURSE_LEVEL using SUBJECT_CODE mapping from students
cis_catalog = cis_catalog.copy()
cis_catalog["SUBJECT_CODE"] = cis_catalog["SUBJECT_CODE"].astype(str).str.strip().str.upper()
cis_with_level = cis_catalog.merge(level_mode, on="SUBJECT_CODE", how="left")

# 4) Join CIS to SIS_DEPARTMENT via DEPARTMENT_CODE to get school and department info
sis_cols = ["DEPARTMENT_CODE", "DEPARTMENT_NAME", "department_full_name", "SCHOOL_CODE", "SCHOOL_NAME"]
sis_cols_existing = [c for c in sis_cols if c in sis_dept.columns]
sis_dept_slice = sis_dept[sis_cols_existing].drop_duplicates(subset=["DEPARTMENT_CODE"])

cis_enriched = cis_with_level.merge(sis_dept_slice, on="DEPARTMENT_CODE", how="left")

# 5) Degree-granting flag from SIS_DEPARTMENT
is_deg = sis_dept[["DEPARTMENT_CODE", "IS_DEGREE_GRANTING"]].copy()
if "IS_DEGREE_GRANTING" in is_deg.columns:
    is_deg["IS_DEGREE_GRANTING_BOOL"] = is_deg["IS_DEGREE_GRANTING"].astype(str).str.upper().str.strip().eq("Y")
else:
    is_deg["IS_DEGREE_GRANTING_BOOL"] = False

cis_enriched = cis_enriched.merge(
    is_deg[["DEPARTMENT_CODE", "IS_DEGREE_GRANTING_BOOL"]].drop_duplicates("DEPARTMENT_CODE"),
    on="DEPARTMENT_CODE",
    how="left"
)

# 6) Aggregate by [SCHOOL_CODE, SCHOOL_NAME, DEPARTMENT_CODE, department_full_name, COURSE_LEVEL_FROM_STU]
# Choose a unique key for "course". Prefer SUBJECT_ID if exists, else (SUBJECT_CODE, SUBJECT_NUMBER), else fallback.
course_key_cols = []
if "SUBJECT_ID" in cis_enriched.columns:
    course_key_cols = ["SUBJECT_ID"]
elif all(c in cis_enriched.columns for c in ["SUBJECT_CODE", "SUBJECT_NUMBER"]):
    course_key_cols = ["SUBJECT_CODE", "SUBJECT_NUMBER"]
else:
    for alt in [["PRINT_SUBJECT_ID"], ["SOURCE_SUBJECT_ID"]]:
        if all(c in cis_enriched.columns for c in alt):
            course_key_cols = alt
            break
    if not course_key_cols:
        cis_enriched = cis_enriched.reset_index().rename(columns={"index": "ROW_ID"})
        course_key_cols = ["ROW_ID"]

group_cols = [
    c for c in [
        "SCHOOL_CODE",
        "SCHOOL_NAME",
        "DEPARTMENT_CODE",
        "department_full_name",
        "COURSE_LEVEL_FROM_STU",
    ] if c in cis_enriched.columns
]

def count_distinct_courses(df, key_cols):
    return pd.DataFrame(df)[key_cols].drop_duplicates().shape[0]

agg_total = (
    cis_enriched
    .groupby(group_cols, dropna=False)
    .apply(lambda g: count_distinct_courses(g, course_key_cols))
    .reset_index(name="total_courses")
)

deg_subset = cis_enriched[cis_enriched["IS_DEGREE_GRANTING_BOOL"].fillna(False)].copy()
agg_deg = (
    deg_subset
    .groupby(group_cols, dropna=False)
    .apply(lambda g: count_distinct_courses(g, course_key_cols))
    .reset_index(name="degree_granting_courses")
)

agg_final = agg_total.merge(agg_deg, on=group_cols, how="left")
agg_final["degree_granting_courses"] = agg_final["degree_granting_courses"].fillna(0).astype(int)
agg_final["total_courses"] = agg_final["total_courses"].fillna(0).astype(int)

# Keep requested columns in final output
final_cols = [c for c in [
    "SCHOOL_CODE",
    "SCHOOL_NAME",
    "department_full_name",
    "COURSE_LEVEL_FROM_STU",
    "total_courses",
    "degree_granting_courses",
] if c in agg_final.columns]

final_table = agg_final[final_cols].sort_values(
    [c for c in ["SCHOOL_CODE", "SCHOOL_NAME", "department_full_name", "COURSE_LEVEL_FROM_STU"] if c in final_cols]
).reset_index(drop=True)

# Assign to result dict as required
result = {
    "courses_by_school_dept_level": final_table
}