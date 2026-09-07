import pandas as pd
import numpy as np
import re

offers = tables["table_3"].copy()
materials = tables["table_9"].copy()

def clean_str(s):
    return s.astype("string").str.strip()

def term_rank(term):
    term = str(term).strip().upper()
    m = re.match(r"^(\d{4})([A-Z]+)$", term)
    if not m:
        return (-1, -1, term)
    year = int(m.group(1))
    term_part = m.group(2)
    term_order = {"JA": 1, "IAP": 1, "WI": 1, "SP": 2, "SU": 3, "FA": 4}
    return (year, term_order.get(term_part, 0), term)

# Normalize term/subject fields
offers["TERM_CODE_CLEAN"] = clean_str(offers["TERM_CODE"]).str.upper()
offers["SUBJECT_ID_CLEAN"] = clean_str(offers["SUBJECT_ID"]).str.upper()

materials["TERM_CODE_CLEAN"] = clean_str(materials["TERM_CODE"]).str.upper()
materials["SUBJECT_ID_CLEAN"] = clean_str(materials["subject_id"]).str.upper()
materials["ISBN_CLEAN"] = clean_str(materials["ISBN"])
materials.loc[materials["ISBN_CLEAN"].isin(["", "nan", "None", "<NA>"]), "ISBN_CLEAN"] = pd.NA

# Infer current term as the latest term available in the TIP subject-offered data
terms = offers["TERM_CODE_CLEAN"].dropna().unique().tolist()
current_term = max(terms, key=term_rank)

current_offers = offers[offers["TERM_CODE_CLEAN"] == current_term].copy()

# Avoid double-counting offered subjects if duplicated
if "TIP_SUBJECT_OFFERED_KEY" in current_offers.columns:
    current_offers["TIP_SUBJECT_OFFERED_KEY_CLEAN"] = clean_str(current_offers["TIP_SUBJECT_OFFERED_KEY"])
    dedup_keys = ["TIP_SUBJECT_OFFERED_KEY_CLEAN"]
else:
    dedup_keys = ["TERM_CODE_CLEAN", "SUBJECT_ID_CLEAN"]

current_offers = current_offers.drop_duplicates(subset=dedup_keys)

# Final grouping fields
group_cols = [
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "COURSE_NUMBER",
    "SUBJECT_TITLE",
    "TERM_CODE_CLEAN",
]

# Total enrolled students by displayed course row
enrollment_by_course = (
    current_offers
    .groupby(group_cols, dropna=False, as_index=False)
    .agg(total_enrolled_students=("NUM_ENROLLED_STUDENTS", "sum"))
)

# Count distinct ISBNs by displayed course row
current_materials = materials[
    (materials["TERM_CODE_CLEAN"] == current_term) &
    (materials["ISBN_CLEAN"].notna())
].copy()

isbn_join = current_offers[group_cols + ["SUBJECT_ID_CLEAN"]].merge(
    current_materials[["TERM_CODE_CLEAN", "SUBJECT_ID_CLEAN", "ISBN_CLEAN"]],
    on=["TERM_CODE_CLEAN", "SUBJECT_ID_CLEAN"],
    how="left"
)

isbn_by_course = (
    isbn_join
    .groupby(group_cols, dropna=False, as_index=False)
    .agg(distinct_catalog_isbns=("ISBN_CLEAN", "nunique"))
)

out = enrollment_by_course.merge(
    isbn_by_course,
    on=group_cols,
    how="left"
)

out["distinct_catalog_isbns"] = out["distinct_catalog_isbns"].fillna(0).astype(int)

out = out.rename(columns={
    "OFFER_DEPT_NAME": "department",
    "OFFER_SCHOOL_NAME": "school",
    "COURSE_NUMBER": "course_number",
    "SUBJECT_TITLE": "subject_title",
    "TERM_CODE_CLEAN": "term_code",
})

out = out[
    [
        "department",
        "school",
        "course_number",
        "subject_title",
        "total_enrolled_students",
        "term_code",
        "distinct_catalog_isbns",
    ]
].sort_values(
    ["department", "school", "course_number", "subject_title"],
    na_position="last"
).reset_index(drop=True)

summary_row = pd.DataFrame([{
    "department": "TOTAL:",
    "school": pd.NA,
    "course_number": pd.NA,
    "subject_title": pd.NA,
    "total_enrolled_students": int(current_offers["NUM_ENROLLED_STUDENTS"].sum()),
    "term_code": pd.NA,
    "distinct_catalog_isbns": int(current_materials["ISBN_CLEAN"].nunique()),
}])

final_table = pd.concat([out, summary_row], ignore_index=True)

result = {"current_term_course_isbn_summary": final_table}
