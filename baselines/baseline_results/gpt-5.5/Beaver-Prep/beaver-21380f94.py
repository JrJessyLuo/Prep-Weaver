import pandas as pd

students = tables["table_7"].copy()
departments = tables["table_1"].copy()

# Normalize department codes for joining
students["DEPARTMENT_NORM"] = students["DEPARTMENT"].astype(str).str.strip()
departments["DEPARTMENT_CODE_NORM"] = departments["DEPARTMENT_CODE"].astype(str).str.strip()

students_with_school = students.merge(
    departments[["DEPARTMENT_CODE_NORM", "SCHOOL_NAME"]],
    left_on="DEPARTMENT_NORM",
    right_on="DEPARTMENT_CODE_NORM",
    how="left"
)

summary = pd.DataFrame([{
    "number_of_students": students_with_school["EMAIL_ADDRESS"].nunique(),
    "number_of_departments": students_with_school["DEPARTMENT_NORM"].nunique(),
    "number_of_schools": students_with_school["SCHOOL_NAME"].nunique()
}])

result = {
    "duo_users_mailing_list_summary": summary
}
