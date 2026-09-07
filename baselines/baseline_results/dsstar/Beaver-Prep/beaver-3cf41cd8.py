import pandas as pd

# Access input tables from the provided `tables` dict
lib_df = tables['table_1']        # LIBRARY_SUBJECT_OFFERED.pkl
tip_df = tables['table_9']        # TIP_DETAIL.pkl

# Key columns for grouping/output
group_dims = ["OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME", "COURSE_NUMBER", "SUBJECT_TITLE", "term_code"]

# 1) Determine current term (max term_code)
current_term = lib_df["term_code"].dropna().max()

# 2) Filter library data to current term
lib_cur = lib_df.loc[lib_df["term_code"] == current_term].copy()

# 3) Prepare TIP_DETAIL for join: keep current term rows with non-null ISBNs
tip_cur = tip_df.copy()
tip_cur = tip_cur.rename(columns={"subject_id": "SUBJECT_ID", "TERM_CODE": "term_code"})
tip_cur = tip_cur.loc[(tip_cur["term_code"] == current_term) & (tip_cur["ISBN"].notna())]

# 4) Build mapping from library groups to SUBJECT_IDs for the current term
lib_keys = lib_cur[group_dims + ["SUBJECT_ID"]].drop_duplicates()

# 5) Join to TIP ISBNs and compute distinct ISBNs per group
tip_isbn_for_groups = lib_keys.merge(
    tip_cur[["term_code", "SUBJECT_ID", "ISBN"]].drop_duplicates(),
    on=["term_code", "SUBJECT_ID"],
    how="left",
)

group_isbn = (
    tip_isbn_for_groups.groupby(group_dims)["ISBN"]
    .nunique(dropna=True)
    .reset_index(name="distinct_isbn_count")
)

# 6) Compute total enrolled students per group
group_students = (
    lib_cur.groupby(group_dims, as_index=False)["NUM_ENROLLED_STUDENTS"]
    .sum()
    .rename(columns={"NUM_ENROLLED_STUDENTS": "total_enrolled_students"})
)

# 7) Combine aggregates
result_df = group_students.merge(group_isbn, on=group_dims, how="left")
result_df["distinct_isbn_count"] = result_df["distinct_isbn_count"].fillna(0).astype(int)

# 8) Create the required summary row:
#    ('TOTAL:', null, null, null, total number of students, null, number of distinct catalog ISBNs)
term_distinct_isbn = tip_cur["ISBN"].nunique(dropna=True)
term_total_students = result_df["total_enrolled_students"].sum()

summary_row = {
    "OFFER_DEPT_NAME": "TOTAL:",
    "OFFER_SCHOOL_NAME": pd.NA,
    "COURSE_NUMBER": pd.NA,
    "SUBJECT_TITLE": pd.NA,
    "total_enrolled_students": term_total_students,
    "term_code": pd.NA,
    "distinct_isbn_count": int(term_distinct_isbn),
}

# 9) Arrange columns as requested and append summary
result_df = result_df[[
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "COURSE_NUMBER",
    "SUBJECT_TITLE",
    "total_enrolled_students",
    "term_code",
    "distinct_isbn_count",
]]

result_with_summary = pd.concat(
    [result_df, pd.DataFrame([summary_row])],
    ignore_index=True
)

# 10) Assign to output variable `result`
result = {"library_isbn_summary": result_with_summary}