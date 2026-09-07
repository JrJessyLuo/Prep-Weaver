import pandas as pd

catalog = tables["table_1"].copy()
courses = tables["table_3"].copy()

# Normalize course identifiers for matching
catalog["course_key"] = (
    catalog["COURSE_NUMBER"]
    .astype(str)
    .str.strip()
    .str.upper()
    .str.replace(r"\s+", " ", regex=True)
)

courses["course_key"] = (
    courses["COURSE"]
    .astype(str)
    .str.strip()
    .str.upper()
    .str.replace(r"\s+", " ", regex=True)
)

# One row per school/course in the SIS subject code catalog
catalog_courses = (
    catalog[["SCHOOL_NAME", "course_key"]]
    .dropna(subset=["SCHOOL_NAME", "course_key"])
    .drop_duplicates()
)

# Determine whether each course is degree-granting in SIS course descriptions
degree_flags = (
    courses.assign(is_degree_granting_flag=courses["IS_DEGREE_GRANTING"].eq("Y"))
    .groupby("course_key", as_index=False)["is_degree_granting_flag"]
    .max()
)

joined = catalog_courses.merge(degree_flags, on="course_key", how="left")
joined["is_degree_granting_flag"] = joined["is_degree_granting_flag"].fillna(False)

out = (
    joined.groupby("SCHOOL_NAME", as_index=False)
    .agg(
        total_courses_in_sis_subject_code_catalog=("course_key", "nunique"),
        total_degree_granting_courses_in_sis_subject_code_catalog=("is_degree_granting_flag", "sum"),
    )
)

out["total_degree_granting_courses_in_sis_subject_code_catalog"] = (
    out["total_degree_granting_courses_in_sis_subject_code_catalog"].astype(int)
)

out = out.sort_values("SCHOOL_NAME").reset_index(drop=True)

result = {"school_course_counts": out}
