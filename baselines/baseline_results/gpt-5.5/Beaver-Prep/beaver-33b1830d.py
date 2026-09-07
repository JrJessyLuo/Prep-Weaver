import pandas as pd
import numpy as np

courses = tables["table_3"].copy()

dept2 = tables["table_2"][["DEPARTMENT_CODE", "DEPARTMENT_FULL_NAME", "SCHOOL_CODE", "SCHOOL_NAME"]].copy()

dept1 = tables["table_1"][["DEPARTMENT_CODE", "department_full_name", "SCHOOL_CODE", "SCHOOL_NAME"]].copy()
dept1 = dept1.rename(columns={"department_full_name": "DEPARTMENT_FULL_NAME"})

dept_lookup = pd.concat([dept2, dept1], ignore_index=True)
for col in ["DEPARTMENT_CODE", "DEPARTMENT_FULL_NAME", "SCHOOL_CODE", "SCHOOL_NAME"]:
    dept_lookup[col] = dept_lookup[col].astype("string").str.strip()

dept_lookup = dept_lookup.drop_duplicates(subset=["DEPARTMENT_CODE"], keep="first")

for col in ["DEPARTMENT", "DEPARTMENT_NAME", "SCHOOL_NAME", "COURSE", "COURSE_LEVEL", "IS_DEGREE_GRANTING"]:
    courses[col] = courses[col].astype("string").str.strip()

df = courses.merge(
    dept_lookup,
    left_on="DEPARTMENT",
    right_on="DEPARTMENT_CODE",
    how="left",
    suffixes=("_course", "_dept")
)

df["SCHOOL_NAME_FINAL"] = df["SCHOOL_NAME_dept"].combine_first(df["SCHOOL_NAME_course"])
df["DEPARTMENT_FULL_NAME_FINAL"] = df["DEPARTMENT_FULL_NAME"].combine_first(
    df["DEPARTMENT"].fillna("") + "-" + df["DEPARTMENT_NAME"].fillna("")
)

df["course_identifier"] = df["COURSE"].combine_first(df["SIS_COURSE_DESCRIPTION_KEY"].astype("string"))
df["degree_granting_course_identifier"] = np.where(
    df["IS_DEGREE_GRANTING"].str.upper().eq("Y"),
    df["course_identifier"],
    pd.NA
)

answer = (
    df.groupby(
        ["SCHOOL_CODE", "SCHOOL_NAME_FINAL", "DEPARTMENT_FULL_NAME_FINAL", "COURSE_LEVEL"],
        dropna=False,
        as_index=False
    )
    .agg(
        total_number_of_courses=("course_identifier", "nunique"),
        total_number_of_degree_granting_courses=("degree_granting_course_identifier", lambda s: s.dropna().nunique())
    )
    .rename(columns={
        "SCHOOL_NAME_FINAL": "SCHOOL_NAME",
        "DEPARTMENT_FULL_NAME_FINAL": "DEPARTMENT_FULL_NAME"
    })
    .sort_values(["SCHOOL_CODE", "DEPARTMENT_FULL_NAME", "COURSE_LEVEL"], na_position="last")
    .reset_index(drop=True)
)

result = {
    "courses_by_school_department_level": answer
}
