import pandas as pd

# Source tables
courses = tables["table_1"].copy()
catalog_links = tables["table_6"].copy()

# Normalize join keys
courses["course_key"] = (
    courses["LIBRARY_SUBJECT_OFFERED_KEY"]
    .astype(str)
    .str.strip()
    .str.upper()
)

catalog_links["course_key"] = (
    catalog_links["LIBRARY_SUBJECT_OFFERED_KEY"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# One row per library course offering, carrying department and enrollment
course_level = (
    courses
    .assign(
        department_name=courses["OFFER_DEPT_NAME"].astype(str).str.strip(),
        enrollment=pd.to_numeric(courses["NUM_ENROLLED_STUDENTS"], errors="coerce")
    )
    .groupby("course_key", as_index=False)
    .agg(
        department_name=("department_name", "first"),
        enrollment=("enrollment", "first")
    )
)

# Count catalog items associated with each course offering
catalog_counts = (
    catalog_links
    .dropna(subset=["LIBRARY_RESERVE_CATALOG_KEY"])
    .groupby("course_key", as_index=False)
    .agg(catalog_items=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"))
)

# Keep courses that have at least one associated catalog item
course_level = (
    course_level
    .merge(catalog_counts, on="course_key", how="inner")
)

# Department-level summary
dept_summary = (
    course_level
    .groupby("department_name", as_index=False)
    .agg(
        total_number_of_courses_using_library_materials=("course_key", "nunique"),
        number_of_catalog_items_associated_with_those_courses=("catalog_items", "sum"),
        average_enrollment_per_course=("enrollment", "mean")
    )
    .sort_values("department_name")
    .reset_index(drop=True)
)

# Grand total row
grand_total = pd.DataFrame([{
    "department_name": "Grand Total",
    "total_number_of_courses_using_library_materials": course_level["course_key"].nunique(),
    "number_of_catalog_items_associated_with_those_courses": course_level["catalog_items"].sum(),
    "average_enrollment_per_course": course_level["enrollment"].mean()
}])

final_answer = pd.concat([dept_summary, grand_total], ignore_index=True)

result = {
    "department_library_materials_summary": final_answer
}
