import pandas as pd

sis_subjects = tables["table_1"].copy()
courses = tables["table_2"].copy()

# Normalize join keys and text fields
sis_subjects["dept_key"] = sis_subjects["DEPARTMENT_CODE"].astype("string").str.strip().str.upper()
sis_subjects["DEPARTMENT_NAME"] = sis_subjects["DEPARTMENT_NAME"].astype("string").str.strip()
sis_subjects["SIS_SUBJECT_CODE"] = sis_subjects["SUBJECT_CODE"].astype("string").str.strip()
sis_subjects["SUBJECT_CODE_DESC"] = sis_subjects["SUBJECT_CODE_DESC"].astype("string").str.strip()

courses["dept_key"] = courses["DEPARTMENT"].astype("string").str.strip().str.upper()
courses["course_key"] = courses["COURSE"].astype("string").str.strip()

grad_col = "GRADUATE_LEVEL" if "GRADUATE_LEVEL" in courses.columns else "GRADAUTE_LEVEL"
courses["GRADUATE_LEVEL"] = courses[grad_col].astype("string").str.strip()
courses["GRADUATE_LEVEL"] = courses["GRADUATE_LEVEL"].where(courses["GRADUATE_LEVEL"].ne(""), pd.NA)

# One row per department/SIS subject code
subject_dim = (
    sis_subjects[
        ["dept_key", "DEPARTMENT_NAME", "SIS_SUBJECT_CODE", "SUBJECT_CODE_DESC"]
    ]
    .drop_duplicates()
)

# Total number of distinct courses per department
course_counts = (
    courses.dropna(subset=["dept_key"])
    .groupby("dept_key", as_index=False)
    .agg(
        TOTAL_COURSES_PER_DEPARTMENT=(
            "course_key",
            lambda s: s.dropna().nunique()
        )
    )
)

# Graduate level(s) associated with each department
def join_unique(values):
    vals = sorted(values.dropna().astype(str).unique())
    return ", ".join(vals) if vals else pd.NA

graduate_levels = (
    courses.dropna(subset=["dept_key"])
    .groupby("dept_key", as_index=False)
    .agg(GRADUATE_LEVEL=("GRADUATE_LEVEL", join_unique))
)

final_df = (
    subject_dim
    .merge(graduate_levels, on="dept_key", how="left")
    .merge(course_counts, on="dept_key", how="left")
)

final_df["TOTAL_COURSES_PER_DEPARTMENT"] = (
    final_df["TOTAL_COURSES_PER_DEPARTMENT"]
    .fillna(0)
    .astype(int)
)

final_df = (
    final_df[
        [
            "DEPARTMENT_NAME",
            "SIS_SUBJECT_CODE",
            "SUBJECT_CODE_DESC",
            "GRADUATE_LEVEL",
            "TOTAL_COURSES_PER_DEPARTMENT",
        ]
    ]
    .sort_values(["DEPARTMENT_NAME", "SIS_SUBJECT_CODE"], na_position="last")
    .reset_index(drop=True)
)

result = {
    "department_subject_course_summary": final_df
}
