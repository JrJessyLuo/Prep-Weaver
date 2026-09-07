import pandas as pd
import numpy as np

# Source tables from the provided `tables` dict
detail_df = tables['table_1'].copy()
instructor_df = tables['table_2'].copy()

# Ensure key columns are string for safe merge
detail_df["LIBRARY_COURSE_INSTRUCTOR_KEY"] = detail_df["LIBRARY_COURSE_INSTRUCTOR_KEY"].astype(str)
instructor_df["LIBRARY_COURSE_INSTRUCTOR_KEY"] = instructor_df["LIBRARY_COURSE_INSTRUCTOR_KEY"].astype(str)

# Select only necessary columns from instructor_df to avoid column bloat
instructor_cols = [
    "LIBRARY_COURSE_INSTRUCTOR_KEY",
    "COURSE_NAME",
    "INSTRUCTOR_NAME",
    "DEPARTMENT",
    "DATE_FROM",
    "DATE_TO",
    "UNIT_CODE",
    "UNIT",
    "WAREHOUSE_LOAD_DATE"
]
instructor_df_sel = instructor_df[instructor_cols].rename(columns={"WAREHOUSE_LOAD_DATE": "WAREHOUSE_LOAD_DATE_INSTRUCTOR"})

# Perform inner merge on key
merged_df = detail_df.merge(instructor_df_sel, on="LIBRARY_COURSE_INSTRUCTOR_KEY", how="inner")

# Create helper columns
merged_df["course_id"] = merged_df["SUBJECT_ID"].astype(str)

# Extract the first 4 digits of TERM_CODE as year; coerce to numeric
def extract_year(term_code):
    if pd.isna(term_code):
        return np.nan
    s = str(term_code)
    return pd.to_numeric(s[:4], errors="coerce")

merged_df["pub_year"] = merged_df["TERM_CODE"].apply(extract_year)

# Group by INSTRUCTOR_NAME and aggregate as specified
agg_df = (
    merged_df.groupby("INSTRUCTOR_NAME", dropna=False)
    .agg(
        n_unique_courses=("course_id", "nunique"),
        total_material_assignments=("LIBRARY_RESERVE_CATALOG_KEY", "count"),
        avg_publication_year=("pub_year", "mean"),
        n_distinct_status=("LIBRARY_MATERIAL_STATUS_KEY", "nunique"),
    )
    .reset_index()
)

# Sort by number of unique courses in descending order
agg_df_sorted = agg_df.sort_values(by="n_unique_courses", ascending=False)

# Assign final result to the required dict
result = {"instructor_materials_summary": agg_df_sorted}