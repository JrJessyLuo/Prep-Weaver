import pandas as pd
import numpy as np
import re

departments = tables["table_1"].copy()
sis_courses = tables["table_2"].copy()

departments["_department_code"] = departments["DEPARTMENT_CODE"].astype("string").str.strip()
sis_courses["_department_code"] = sis_courses["DEPARTMENT"].astype("string").str.strip()
sis_courses["_course_number"] = sis_courses["COURSE"].astype("string").str.strip()

grad_col = "GRADUATE_LEVEL" if "GRADUATE_LEVEL" in sis_courses.columns else "GRADAUTE_LEVEL"
sis_courses["_graduate_level"] = sis_courses[grad_col]

dept_lookup = (
    departments[
        ["_department_code", "SCHOOL_CODE", "SCHOOL_NAME", "DLC_KEY"]
    ]
    .drop_duplicates(subset=["_department_code"])
)

merged = sis_courses.merge(
    dept_lookup,
    on="_department_code",
    how="left",
    suffixes=("_sis", "_dept")
)

merged["_school_name"] = merged["SCHOOL_NAME_dept"].combine_first(merged["SCHOOL_NAME_sis"])
merged["_school_code"] = merged["SCHOOL_CODE"]
merged["_dlc_key"] = merged["DLC_KEY"]

def course_sort_key(value):
    if pd.isna(value):
        return (1, "")
    s = str(value).strip().upper()
    parts = re.split(r"(\d+)", s)
    key = []
    for part in parts:
        if not part:
            continue
        if part.isdigit():
            key.append((0, int(part)))
        else:
            key.append((1, part))
    return (0, key)

def min_course(series):
    vals = [v for v in series.dropna().astype(str).str.strip().unique() if v]
    return min(vals, key=course_sort_key) if vals else pd.NA

def max_course(series):
    vals = [v for v in series.dropna().astype(str).str.strip().unique() if v]
    return max(vals, key=course_sort_key) if vals else pd.NA

answer = (
    merged
    .groupby(
        ["_school_code", "_school_name", "_dlc_key", "_graduate_level"],
        dropna=False,
        as_index=False
    )
    .agg(
        total_number_of_sis_subjects=("SIS_COURSE_DESCRIPTION_KEY", "nunique"),
        minimum_course_number=("_course_number", min_course),
        maximum_course_number=("_course_number", max_course),
        total_number_of_departments_offering_subjects=("_department_code", "nunique")
    )
    .rename(columns={
        "_school_code": "school_code",
        "_school_name": "school_name",
        "_dlc_key": "dlc_key",
        "_graduate_level": "graduate_level"
    })
    .sort_values(
        ["school_code", "school_name", "dlc_key", "graduate_level"],
        na_position="last"
    )
    .reset_index(drop=True)
)

result = {
    "school_sis_subject_summary": answer
}
