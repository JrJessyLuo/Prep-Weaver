import pandas as pd

students = tables["table_1"].copy()

# Normalize department code for joins
students["DEPARTMENT_CODE"] = students["DEPARTMENT"].astype(str).str.strip()

# Build department/school lookup, preferring the fuller department table when available
dept_sources = []

if "table_4" in tables:
    d4 = tables["table_4"].copy()
    d4["DEPARTMENT_CODE"] = d4["DEPARTMENT_CODE"].astype(str).str.strip()
    dept_sources.append(
        d4[["DEPARTMENT_CODE", "DEPARTMENT_NAME", "SCHOOL_NAME"]]
        .dropna(subset=["DEPARTMENT_CODE"])
        .drop_duplicates(subset=["DEPARTMENT_CODE"], keep="first")
    )

if "table_2" in tables:
    d2 = tables["table_2"].copy()
    d2["DEPARTMENT_CODE"] = d2["DEPARTMENT_CODE"].astype(str).str.strip()
    dept_sources.append(
        d2[["DEPARTMENT_CODE", "DEPARTMENT_NAME", "SCHOOL_NAME"]]
        .dropna(subset=["DEPARTMENT_CODE"])
        .drop_duplicates(subset=["DEPARTMENT_CODE"], keep="first")
    )

dept_lookup = (
    pd.concat(dept_sources, ignore_index=True)
    .drop_duplicates(subset=["DEPARTMENT_CODE"], keep="first")
    if dept_sources
    else pd.DataFrame(columns=["DEPARTMENT_CODE", "DEPARTMENT_NAME", "SCHOOL_NAME"])
)

# Join all students to school metadata
students_enriched = students.merge(
    dept_lookup,
    on="DEPARTMENT_CODE",
    how="left",
    suffixes=("", "_LOOKUP")
)

students_enriched["FINAL_DEPARTMENT_NAME"] = students_enriched["DEPARTMENT_NAME_LOOKUP"].combine_first(
    students_enriched["DEPARTMENT_NAME"]
)

# Total student count per department and school
dept_school_counts = (
    students_enriched
    .groupby(["DEPARTMENT_CODE", "FINAL_DEPARTMENT_NAME", "SCHOOL_NAME"], dropna=False)
    .agg(total_student_count=("EMAIL_ADDRESS", "nunique"))
    .reset_index()
)

# Filter students with first name Kevin
kevin_students = students_enriched[
    students_enriched["FIRST_NAME"].astype(str).str.strip().str.casefold() == "kevin"
].copy()

# Add counts
kevin_students = kevin_students.merge(
    dept_school_counts,
    on=["DEPARTMENT_CODE", "FINAL_DEPARTMENT_NAME", "SCHOOL_NAME"],
    how="left"
)

# Final answer
out = kevin_students[
    [
        "FULL_NAME",
        "EMAIL_ADDRESS",
        "FINAL_DEPARTMENT_NAME",
        "OFFICE_PHONE",
        "SCHOOL_NAME",
        "total_student_count",
    ]
].rename(
    columns={
        "FULL_NAME": "full_name",
        "EMAIL_ADDRESS": "email_address",
        "FINAL_DEPARTMENT_NAME": "department_name",
        "OFFICE_PHONE": "department_phone_number",
        "SCHOOL_NAME": "school_name",
    }
).sort_values(
    ["full_name", "department_name", "school_name"],
    na_position="last"
).reset_index(drop=True)

result = {"kevin_students_department_school_info": out}
