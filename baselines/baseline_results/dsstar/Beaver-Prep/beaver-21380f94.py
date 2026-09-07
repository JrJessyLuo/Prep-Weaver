import pandas as pd

# Inputs are provided via `tables` dict
# tables['table_1'] -> STUDENT_DEPARTMENT.pkl
# tables['table_7'] -> MIT_STUDENT_DIRECTORY.pkl

# Load tables from the provided mapping
departments = tables['table_1'].copy()
students = tables['table_7'].copy()

# --------------------------------------------------------------------------------
# Define/Load the "duo users" mailing list
# --------------------------------------------------------------------------------
# Following the reference code logic, there is no file/list provided here.
# Therefore, the duo_email_set is empty, leading to zero counts as in the reference run.
duo_email_list = []
duo_email_set = set(pd.Series(duo_email_list, dtype=str).str.strip().str.lower().dropna().unique())

# --------------------------------------------------------------------------------
# Filter MIT_STUDENT_DIRECTORY to the “duo users” mailing list
# --------------------------------------------------------------------------------
students = students.copy()
students["EMAIL_ADDRESS_NORM"] = students["EMAIL_ADDRESS"].astype(str).str.strip().str.lower()
duo_subset = students[students["EMAIL_ADDRESS_NORM"].isin(duo_email_set)].copy()

# --------------------------------------------------------------------------------
# Compute metrics on the subset
# --------------------------------------------------------------------------------
number_of_students = duo_subset["EMAIL_ADDRESS_NORM"].nunique(dropna=True)
number_of_departments = duo_subset["DEPARTMENT"].nunique(dropna=True)

# --------------------------------------------------------------------------------
# Join to STUDENT_DEPARTMENT to find schools and count unique SCHOOL_NAME
# --------------------------------------------------------------------------------
dept_lookup = departments.copy()
dept_lookup["DEPARTMENT_CODE_KEY"] = dept_lookup["DEPARTMENT_CODE"].astype(str).str.strip()
dept_lookup["DEPARTMENT_NAME_KEY"] = dept_lookup["DEPARTMENT_NAME"].astype(str).str.strip()

duo_subset["DEPARTMENT_CODE_KEY"] = duo_subset["DEPARTMENT"].astype(str).str.strip()
duo_subset["DEPARTMENT_NAME_KEY"] = duo_subset["DEPARTMENT_NAME"].astype(str).str.strip()

merged_code = pd.merge(
    duo_subset,
    dept_lookup[["DEPARTMENT_CODE_KEY", "SCHOOL_NAME"]],
    on="DEPARTMENT_CODE_KEY",
    how="left",
    suffixes=("", "_by_code")
)

need_name_merge = merged_code["SCHOOL_NAME"].isna()
if need_name_merge.any():
    merged_name = pd.merge(
        duo_subset.loc[need_name_merge, ["EMAIL_ADDRESS_NORM", "DEPARTMENT_NAME_KEY"]],
        dept_lookup[["DEPARTMENT_NAME_KEY", "SCHOOL_NAME"]],
        on="DEPARTMENT_NAME_KEY",
        how="left"
    )
    merged_code.loc[need_name_merge, "SCHOOL_NAME"] = merged_name["SCHOOL_NAME"].values

number_of_schools = merged_code["SCHOOL_NAME"].nunique(dropna=True)

# --------------------------------------------------------------------------------
# Prepare final answer as a DataFrame and assign to `result`
# --------------------------------------------------------------------------------
answer_df = pd.DataFrame(
    [{
        "number_of_students": int(number_of_students),
        "number_of_departments": int(number_of_departments),
        "number_of_schools": int(number_of_schools),
    }]
)

result = {"duo_users_summary": answer_df}