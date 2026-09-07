import pandas as pd

# Access input tables from the provided `tables` dict
student_df = tables['table_1']
stud_dept_df = tables['table_2']

# Ensure required columns exist
expected_cols = {"FIRST_NAME", "FULL_NAME", "EMAIL_ADDRESS", "DEPARTMENT", "DEPARTMENT_NAME"}
missing = expected_cols - set(student_df.columns)
if missing:
    raise ValueError(f"Missing expected columns in MIT_STUDENT_DIRECTORY: {missing}")

dept_expected_cols = {
    "DEPARTMENT_CODE",
    "DEPARTMENT_NAME",
    "DEPARTMENT_FULL_NAME",
    "SCHOOL_CODE",
    "SCHOOL_NAME",
}
missing_dept = dept_expected_cols - set(stud_dept_df.columns)
if missing_dept:
    raise ValueError(f"Missing expected columns in STUDENT_DEPARTMENT: {missing_dept}")

# Additional optional column for department phone, if present
dept_phone_col = "DEPARTMENT_PHONE"
has_dept_phone = dept_phone_col in stud_dept_df.columns

# Filter students with first name "Kevin" (case-insensitive)
mask = student_df["FIRST_NAME"].astype(str).str.casefold() == "kevin".casefold()
kevin_students = student_df.loc[
    mask, ["FULL_NAME", "EMAIL_ADDRESS", "DEPARTMENT", "DEPARTMENT_NAME"]
].copy()

# Join Kevin records to department info
dept_cols = ["DEPARTMENT_CODE", "DEPARTMENT_FULL_NAME", "SCHOOL_NAME", "SCHOOL_CODE"]
if has_dept_phone:
    dept_cols.append(dept_phone_col)

kevin_with_dept = kevin_students.merge(
    stud_dept_df[dept_cols],
    left_on="DEPARTMENT",
    right_on="DEPARTMENT_CODE",
    how="left"
)

# Compute total student counts per department and per school from the full student directory
# Normalize case for robust grouping
stud_dept_counts = (
    student_df
    .assign(
        DEPARTMENT=student_df["DEPARTMENT"].astype(str),
        SCHOOL_CODE=None  # placeholder; school aggregation will use mapping below
    )
)

# Map department -> school via STUDENT_DEPARTMENT to aggregate students by school
dept_to_school = stud_dept_df[["DEPARTMENT_CODE", "SCHOOL_CODE", "SCHOOL_NAME"]].drop_duplicates()
stud_dept_counts = stud_dept_counts.merge(
    dept_to_school,
    left_on="DEPARTMENT",
    right_on="DEPARTMENT_CODE",
    how="left"
)

dept_counts = (
    stud_dept_counts.groupby("DEPARTMENT", dropna=False)
    .size()
    .rename("TOTAL_STUDENTS_IN_DEPARTMENT")
    .reset_index()
)

school_counts = (
    stud_dept_counts.groupby("SCHOOL_CODE", dropna=False)
    .size()
    .rename("TOTAL_STUDENTS_IN_SCHOOL")
    .reset_index()
)

# Merge counts back onto Kevin rows
out = kevin_with_dept.merge(
    dept_counts, on="DEPARTMENT", how="left"
).merge(
    school_counts, on="SCHOOL_CODE", how="left"
)

# Select and order final columns
final_cols = [
    "FULL_NAME",
    "EMAIL_ADDRESS",
    "DEPARTMENT_NAME",
]
if has_dept_phone:
    final_cols.append(dept_phone_col)
final_cols += [
    "SCHOOL_NAME",
    "TOTAL_STUDENTS_IN_DEPARTMENT",
    "TOTAL_STUDENTS_IN_SCHOOL",
]

final = out[final_cols].copy()

# Assign final result to required mapping
result = {"kevin_students_details": final}