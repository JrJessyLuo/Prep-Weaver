import pandas as pd

def norm_key(s):
    return s.astype("string").str.strip().str.upper().replace("", pd.NA)

def clean_text(s):
    return s.astype("string").str.strip().replace("", pd.NA)

# Course offerings / departments
courses = tables["table_4"].copy()
courses["_course_offered_key"] = norm_key(courses["LIBRARY_SUBJECT_OFFERED_KEY"])
courses["_dept_name"] = clean_text(courses["OFFER_DEPT_NAME"])

# Fallback course key if needed
fallback_course_key = norm_key(courses["SUBJECT_ID"]) + norm_key(courses["term_code"])
courses["_course_offered_key"] = courses["_course_offered_key"].fillna(fallback_course_key)

course_dept = (
    courses[["_course_offered_key", "_dept_name"]]
    .dropna(subset=["_course_offered_key", "_dept_name"])
    .drop_duplicates()
)

courses_by_dept = (
    course_dept.groupby("_dept_name", as_index=False)
    .agg(unique_courses_offered=("_course_offered_key", "nunique"))
)

# Reserve-course bridge
reserves = tables["table_1"].copy()
reserves["_course_offered_key"] = norm_key(reserves["LIBRARY_SUBJECT_OFFERED_KEY"])
fallback_reserve_key = norm_key(reserves["SUBJECT_ID"]) + norm_key(reserves["TERM_CODE"])
reserves["_course_offered_key"] = reserves["_course_offered_key"].fillna(fallback_reserve_key)
reserves["_instructor_key"] = norm_key(reserves["LIBRARY_COURSE_INSTRUCTOR_KEY"])

reserves_with_dept = reserves.merge(course_dept, on="_course_offered_key", how="left")

materials_by_dept = (
    reserves_with_dept.dropna(subset=["_dept_name"])
    .groupby("_dept_name", as_index=False)
    .agg(unique_reserved_materials=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"))
)

# Instructors
instructors = tables["table_7"].copy()
instructors["_instructor_key"] = norm_key(instructors["LIBRARY_COURSE_INSTRUCTOR_KEY"])
instructors["_instructor_name"] = clean_text(instructors["INSTRUCTOR_NAME"]).str.upper()

instructor_dim = (
    instructors[["_instructor_key", "_instructor_name"]]
    .dropna(subset=["_instructor_key"])
    .drop_duplicates()
)

reserves_instructors = reserves_with_dept.merge(
    instructor_dim,
    on="_instructor_key",
    how="left"
)

reserves_instructors["_instructor_unique"] = reserves_instructors["_instructor_name"].fillna(
    reserves_instructors["_instructor_key"]
)

instructors_by_dept = (
    reserves_instructors.dropna(subset=["_dept_name", "_instructor_unique"])
    .groupby("_dept_name", as_index=False)
    .agg(unique_instructors=("_instructor_unique", "nunique"))
)

final = (
    courses_by_dept
    .merge(materials_by_dept, on="_dept_name", how="left")
    .merge(instructors_by_dept, on="_dept_name", how="left")
)

final[["unique_reserved_materials", "unique_instructors"]] = (
    final[["unique_reserved_materials", "unique_instructors"]]
    .fillna(0)
    .astype(int)
)

final = (
    final.rename(columns={"_dept_name": "department_name"})
    [["department_name", "unique_courses_offered", "unique_reserved_materials", "unique_instructors"]]
    .sort_values(["unique_courses_offered", "department_name"], ascending=[False, True])
    .reset_index(drop=True)
)

result = {"department_course_reserve_instructor_counts": final}
