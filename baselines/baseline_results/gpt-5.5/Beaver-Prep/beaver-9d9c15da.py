import pandas as pd
import numpy as np

# Source tables
course_summary = tables["table_3"].copy()
tip_subjects = tables["table_2"].copy()
tip_assoc = tables["table_1"].copy()
materials = tables["table_4"].copy()

def clean_str(s):
    return s.astype("string").str.strip()

def first_non_null(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else pd.NA

# -----------------------------
# Course / enrollment base
# -----------------------------
for df, cols in [
    (course_summary, ["TERM_CODE", "SUBJECT_ID", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME",
                      "SUBJECT_TITLE", "CLUSTER_TYPE", "CLUSTER_TYPE_DESC",
                      "HGN_CODE", "HGN_CODE_DESC", "SUBJECT_OFFERED_SUMMARY_KEY",
                      "SUBJECT_GROUPING_KEY"]),
    (tip_subjects, ["TERM_CODE", "SUBJECT_ID", "TIP_SUBJECT_OFFERED_KEY"]),
]:
    for c in cols:
        if c in df.columns:
            df[c] = clean_str(df[c])

# De-duplicate to one row per subject offering / cluster
course_base = course_summary.drop_duplicates(
    subset=[
        "SUBJECT_OFFERED_SUMMARY_KEY",
        "TERM_CODE",
        "SUBJECT_ID",
        "CLUSTER_TYPE",
        "HGN_CODE",
        "SUBJECT_GROUPING_KEY",
    ]
).copy()

# Identify biology-related courses/departments
bio_search_cols = [
    c for c in [
        "COURSE_NUMBER_DESC",
        "MASTER_COURSE_NUMBER_DESC",
        "OFFER_DEPT_NAME",
        "SUBJECT_TITLE",
        "SUBJECT_ID",
        "MASTER_SUBJECT_ID",
    ]
    if c in course_base.columns
]

bio_mask = pd.Series(False, index=course_base.index)
for c in bio_search_cols:
    bio_mask |= course_base[c].astype("string").str.contains("biolog", case=False, na=False)

# Include MIT Course 7 Biology explicitly
if "COURSE_NUMBER" in course_base.columns:
    bio_mask |= clean_str(course_base["COURSE_NUMBER"]).eq("7")
if "OFFER_DEPT_CODE" in course_base.columns:
    bio_mask |= clean_str(course_base["OFFER_DEPT_CODE"]).eq("7")

bio_courses = course_base.loc[bio_mask].copy()

# Semantic final grouping fields
bio_courses["department_name"] = bio_courses["OFFER_DEPT_NAME"]
bio_courses["course_title"] = bio_courses["SUBJECT_TITLE"]
bio_courses["cluster_type"] = bio_courses["CLUSTER_TYPE"]
bio_courses["course_level"] = bio_courses["HGN_CODE_DESC"].fillna(bio_courses["HGN_CODE"])

group_cols = ["department_name", "course_title", "cluster_type", "course_level"]

enrollment_summary = (
    bio_courses
    .groupby(group_cols, dropna=False, as_index=False)
    .agg(
        total_enrollments=("NUM_ENROLLED_STUDENTS", "sum"),
        average_enrollment_within_cluster=("CLUSTER_ENROLLMENT_NUMBER", "mean"),
    )
)

# -----------------------------
# TIP material / library metrics
# -----------------------------
tip_subject_keys = (
    tip_subjects[["TERM_CODE", "SUBJECT_ID", "TIP_SUBJECT_OFFERED_KEY"]]
    .dropna(subset=["TIP_SUBJECT_OFFERED_KEY"])
    .drop_duplicates()
)

bio_tip_keys = (
    bio_courses[["TERM_CODE", "SUBJECT_ID"] + group_cols]
    .drop_duplicates()
    .merge(tip_subject_keys, on=["TERM_CODE", "SUBJECT_ID"], how="left")
    .dropna(subset=["TIP_SUBJECT_OFFERED_KEY"])
)

for c in ["TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY", "TIP_MATERIAL_STATUS_KEY", "ISBN"]:
    if c in tip_assoc.columns:
        tip_assoc[c] = clean_str(tip_assoc[c])

valid_tip_assoc = tip_assoc[
    tip_assoc["TIP_SUBJECT_OFFERED_KEY"].notna()
    & tip_assoc["TIP_MATERIAL_KEY"].notna()
    & ~tip_assoc["TIP_MATERIAL_KEY"].str.contains("Course has no materials", case=False, na=False)
    & tip_assoc["TIP_MATERIAL_STATUS_KEY"].ne("NM")
].copy()

for c in ["TIP_MATERIAL_KEY", "ISBN", "TITLE"]:
    if c in materials.columns:
        materials[c] = clean_str(materials[c])

material_meta = (
    materials
    .dropna(subset=["TIP_MATERIAL_KEY"])
    .groupby("TIP_MATERIAL_KEY", dropna=False, as_index=False)
    .agg(
        library_title=("TITLE", first_non_null),
        material_isbn=("ISBN", first_non_null),
        new_shelf_price=("NEW_SHELF_PRICE", "mean"),
        used_shelf_price=("USED_SHELF_PRICE", "mean"),
    )
)

mat_joined = (
    bio_tip_keys
    .merge(valid_tip_assoc, on="TIP_SUBJECT_OFFERED_KEY", how="inner")
    .merge(material_meta, on="TIP_MATERIAL_KEY", how="left")
)

mat_joined["library_isbn"] = mat_joined["material_isbn"].fillna(mat_joined["ISBN"])

material_summary = (
    mat_joined
    .groupby(group_cols, dropna=False, as_index=False)
    .agg(
        number_of_unique_course_materials=("TIP_MATERIAL_KEY", "nunique"),
        average_new_price_for_tip_materials=("new_shelf_price", "mean"),
        average_used_price_for_tip_materials=("used_shelf_price", "mean"),
        total_material_record_count_for_tip_materials=("RECORD_COUNT", "sum"),
        number_of_unique_library_titles=("library_title", "nunique"),
        number_of_unique_library_isbns=("library_isbn", "nunique"),
    )
)

# -----------------------------
# Final answer
# -----------------------------
final = enrollment_summary.merge(material_summary, on=group_cols, how="left")

count_cols = [
    "number_of_unique_course_materials",
    "total_material_record_count_for_tip_materials",
    "number_of_unique_library_titles",
    "number_of_unique_library_isbns",
]
for c in count_cols:
    final[c] = final[c].fillna(0).astype(int)

final = final[
    [
        "department_name",
        "course_title",
        "cluster_type",
        "total_enrollments",
        "average_enrollment_within_cluster",
        "course_level",
        "number_of_unique_course_materials",
        "average_new_price_for_tip_materials",
        "average_used_price_for_tip_materials",
        "total_material_record_count_for_tip_materials",
        "number_of_unique_library_titles",
        "number_of_unique_library_isbns",
    ]
].sort_values(
    ["cluster_type", "course_level", "department_name", "course_title"],
    na_position="last"
).reset_index(drop=True)

result = {
    "biology_courses_by_cluster_type_and_course_level": final
}
