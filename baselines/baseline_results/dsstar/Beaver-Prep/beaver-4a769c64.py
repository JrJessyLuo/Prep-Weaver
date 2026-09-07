import pandas as pd

# 1) Load DataFrames from the provided `tables` dict
df_lib = tables['table_1']  # LIBRARY_RESERVE_MATRL_DETAIL.pkl
df_status = tables['table_3']  # LIBRARY_MATERIAL_STATUS.pkl
df_terms = tables['table_6']  # ACADEMIC_TERMS_ALL.pkl
df_tip_so = tables['table_4']  # TIP_SUBJECT_OFFERED.pkl

# 2) Select minimal fields and prepare for joins (reproduce reference logic)
lib_cols = [
    "LIBRARY_COURSE_INSTRUCTOR_KEY",
    "LIBRARY_RESERVE_CATALOG_KEY",
    "LIBRARY_SUBJECT_OFFERED_KEY",
    "LIBRARY_MATERIAL_STATUS_KEY",
    "TERM_CODE",
    "SUBJECT_ID",
    "WAREHOUSE_LOAD_DATE",
]
df_lib2 = df_lib[[c for c in lib_cols if c in df_lib.columns]].copy()

status_cols = [
    "LIBRARY_MATERIAL_STATUS_KEY",
    "LIBRARY_MATERIAL_STATUS_CODE",
    "LIBRARY_MATERIAL_STATUS",
]
df_status2 = df_status[[c for c in status_cols if c in df_status.columns]].drop_duplicates().copy()

terms_cols = [
    "term_code",
    "TERM_DESCRIPTION",
    "TERM_START_DATE",
    "TERM_END_DATE",
    "ACADEMIC_YEAR",
    "IS_CURRENT_TERM",
]
df_terms2 = df_terms[[c for c in terms_cols if c in df_terms.columns]].drop_duplicates().copy()

tip_cols = [
    "TERM_CODE",
    "SUBJECT_ID",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "RESPONSIBLE_FACULTY_NAME",
    "SUBJECT_TITLE",
    "NUM_ENROLLED_STUDENTS",
    "IS_NO_COURSE_MATERIAL",
]
df_tip2 = df_tip_so[[c for c in tip_cols if c in df_tip_so.columns]].drop_duplicates().copy()

# Normalize key dtypes to strings for safer joins
for df_, cols in [
    (df_lib2, ["LIBRARY_MATERIAL_STATUS_KEY", "TERM_CODE", "SUBJECT_ID"]),
    (df_status2, ["LIBRARY_MATERIAL_STATUS_KEY"]),
    (df_terms2, ["term_code"]),
    (df_tip2, ["TERM_CODE", "SUBJECT_ID"]),
]:
    for c in cols:
        if c in df_.columns:
            df_[c] = df_[c].astype(str)

# 3) Join pipeline (reproduce reference logic)
# a) Join material status
df_join = df_lib2.merge(df_status2, on="LIBRARY_MATERIAL_STATUS_KEY", how="left")

# b) Join terms (TERM_CODE -> term_code)
if "TERM_CODE" in df_join.columns and "term_code" in df_terms2.columns:
    df_join = df_join.merge(df_terms2, left_on="TERM_CODE", right_on="term_code", how="left")
    if "term_code" in df_join.columns:
        df_join = df_join.drop(columns=["term_code"])

# c) Left-join TIP_SUBJECT_OFFERED by [TERM_CODE, SUBJECT_ID]
tip_keys = [k for k in ["TERM_CODE", "SUBJECT_ID"] if k in df_join.columns and k in df_tip2.columns]
if tip_keys:
    df_join = df_join.merge(df_tip2, on=tip_keys, how="left")

# 4) Select output columns and de-duplicate
out_cols = [
    "LIBRARY_COURSE_INSTRUCTOR_KEY",
    "LIBRARY_RESERVE_CATALOG_KEY",
    "LIBRARY_SUBJECT_OFFERED_KEY",
    "LIBRARY_MATERIAL_STATUS_KEY",
    "LIBRARY_MATERIAL_STATUS_CODE",
    "LIBRARY_MATERIAL_STATUS",
    "TERM_CODE",
    "SUBJECT_ID",
    "WAREHOUSE_LOAD_DATE",
    "TERM_DESCRIPTION",
    "TERM_START_DATE",
    "TERM_END_DATE",
    "ACADEMIC_YEAR",
    "IS_CURRENT_TERM",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "RESPONSIBLE_FACULTY_NAME",
    "SUBJECT_TITLE",
    "NUM_ENROLLED_STUDENTS",
    "IS_NO_COURSE_MATERIAL",
]
out_cols = [c for c in out_cols if c in df_join.columns]
df_base = df_join[out_cols].drop_duplicates().reset_index(drop=True)

# 5) Aggregations per requirement:
# - material status (name) and term description
# - total number of courses: count distinct SUBJECT_ID within (status code, term)
# - total number of materials: count rows (or distinct LIBRARY_RESERVE_CATALOG_KEY to be conservative)
# - occurrences in departments and school: count distinct OFFER_DEPT_CODE and OFFER_SCHOOL_NAME
# - total number of instructors: count distinct LIBRARY_COURSE_INSTRUCTOR_KEY

group_keys = ["LIBRARY_MATERIAL_STATUS_CODE", "TERM_CODE"]

def nunique_safe(s):
    return s.dropna().nunique()

agg_df = df_base.groupby(group_keys).agg(
    MATERIAL_STATUS=("LIBRARY_MATERIAL_STATUS", lambda x: x.dropna().iloc[0] if len(x.dropna()) else None),
    TERM_DESCRIPTION=("TERM_DESCRIPTION", lambda x: x.dropna().iloc[0] if len(x.dropna()) else None),
    TOTAL_COURSES=("SUBJECT_ID", nunique_safe),
    TOTAL_MATERIALS=("LIBRARY_RESERVE_CATALOG_KEY", nunique_safe if "LIBRARY_RESERVE_CATALOG_KEY" in df_base.columns else "size"),
    OCCURRENCES_DEPARTMENTS=("OFFER_DEPT_CODE", nunique_safe),
    OCCURRENCES_SCHOOLS=("OFFER_SCHOOL_NAME", nunique_safe),
    TOTAL_INSTRUCTORS=("LIBRARY_COURSE_INSTRUCTOR_KEY", nunique_safe),
).reset_index()

# Ensure column order
final_cols = [
    "LIBRARY_MATERIAL_STATUS_CODE",
    "TERM_CODE",
    "MATERIAL_STATUS",
    "TERM_DESCRIPTION",
    "TOTAL_COURSES",
    "TOTAL_MATERIALS",
    "OCCURRENCES_DEPARTMENTS",
    "OCCURRENCES_SCHOOLS",
    "TOTAL_INSTRUCTORS",
]
agg_df = agg_df[final_cols]

# 6) Package result
result = {
    "material_status_by_term": agg_df
}