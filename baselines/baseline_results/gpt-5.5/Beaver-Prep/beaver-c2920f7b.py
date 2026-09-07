import pandas as pd
import numpy as np

# Source tables
reserves = tables["table_1"].copy()
course_instr = tables["table_2"].copy()
subjects = tables["table_3"].copy()
catalog = tables["table_5"].copy()

# Normalize join keys
reserves["course_instructor_key_norm"] = reserves["LIBRARY_COURSE_INSTRUCTOR_KEY"].astype(str).str.strip()
reserves["subject_offered_key_norm"] = reserves["LIBRARY_SUBJECT_OFFERED_KEY"].astype(str).str.strip().str.upper()

course_instr["course_instructor_key_norm"] = course_instr["LIBRARY_COURSE_INSTRUCTOR_KEY"].astype(str).str.strip()

subjects["subject_offered_key_norm"] = subjects["LIBRARY_SUBJECT_OFFERED_KEY"].astype(str).str.strip().str.upper()

catalog = catalog.rename(columns={"library_reserve_catalog_key": "LIBRARY_RESERVE_CATALOG_KEY"})
catalog["CATALOG_YEAR_CLEAN"] = pd.to_numeric(catalog["CATALOG_YEAR"], errors="coerce")
catalog.loc[catalog["CATALOG_YEAR_CLEAN"] <= 0, "CATALOG_YEAR_CLEAN"] = np.nan

# One row per course instructor key from the instructor dimension
course_instr_dim = (
    course_instr.sort_values("course_instructor_key_norm")
    .drop_duplicates("course_instructor_key_norm")
    [[
        "course_instructor_key_norm",
        "LIBRARY_COURSE_INSTRUCTOR_KEY",
        "COURSE_NAME",
        "INSTRUCTOR_NAME",
        "DEPARTMENT"
    ]]
)

# Reserve material count and publication-year range per course instructor
reserve_catalog = reserves.merge(
    catalog[["LIBRARY_RESERVE_CATALOG_KEY", "CATALOG_YEAR_CLEAN"]],
    on="LIBRARY_RESERVE_CATALOG_KEY",
    how="left"
)

reserve_agg = (
    reserve_catalog
    .groupby("course_instructor_key_norm", as_index=False)
    .agg(
        total_library_reserve_materials=("LIBRARY_RESERVE_CATALOG_KEY", "count"),
        min_publication_year=("CATALOG_YEAR_CLEAN", "min"),
        max_publication_year=("CATALOG_YEAR_CLEAN", "max")
    )
)

# Enrollment should be counted once per distinct course-instructor / subject-offering pair
subject_enrollment = (
    subjects
    .groupby("subject_offered_key_norm", as_index=False)
    .agg(NUM_ENROLLED_STUDENTS=("NUM_ENROLLED_STUDENTS", "first"))
)

course_subject_pairs = reserves[
    ["course_instructor_key_norm", "subject_offered_key_norm"]
].drop_duplicates()

enrollment_agg = (
    course_subject_pairs
    .merge(subject_enrollment, on="subject_offered_key_norm", how="left")
    .groupby("course_instructor_key_norm", as_index=False)
    .agg(total_enrolled_students=("NUM_ENROLLED_STUDENTS", "sum"))
)

# Final result
final = (
    course_instr_dim
    .merge(reserve_agg, on="course_instructor_key_norm", how="left")
    .merge(enrollment_agg, on="course_instructor_key_norm", how="left")
)

final["total_library_reserve_materials"] = final["total_library_reserve_materials"].fillna(0).astype(int)
final["total_enrolled_students"] = final["total_enrolled_students"].fillna(0).astype(int)

final = final[
    [
        "LIBRARY_COURSE_INSTRUCTOR_KEY",
        "COURSE_NAME",
        "INSTRUCTOR_NAME",
        "DEPARTMENT",
        "total_library_reserve_materials",
        "min_publication_year",
        "max_publication_year",
        "total_enrolled_students"
    ]
].sort_values(["INSTRUCTOR_NAME", "COURSE_NAME", "LIBRARY_COURSE_INSTRUCTOR_KEY"]).reset_index(drop=True)

result = {
    "course_instructor_library_reserve_summary": final
}
