import pandas as pd
import numpy as np

students = tables["table_2"].copy()
moira = tables["table_4"].copy()
dept_phone = tables["table_3"].copy()

# Normalize mailing-list member identifiers and student email usernames
moira["member_key"] = moira["moira_list_member"].astype(str).str.strip().str.upper()
students["member_key"] = (
    students["EMAIL_ADDRESS"]
    .astype(str)
    .str.split("@", n=1)
    .str[0]
    .str.strip()
    .str.upper()
)

# Filter to the requested mailing list
ocean_apple = moira[
    moira["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower().eq("ocean-apple")
].copy()

# Join mailing-list members to students
subscribed_students = ocean_apple.merge(
    students[["member_key", "EMAIL_ADDRESS", "DEPARTMENT", "DEPARTMENT_NAME"]],
    on="member_key",
    how="inner"
)

# Normalize department codes
subscribed_students["dept_code"] = subscribed_students["DEPARTMENT"].astype(str).str.strip()
dept_phone["dept_code"] = dept_phone["SIS_ADMIN_DEPARTMENT_CODE"].astype(str).str.strip()

# Count distinct subscribed students per department
dept_counts = (
    subscribed_students
    .drop_duplicates(subset=["member_key", "dept_code"])
    .groupby(["dept_code", "DEPARTMENT_NAME"], as_index=False)
    .agg(total_students=("member_key", "nunique"))
)

# Keep all departments tied for the highest count
max_count = dept_counts["total_students"].max() if not dept_counts.empty else 0
top_depts = dept_counts[dept_counts["total_students"].eq(max_count)].copy()

# Prepare department phone numbers
phones = dept_phone[["dept_code", "DEPARTMENT_PHONE_AREA_CODE", "department_phone_number"]].drop_duplicates("dept_code").copy()

def fmt_num(x):
    if pd.isna(x):
        return np.nan
    return str(int(float(x)))

phones["phone_number"] = phones.apply(
    lambda r: (
        fmt_num(r["DEPARTMENT_PHONE_AREA_CODE"]) + "-" + fmt_num(r["department_phone_number"])
        if pd.notna(r["DEPARTMENT_PHONE_AREA_CODE"])
        else fmt_num(r["department_phone_number"])
    ),
    axis=1
)

# Final answer
out = top_depts.merge(
    phones[["dept_code", "phone_number"]],
    on="dept_code",
    how="left"
)

out = (
    out[["DEPARTMENT_NAME", "phone_number", "total_students"]]
    .rename(columns={
        "DEPARTMENT_NAME": "department_name",
        "phone_number": "phone_number",
        "total_students": "total_students_subscribed"
    })
    .sort_values(["department_name"])
    .reset_index(drop=True)
)

result = {"ocean_apple_top_department_student_count": out}
