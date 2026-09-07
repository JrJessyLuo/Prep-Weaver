import pandas as pd
import numpy as np

# Source tables
lists = tables["table_1"].copy()
members = tables["table_2"].copy()
students = tables["table_5"].copy()

# Normalize list keys/names
lists["list_key_norm"] = lists["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()
lists["list_name_norm"] = lists["MOIRA_LIST_NAME"].astype(str).str.strip().str.lower()
members["list_key_norm"] = members["MOIRA_LIST_KEY"].astype(str).str.strip().str.lower()

# Keep Moira mailing/email lists
email_lists = lists[
    lists["IS_MOIRA_MAILING_LIST"].astype(str).str.strip().str.upper().eq("Y")
].copy()

# Count total subscribers per mailing list
subscriber_counts = (
    members.merge(
        email_lists[["list_key_norm", "MOIRA_LIST_NAME", "IS_PUBLIC"]],
        on="list_key_norm",
        how="inner"
    )
    .assign(_subscriber_counter=lambda d: pd.to_numeric(d["COUNTER"], errors="coerce").fillna(1))
    .groupby(["list_key_norm", "MOIRA_LIST_NAME", "IS_PUBLIC"], as_index=False)
    .agg(total_number_of_subscribers=("_subscriber_counter", "sum"))
)

# Top 100 lists by total subscribers
top_100_lists = (
    subscriber_counts
    .sort_values(
        ["total_number_of_subscribers", "MOIRA_LIST_NAME"],
        ascending=[False, True]
    )
    .head(100)
    .copy()
)

# Normalize member/student identifiers for matching list members to students
members_top = members.merge(
    top_100_lists[["list_key_norm"]],
    on="list_key_norm",
    how="inner"
).copy()
members_top["member_kerberos"] = members_top["moira_list_member"].astype(str).str.strip().str.upper()

students["student_kerberos"] = (
    students["EMAIL_ADDRESS"]
    .astype(str)
    .str.split("@", n=1)
    .str[0]
    .str.strip()
    .str.upper()
)

students_small = (
    students[["student_kerberos", "DEPARTMENT_NAME"]]
    .dropna(subset=["student_kerberos", "DEPARTMENT_NAME"])
    .drop_duplicates()
)

# Count students by department within each top list
student_dept_counts = (
    members_top[["list_key_norm", "member_kerberos"]]
    .drop_duplicates()
    .merge(
        students_small,
        left_on="member_kerberos",
        right_on="student_kerberos",
        how="inner"
    )
    .groupby(["list_key_norm", "DEPARTMENT_NAME"], as_index=False)
    .agg(number_of_students_from_department=("member_kerberos", "nunique"))
)

# Department with the most student presence per list
top_dept_per_list = (
    student_dept_counts
    .sort_values(
        ["list_key_norm", "number_of_students_from_department", "DEPARTMENT_NAME"],
        ascending=[True, False, True]
    )
    .drop_duplicates("list_key_norm", keep="first")
    .rename(columns={"DEPARTMENT_NAME": "department_with_most_presence"})
)

# Final answer
answer = (
    top_100_lists
    .merge(top_dept_per_list, on="list_key_norm", how="left")
    .rename(columns={
        "MOIRA_LIST_NAME": "list_name",
        "IS_PUBLIC": "public_status"
    })
    [[
        "list_name",
        "total_number_of_subscribers",
        "public_status",
        "department_with_most_presence",
        "number_of_students_from_department"
    ]]
    .reset_index(drop=True)
)

result = {"top_100_email_lists_by_subscribers": answer}
