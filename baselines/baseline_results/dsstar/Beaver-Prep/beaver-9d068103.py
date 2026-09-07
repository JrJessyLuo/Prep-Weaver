import pandas as pd

# Access input tables from the provided `tables` dict
moira_df = tables['table_4']
student_df = tables['table_2']
dept_admin_df = tables['table_3']  # to get department phone numbers

# 1) Filter MOIRA members for the target list
filtered_members = moira_df[moira_df["MOIRA_LIST_KEY"] == "ocean-apple"].copy()

# 2) Prepare join keys:
def extract_kerb(email):
    if isinstance(email, str) and "@" in email:
        return email.split("@", 1)[0].strip().lower()
    return None

student_df = student_df.copy()
student_df["KERB_FROM_EMAIL"] = student_df["EMAIL_ADDRESS"].astype(str).str.strip().str.lower().map(extract_kerb)

filtered_members["moira_list_member_lc"] = filtered_members["moira_list_member"].astype(str).str.strip().str.lower()

# 3) Join on kerberos
merged = filtered_members.merge(
    student_df,
    left_on="moira_list_member_lc",
    right_on="KERB_FROM_EMAIL",
    how="left",
    suffixes=("_MOIRA", "_STUDENT")
)

# 4) Extract department names and count
dept_counts = (
    merged
    .dropna(subset=["DEPARTMENT_NAME"])
    .groupby("DEPARTMENT_NAME", dropna=False)
    .size()
    .reset_index(name="count")
)

# 5) Find the maximum count and keep only top departments
if not dept_counts.empty:
    max_count = dept_counts["count"].max()
    top_departments = dept_counts[dept_counts["count"] == max_count].copy()
else:
    top_departments = pd.DataFrame(columns=["DEPARTMENT_NAME", "count"])

# 6) Attach department phone numbers from SIS_ADMIN_DEPARTMENT if available
# Attempt to match on department name; keep phone if present
dept_admin_df_lc = dept_admin_df.copy()
if "DEPARTMENT_NAME" in dept_admin_df_lc.columns:
    dept_admin_df_lc["DEPARTMENT_NAME"] = dept_admin_df_lc["DEPARTMENT_NAME"].astype(str)
# Common phone column guess based on typical naming
phone_col_candidates = [c for c in dept_admin_df_lc.columns if "PHONE" in c.upper()]
phone_col = phone_col_candidates[0] if phone_col_candidates else None

if phone_col is not None:
    enriched = top_departments.merge(
        dept_admin_df_lc[["DEPARTMENT_NAME", phone_col]].drop_duplicates(),
        on="DEPARTMENT_NAME",
        how="left"
    ).rename(columns={phone_col: "PHONE_NUMBER"})
else:
    enriched = top_departments.copy()
    enriched["PHONE_NUMBER"] = pd.NA

# 7) Reorder columns
final_answer = enriched[["DEPARTMENT_NAME", "PHONE_NUMBER", "count"]].sort_values(
    by=["count", "DEPARTMENT_NAME"], ascending=[False, True]
).reset_index(drop=True)

# 8) Package result
result = {
    "top_departments_ocean_apple": final_answer
}