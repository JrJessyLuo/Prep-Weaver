import pandas as pd

faculty = tables["table_1"].copy()
lists = tables["table_5"].copy()
subjects = tables["table_6"].copy()

# Faculty members with last names beginning with Y
y_faculty = faculty[
    faculty["LAST_NAME"].astype(str).str.strip().str.upper().str.startswith("Y", na=False)
][["MIT_ID"]].drop_duplicates()

# Mailing-list memberships for those faculty
list_members = lists.copy()
list_members["MOIRA_LIST_MEMBER_MIT_ID"] = pd.to_numeric(
    list_members["MOIRA_LIST_MEMBER_MIT_ID"], errors="coerce"
).astype("Int64")

y_list_members = list_members.merge(
    y_faculty,
    left_on="MOIRA_LIST_MEMBER_MIT_ID",
    right_on="MIT_ID",
    how="inner"
)

# Subject counts managed by each faculty member
subjects["RESPONSIBLE_FACULTY_MIT_ID"] = pd.to_numeric(
    subjects["RESPONSIBLE_FACULTY_MIT_ID"], errors="coerce"
).astype("Int64")

subject_counts = (
    subjects.dropna(subset=["RESPONSIBLE_FACULTY_MIT_ID"])
    .drop_duplicates(["RESPONSIBLE_FACULTY_MIT_ID", "SUBJECT_OFFERED_SUMMARY_KEY"])
    .groupby("RESPONSIBLE_FACULTY_MIT_ID", as_index=False)
    .agg(subjects_managed=("SUBJECT_OFFERED_SUMMARY_KEY", "nunique"))
)

# Aggregate by mailing list
answer = (
    y_list_members[["MOIRA_LIST_KEY", "MOIRA_LIST_MEMBER_MIT_ID"]]
    .drop_duplicates()
    .merge(
        subject_counts,
        left_on="MOIRA_LIST_MEMBER_MIT_ID",
        right_on="RESPONSIBLE_FACULTY_MIT_ID",
        how="left"
    )
)

answer["subjects_managed"] = answer["subjects_managed"].fillna(0).astype(int)

answer = (
    answer.groupby("MOIRA_LIST_KEY", as_index=False)
    .agg(
        total_number_of_subjects_managed=("subjects_managed", "sum"),
        number_of_faculty_in_list=("MOIRA_LIST_MEMBER_MIT_ID", "nunique")
    )
    .rename(columns={"MOIRA_LIST_KEY": "email_list_name"})
    .sort_values("email_list_name")
    .reset_index(drop=True)
)

result = {
    "email_lists_for_y_faculty": answer
}
