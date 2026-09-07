import pandas as pd

# Access input tables from the provided `tables` dict
moira_list = tables['table_1']
moira_list_detail = tables['table_2']
student_dir = tables['table_5']

# =========================
# Subscriber counts per list
# =========================
subscriber_counts = (
    moira_list_detail
    .groupby("MOIRA_LIST_KEY", as_index=False)
    .size()
    .rename(columns={"size": "SUBSCRIBER_COUNT"})
)

base = (
    moira_list[["MOIRA_LIST_KEY", "MOIRA_LIST_NAME", "IS_PUBLIC"]]
    .merge(subscriber_counts, on="MOIRA_LIST_KEY", how="left")
    .fillna({"SUBSCRIBER_COUNT": 0})
)

base["SUBSCRIBER_COUNT"] = base["SUBSCRIBER_COUNT"].astype(int)

# =========================
# Match list members to student directory by email (case-insensitive)
# and compute top department per list
# =========================
mld = moira_list_detail.copy()
std = student_dir.copy()

mld["moira_list_member_lc"] = mld["moira_list_member"].astype(str).str.strip().str.lower()
std["EMAIL_ADDRESS_lc"] = std["EMAIL_ADDRESS"].astype(str).str.strip().str.lower()

mld_std = mld.merge(
    std[["EMAIL_ADDRESS_lc", "DEPARTMENT_NAME"]],
    left_on="moira_list_member_lc",
    right_on="EMAIL_ADDRESS_lc",
    how="inner"
).drop(columns=["EMAIL_ADDRESS_lc"])

mld_std["DEPARTMENT_NAME"] = mld_std["DEPARTMENT_NAME"].fillna("Unknown")

dept_counts = (
    mld_std.groupby(["MOIRA_LIST_KEY", "DEPARTMENT_NAME"], as_index=False)
    .size()
    .rename(columns={"size": "DEPT_STUDENT_COUNT"})
)

dept_counts_sorted = dept_counts.sort_values(
    by=["MOIRA_LIST_KEY", "DEPT_STUDENT_COUNT", "DEPARTMENT_NAME"],
    ascending=[True, False, True]
)

top_dept_per_list = dept_counts_sorted.groupby("MOIRA_LIST_KEY", as_index=False).first()
top_dept_per_list = top_dept_per_list.rename(
    columns={
        "DEPARTMENT_NAME": "TOP_DEPARTMENT_NAME",
        "DEPT_STUDENT_COUNT": "TOP_DEPARTMENT_STUDENT_COUNT"
    }
)

# =========================
# Merge top department info, then select top 100 lists by subscribers
# =========================
final = (
    base.merge(top_dept_per_list, on="MOIRA_LIST_KEY", how="left")
    .sort_values(by=["SUBSCRIBER_COUNT", "MOIRA_LIST_NAME"], ascending=[False, True])
    .head(100)
    [["MOIRA_LIST_NAME", "SUBSCRIBER_COUNT", "IS_PUBLIC", "TOP_DEPARTMENT_NAME", "TOP_DEPARTMENT_STUDENT_COUNT"]]
)

# Package the final answer
result = {
    "top_100_lists_with_top_department": final
}