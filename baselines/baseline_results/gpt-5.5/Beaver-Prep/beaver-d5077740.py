import pandas as pd

subjects = tables["table_1"].copy()

enroll_col = "NUM_ENROLLED_STUDENTS" if "NUM_ENROLLED_STUDENTS" in subjects.columns else "SUBJECT_ENROLLMENT_NUMBER"
subjects["_enrollment"] = pd.to_numeric(subjects[enroll_col], errors="coerce")

subjects["_subject_key"] = pd.NA
for col in ["SUBJECT_SUMMARY_KEY", "SUBJECT_OFFERED_SUMMARY_KEY"]:
    if col in subjects.columns:
        subjects["_subject_key"] = subjects["_subject_key"].combine_first(subjects[col])

if subjects["_subject_key"].isna().all():
    subjects["_subject_key"] = (
        subjects["TERM_CODE"].astype("string").str.strip()
        + "|"
        + subjects["SUBJECT_ID"].astype("string").str.strip()
    )

for col in ["CLUSTER_TYPE", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME"]:
    subjects[col] = subjects[col].astype("string").str.strip()

subjects["_dept_code_norm"] = subjects["OFFER_DEPT_CODE"].str.upper()

subjects = subjects[
    subjects["CLUSTER_TYPE"].notna()
    & (subjects["CLUSTER_TYPE"] != "")
    & subjects["OFFER_SCHOOL_NAME"].notna()
    & (subjects["OFFER_SCHOOL_NAME"] != "")
    & subjects["OFFER_DEPT_NAME"].notna()
    & (subjects["OFFER_DEPT_NAME"] != "")
    & subjects["_enrollment"].notna()
].copy()

subjects = subjects.drop_duplicates(
    subset=[
        "CLUSTER_TYPE",
        "OFFER_DEPT_CODE",
        "OFFER_DEPT_NAME",
        "OFFER_SCHOOL_NAME",
        "_subject_key",
    ]
)

dept_degree = tables["table_7"].copy()
dept_degree["DEPARTMENT_CODE"] = dept_degree["DEPARTMENT_CODE"].astype("string").str.strip()
dept_degree["_dept_code_norm"] = dept_degree["DEPARTMENT_CODE"].str.upper()
dept_degree["IS_DEGREE_GRANTING"] = dept_degree["IS_DEGREE_GRANTING"].astype("string").str.strip().str.upper()

dept_degree = (
    dept_degree.dropna(subset=["_dept_code_norm"])
    .groupby("_dept_code_norm", as_index=False)
    .agg(
        department_grants_degrees=(
            "IS_DEGREE_GRANTING",
            lambda s: "Y" if (s == "Y").any() else ("N" if (s == "N").any() else pd.NA),
        )
    )
)

if "table_5" in tables:
    course_degree = tables["table_5"].copy()
    course_degree["DEPARTMENT"] = course_degree["DEPARTMENT"].astype("string").str.strip()
    course_degree["_dept_code_norm"] = course_degree["DEPARTMENT"].str.upper()
    course_degree["IS_DEGREE_GRANTING"] = course_degree["IS_DEGREE_GRANTING"].astype("string").str.strip().str.upper()

    course_degree = (
        course_degree.dropna(subset=["_dept_code_norm"])
        .groupby("_dept_code_norm", as_index=False)
        .agg(
            fallback_department_grants_degrees=(
                "IS_DEGREE_GRANTING",
                lambda s: "Y" if (s == "Y").any() else ("N" if (s == "N").any() else pd.NA),
            )
        )
    )

    dept_degree = dept_degree.merge(course_degree, on="_dept_code_norm", how="outer")
    dept_degree["department_grants_degrees"] = dept_degree["department_grants_degrees"].combine_first(
        dept_degree["fallback_department_grants_degrees"]
    )
    dept_degree = dept_degree[["_dept_code_norm", "department_grants_degrees"]]

subjects = subjects.merge(dept_degree, on="_dept_code_norm", how="left")

summary = (
    subjects.groupby(
        [
            "CLUSTER_TYPE",
            "OFFER_DEPT_NAME",
            "OFFER_SCHOOL_NAME",
            "department_grants_degrees",
        ],
        dropna=False,
        as_index=False,
    )
    .agg(
        total_number_of_subjects=("_subject_key", "nunique"),
        total_enrollment=("_enrollment", "sum"),
    )
)

summary["average_enrollment"] = summary["total_enrollment"] / summary["total_number_of_subjects"]
summary = summary[summary["total_enrollment"] > 0].copy()

summary = summary.rename(
    columns={
        "CLUSTER_TYPE": "cluster_type",
        "OFFER_DEPT_NAME": "department_name",
        "OFFER_SCHOOL_NAME": "school_name",
    }
)

summary = (
    summary[
        [
            "cluster_type",
            "department_name",
            "school_name",
            "department_grants_degrees",
            "total_number_of_subjects",
            "total_enrollment",
            "average_enrollment",
        ]
    ]
    .sort_values(["cluster_type", "department_name", "school_name"], kind="mergesort")
    .reset_index(drop=True)
)

result = {"subject_groups_by_cluster_department_school": summary}
