import pandas as pd

# Alias input DataFrames from provided `tables` dict
lrm = tables["table_1"].copy()  # LIBRARY_RESERVE_MATRL_DETAIL
lci = tables["table_2"].copy()  # LIBRARY_COURSE_INSTRUCTOR
lso = tables["table_3"].copy()  # LIBRARY_SUBJECT_OFFERED
lrc = tables["table_5"].copy()  # LIBRARY_RESERVE_CATALOG

# Prepare/align dtypes for joins (mirror reference logic)
if lrm["LIBRARY_RESERVE_CATALOG_KEY"].dtype != "int64":
    lrm["LIBRARY_RESERVE_CATALOG_KEY"] = pd.to_numeric(
        lrm["LIBRARY_RESERVE_CATALOG_KEY"], errors="coerce"
    ).astype("Int64")
lrc["library_reserve_catalog_key"] = pd.to_numeric(
    lrc["library_reserve_catalog_key"], errors="coerce"
).astype("Int64")

# Join LRM -> LCI on LIBRARY_COURSE_INSTRUCTOR_KEY
lrm_lci = lrm.merge(
    lci[["LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME", "INSTRUCTOR_NAME", "DEPARTMENT"]],
    on="LIBRARY_COURSE_INSTRUCTOR_KEY",
    how="left",
    suffixes=("", "_LCI"),
)

# Join catalog metadata from LRC
lrm_lci_lrc = lrm_lci.merge(
    lrc[["library_reserve_catalog_key", "CATALOG_TITLE", "CATALOG_AUTHOR_NAME", "CATALOG_YEAR"]],
    left_on="LIBRARY_RESERVE_CATALOG_KEY",
    right_on="library_reserve_catalog_key",
    how="left",
    suffixes=("", "_LRC"),
)

# Prepare enrollment mapping from LSO at (TERM_CODE, SUBJECT_ID)
lso_enroll = (
    lso[["term_code", "SUBJECT_ID", "NUM_ENROLLED_STUDENTS"]]
    .dropna(subset=["term_code", "SUBJECT_ID"])
    .drop_duplicates(subset=["term_code", "SUBJECT_ID"])
    .rename(columns={"term_code": "TERM_CODE"})
)

# Join enrollment onto detailed frame
lrm_ready_for_enroll = lrm_lci_lrc.merge(
    lso_enroll,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="left",
    suffixes=("", "_LSO"),
)

# Aggregate per instructor:
# - total number of library reserve materials (distinct by catalog key)
# - min and max publication years
# - total number of enrolled students (sum across matched TERM_CODE+SUBJECT_ID rows)
agg_by_instructor_with_enroll = (
    lrm_ready_for_enroll
    .groupby("INSTRUCTOR_NAME", dropna=False)
    .agg(
        total_materials_distinct=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"),
        min_catalog_year=("CATALOG_YEAR", "min"),
        max_catalog_year=("CATALOG_YEAR", "max"),
        total_enrolled_students=("NUM_ENROLLED_STUDENTS", "sum"),
    )
    .reset_index()
)

# Final result mapping
result = {
    "instructor_materials_and_enrollment": agg_by_instructor_with_enroll
}