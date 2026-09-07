import pandas as pd
import numpy as np

# The input DataFrames are provided in a dict named `tables`
# tables['table_1'] -> SUBJECT_GROUPING.pkl
# tables['table_5'] -> SUBJECT_OFFERED_SUMMARY.pkl
# tables['table_7'] -> SIS_COURSE_DESCRIPTION.pkl

# 1) Load DataFrames from `tables`
df = tables['table_5'].copy()  # SUBJECT_OFFERED_SUMMARY
sg = tables['table_1'].copy()  # SUBJECT_GROUPING
sis_desc = tables['table_7'].copy()  # SIS_COURSE_DESCRIPTION

# Keep only columns we will use
needed_cols = [
    "TERM_CODE",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "SUBJECT_ID",
    "MASTER_SUBJECT_ID",
]
missing = [c for c in needed_cols if c not in df.columns]
if missing:
    raise ValueError(f"Required columns missing from SUBJECT_OFFERED_SUMMARY: {missing}")

# 2) Build distinct subject counts and equivalent groups counts

# Distinct subjects per TERM_CODE + OFFER_DEPT_CODE
distinct_subjects_per_term_dept = (
    df.dropna(subset=["TERM_CODE", "OFFER_DEPT_CODE", "SUBJECT_ID"])
      .groupby(["TERM_CODE", "OFFER_DEPT_CODE"], as_index=False)["SUBJECT_ID"]
      .nunique()
      .rename(columns={"SUBJECT_ID": "num_distinct_subjects"})
)

# Equivalent subject groups per TERM_CODE + OFFER_DEPT_CODE
work = df.copy()
work["EQUIV_GROUP_ID"] = work["MASTER_SUBJECT_ID"].where(
    work["MASTER_SUBJECT_ID"].notna(), work["SUBJECT_ID"]
)

equiv_groups_per_term_dept = (
    work.dropna(subset=["TERM_CODE", "OFFER_DEPT_CODE", "EQUIV_GROUP_ID"])
        .groupby(["TERM_CODE", "OFFER_DEPT_CODE"], as_index=False)["EQUIV_GROUP_ID"]
        .nunique()
        .rename(columns={"EQUIV_GROUP_ID": "num_equiv_groups"})
)

# Merge distinct vs. equivalent summaries
summary = pd.merge(
    distinct_subjects_per_term_dept,
    equiv_groups_per_term_dept,
    on=["TERM_CODE", "OFFER_DEPT_CODE"],
    how="outer",
)

# Add department name if available for readability (pick any representative)
if "OFFER_DEPT_NAME" in df.columns:
    dept_names = (
        df.dropna(subset=["OFFER_DEPT_CODE", "OFFER_DEPT_NAME"])
          .drop_duplicates(subset=["OFFER_DEPT_CODE"])
          .loc[:, ["OFFER_DEPT_CODE", "OFFER_DEPT_NAME"]]
    )
    summary = summary.merge(dept_names, on="OFFER_DEPT_CODE", how="left")

# 3) Map SCHOOL_NAME by (TERM_CODE, OFFER_DEPT_CODE) from SUBJECT_GROUPING
for col in ["TERM_CODE", "DEPARTMENT_CODE", "SCHOOL_NAME"]:
    if col not in sg.columns:
        raise ValueError(f"Column {col} missing from SUBJECT_GROUPING.pkl")
sg_small = sg.loc[:, ["TERM_CODE", "DEPARTMENT_CODE", "SCHOOL_NAME"]].drop_duplicates()
summary = summary.merge(
    sg_small,
    left_on=["TERM_CODE", "OFFER_DEPT_CODE"],
    right_on=["TERM_CODE", "DEPARTMENT_CODE"],
    how="left"
).drop(columns=["DEPARTMENT_CODE"])

# 4) Extract DEPARTMENT_CODE -> phone mapping from SIS_COURSE_DESCRIPTION
cand_code_cols = [c for c in sis_desc.columns if c.upper() in ("DEPARTMENT", "DEPARTMENT_CODE")]
cand_phone_cols = [c for c in sis_desc.columns if "PHONE" in c.upper()]
if cand_code_cols and cand_phone_cols:
    code_col = cand_code_cols[0]
    phone_col = cand_phone_cols[0]
    dept_phone_map = (
        sis_desc.loc[:, [code_col, phone_col]]
                .rename(columns={code_col: "DEPARTMENT_CODE", phone_col: "DEPARTMENT_PHONE"})
                .dropna(subset=["DEPARTMENT_CODE"])
                .drop_duplicates(subset=["DEPARTMENT_CODE"])
    )
else:
    dept_phone_map = pd.DataFrame(columns=["DEPARTMENT_CODE", "DEPARTMENT_PHONE"])

# Merge phone, if we have any
if not dept_phone_map.empty:
    summary = summary.merge(
        dept_phone_map,
        left_on="OFFER_DEPT_CODE",
        right_on="DEPARTMENT_CODE",
        how="left"
    ).drop(columns=["DEPARTMENT_CODE"])
else:
    summary["DEPARTMENT_PHONE"] = pd.NA

# 5) Calculate average number of equivalent subjects
summary["avg_equiv_per_subject"] = summary["num_equiv_groups"] / summary["num_distinct_subjects"]
summary.loc[
    summary["num_distinct_subjects"].isna() | (summary["num_distinct_subjects"] == 0),
    "avg_equiv_per_subject"
] = np.nan

# 6) Append per-term SUBTOTAL rows and an overall TOTAL row
def build_subtotals(df_in: pd.DataFrame) -> pd.DataFrame:
    base_cols = [
        "TERM_CODE",
        "OFFER_DEPT_CODE",
        "OFFER_DEPT_NAME",
        "num_distinct_subjects",
        "num_equiv_groups",
        "SCHOOL_NAME",
        "DEPARTMENT_PHONE",
        "avg_equiv_per_subject",
    ]
    tmp = df_in.copy()
    for c in ["num_distinct_subjects", "num_equiv_groups"]:
        tmp[c] = pd.to_numeric(tmp[c], errors="coerce")

    per_term = (
        tmp.groupby("TERM_CODE", as_index=False)[["num_distinct_subjects", "num_equiv_groups"]]
           .sum(min_count=1)
    )
    per_term["OFFER_DEPT_CODE"] = "SUBTOTAL"
    per_term["OFFER_DEPT_NAME"] = "SUBTOTAL"
    per_term["SCHOOL_NAME"] = pd.NA
    per_term["DEPARTMENT_PHONE"] = pd.NA
    per_term["avg_equiv_per_subject"] = per_term["num_equiv_groups"] / per_term["num_distinct_subjects"]
    per_term.loc[
        per_term["num_distinct_subjects"].isna() | (per_term["num_distinct_subjects"] == 0),
        "avg_equiv_per_subject"
    ] = np.nan
    per_term = per_term.loc[:, base_cols]

    grand = (
        tmp.agg(
            {
                "num_distinct_subjects": "sum",
                "num_equiv_groups": "sum"
            }
        ).to_frame().T
    )
    grand["TERM_CODE"] = "TOTAL"
    grand["OFFER_DEPT_CODE"] = "TOTAL"
    grand["OFFER_DEPT_NAME"] = "TOTAL"
    grand["SCHOOL_NAME"] = pd.NA
    grand["DEPARTMENT_PHONE"] = pd.NA
    grand["avg_equiv_per_subject"] = grand["num_equiv_groups"] / grand["num_distinct_subjects"]
    grand.loc[
        grand["num_distinct_subjects"].isna() | (grand["num_distinct_subjects"] == 0),
        "avg_equiv_per_subject"
    ] = np.nan
    grand = grand.loc[:, base_cols]

    return per_term, grand

detail_cols = [
    "TERM_CODE",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "num_distinct_subjects",
    "num_equiv_groups",
    "SCHOOL_NAME",
    "DEPARTMENT_PHONE",
    "avg_equiv_per_subject",
]
detail = summary.loc[:, detail_cols].copy()

per_term_subtotals, grand_total = build_subtotals(detail)
final_with_totals = pd.concat([detail, per_term_subtotals, grand_total], ignore_index=True)

# 7) Sort by TERM_CODE and OFFER_DEPT_NAME with term suppression for repeated values
def term_sort_key(term):
    if pd.isna(term):
        return ("", 0)
    if term == "TOTAL":
        return ("ZZZZZZZZ", 1)
    return (str(term), 0)

final_with_totals["_TERM_SORT"] = final_with_totals["TERM_CODE"].apply(term_sort_key)
final_sorted = final_with_totals.sort_values(
    by=["_TERM_SORT", "OFFER_DEPT_NAME", "OFFER_DEPT_CODE"], kind="mergesort"
).drop(columns=["_TERM_SORT"]).reset_index(drop=True)

# Suppress TERM_CODE repeats (except for 'TOTAL')
suppressed = final_sorted.copy()
term_col = suppressed["TERM_CODE"]
suppressed_terms = []
prev_term = None
for t in term_col:
    if t == "TOTAL":
        suppressed_terms.append(t)
        prev_term = t
        continue
    if t == prev_term:
        suppressed_terms.append("")
    else:
        suppressed_terms.append(t)
        prev_term = t
suppressed["TERM_CODE"] = suppressed_terms

# Select and rename columns to match the question phrasing if needed
# - TERM_CODE (with suppression), OFFER_DEPT_CODE (department),
# - num_distinct_subjects (number of courses),
# - avg_equiv_per_subject,
# - SCHOOL_NAME,
# - DEPARTMENT_PHONE
answer_cols = [
    "TERM_CODE",
    "OFFER_DEPT_CODE",
    "num_distinct_subjects",
    "avg_equiv_per_subject",
    "SCHOOL_NAME",
    "DEPARTMENT_PHONE",
]
answer = suppressed.loc[:, answer_cols].rename(columns={
    "OFFER_DEPT_CODE": "DEPARTMENT",
    "num_distinct_subjects": "num_courses"
})

# Assign final result mapping
result = {"term_dept_course_equiv_with_school_phone_subtotals": answer}