import pandas as pd

students = tables["table_2"].copy()
departments = tables["table_4"].copy()

students["DEPARTMENT"] = students["DEPARTMENT"].astype(str).str.strip()
departments["SIS_ADMIN_DEPARTMENT_CODE"] = departments["SIS_ADMIN_DEPARTMENT_CODE"].astype(str).str.strip()

students["full_name_length"] = students["FULL_NAME"].astype("string").str.len()

student_stats = (
    students.groupby("DEPARTMENT", dropna=False)
    .agg(
        number_of_students=("FULL_NAME", "size"),
        longest_student_full_name_length=("full_name_length", "max"),
    )
    .reset_index()
)

out = departments.merge(
    student_stats,
    left_on="SIS_ADMIN_DEPARTMENT_CODE",
    right_on="DEPARTMENT",
    how="left",
)

out["number_of_students"] = out["number_of_students"].fillna(0).astype(int)
out["longest_student_full_name_length"] = out["longest_student_full_name_length"].fillna(0).astype(int)

out = out[
    [
        "SIS_ADMIN_DEPARTMENT_NAME",
        "department_phone_number",
        "number_of_students",
        "longest_student_full_name_length",
    ]
].rename(
    columns={
        "SIS_ADMIN_DEPARTMENT_NAME": "department_name",
        "department_phone_number": "department_phone_number",
    }
)

result = {"department_student_name_stats": out}
