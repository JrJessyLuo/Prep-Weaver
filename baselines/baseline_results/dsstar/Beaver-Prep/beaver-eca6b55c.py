import pandas as pd

# The input DataFrames are provided in a dict named `tables`
# tables['table_1'] -> LIBRARY_RESERVE_MATRL_DETAIL.pkl
# tables['table_3'] -> LIBRARY_COURSE_INSTRUCTOR.pkl
# tables['table_6'] -> LIBRARY_RESERVE_CATALOG.pkl

# Load from provided tables dict
matrl_detail = tables['table_1']
course_instr = tables['table_3']
reserve_catalog = tables['table_6']

# Minimal inspect to ensure join keys present (assertions as in reference logic)
assert "LIBRARY_COURSE_INSTRUCTOR_KEY" in matrl_detail.columns
assert "LIBRARY_RESERVE_CATALOG_KEY" in matrl_detail.columns
assert "LIBRARY_COURSE_INSTRUCTOR_KEY" in course_instr.columns
assert "library_reserve_catalog_key" in reserve_catalog.columns
assert "COURSE_NAME" in course_instr.columns
assert "CATALOG_YEAR" in reserve_catalog.columns

# Join detail -> course -> catalog
joined = (
    matrl_detail
    .merge(
        course_instr[["LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME"]],
        on="LIBRARY_COURSE_INSTRUCTOR_KEY",
        how="left",
        validate="m:1"
    )
    .merge(
        reserve_catalog[["library_reserve_catalog_key", "CATALOG_YEAR"]],
        left_on="LIBRARY_RESERVE_CATALOG_KEY",
        right_on="library_reserve_catalog_key",
        how="left",
        validate="m:1"
    )
)

# Aggregate per COURSE_NAME
agg_per_course = (
    joined
    .groupby("COURSE_NAME", dropna=False)
    .agg(
        materials_count=("LIBRARY_RESERVE_CATALOG_KEY", "count"),
        catalog_year_min=("CATALOG_YEAR", "min"),
        catalog_year_max=("CATALOG_YEAR", "max"),
        material_status_count=("LIBRARY_MATERIAL_STATUS_KEY", "count"),
        material_status_nunique=("LIBRARY_MATERIAL_STATUS_KEY", "nunique")
    )
    .reset_index()
    .sort_values(["materials_count", "COURSE_NAME"], ascending=[False, True])
)

# Prepare final result dict as required
result = {
    "library_materials_by_course_name": agg_per_course
}