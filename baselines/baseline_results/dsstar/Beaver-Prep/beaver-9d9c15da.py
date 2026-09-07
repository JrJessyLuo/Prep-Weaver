import pandas as pd
import numpy as np
import re

# Input tables (already loaded in `tables`)
tip_detail = tables['table_1']
tip_so = tables['table_2']
summary = tables['table_3']
tip_material = tables['table_4']
subject_enrollable = tables['table_5']
subject_offered = tables['table_6']
subject_selector = tables['table_7']
sis_course_desc = tables['table_8']
subject_grouping = tables['table_9']

# Normalize key columns to string for safe merge
def to_str_cols(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str)
    return df

for df in (summary, tip_so, subject_offered, tip_detail, tip_material):
    to_str_cols(df, ["TERM_CODE", "SUBJECT_ID", "SUBJECT_TITLE", "OFFER_DEPT_NAME", "OFFER_DEPT_CODE", "COURSE_NUMBER", "COURSE_NUMBER_SORT"])

# Column subsets mirroring reference
summary_cols = [
    "TERM_CODE",
    "SUBJECT_ID",
    "SUBJECT_TITLE",
    "MASTER_SUBJECT_ID",
    "CLUSTER_TYPE",
    "CLUSTER_TYPE_DESC",
    "CLUSTER_LIST",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "RESPONSIBLE_FACULTY_NAME",
    "RESPONSIBLE_FACULTY_MIT_ID",
    "TOTAL_UNITS",
    "SUBJECT_ENROLLMENT_NUMBER",
    "NUM_ENROLLED_STUDENTS",
]
tip_cols = [
    "TIP_SUBJECT_OFFERED_KEY",
    "TERM_CODE",
    "SUBJECT_ID",
    "IS_NO_COURSE_MATERIAL",
    "MASTER_COURSE_NUMBER",
    "MASTER_COURSE_NUMBER_DESC",
    "COURSE_NUMBER",
    "COURSE_NUMBER_DESC",
    "SUBJECT_TITLE",
    "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME",
    "OFFER_SCHOOL_NAME",
    "RESPONSIBLE_FACULTY_NAME",
    "RESPONSIBLE_FACULTY_MIT_ID",
    "NUM_ENROLLED_STUDENTS",
]

summary_sub = summary[[c for c in summary_cols if c in summary.columns]].copy()
tip_so_sub = tip_so[[c for c in tip_cols if c in tip_so.columns]].copy()

# Merge
merged = pd.merge(
    summary_sub,
    tip_so_sub,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="inner",
    suffixes=("_SUM", "_TIP"),
)

# Prepare helper columns for bio filter
if "OFFER_DEPT_NAME_SUM" not in merged.columns:
    if "OFFER_DEPT_NAME" in summary_sub.columns:
        merged["OFFER_DEPT_NAME_SUM"] = merged["OFFER_DEPT_NAME"]
    else:
        merged["OFFER_DEPT_NAME_SUM"] = ""
if "OFFER_DEPT_NAME_TIP" not in merged.columns:
    merged["OFFER_DEPT_NAME_TIP"] = tip_so_sub.get("OFFER_DEPT_NAME", "")

if "OFFER_DEPT_CODE_SUM" not in merged.columns:
    merged["OFFER_DEPT_CODE_SUM"] = summary_sub.get("OFFER_DEPT_CODE", "")
if "OFFER_DEPT_CODE_TIP" not in merged.columns:
    merged["OFFER_DEPT_CODE_TIP"] = tip_so_sub.get("OFFER_DEPT_CODE", "")

# Biology filter (same logic)
bio_patterns = [
    "BIO", "BIOLOGY", "BIOLOGICAL", "NEUROBIO", "MICROBIO", "SYSTEMS BIO",
    "MOLECULAR BIO", "COMPUTATIONAL BIO",
]
def is_bio(row):
    title = str(row.get("SUBJECT_TITLE_SUM", "")) + " " + str(row.get("SUBJECT_TITLE_TIP", ""))
    dept_name = str(row.get("OFFER_DEPT_NAME_SUM", "")) + " " + str(row.get("OFFER_DEPT_NAME_TIP", ""))
    dept_code = str(row.get("OFFER_DEPT_CODE_SUM", "")) + " " + str(row.get("OFFER_DEPT_CODE_TIP", ""))
    subj_id = str(row.get("SUBJECT_ID", ""))
    title_upper = title.upper()
    dept_upper = (dept_name + " " + dept_code).upper()
    text_hit = any(pat in title_upper for pat in bio_patterns) or any(pat in dept_upper for pat in bio_patterns)
    id_hit = subj_id.startswith(("7", "20"))  # Course 7 (Biology), Course 20 (Biological Engineering)
    return text_hit or id_hit

bio_mask = merged.apply(is_bio, axis=1)
biology_subjects = merged[bio_mask].copy()

# Final columns selection similar to reference
final_cols = [
    "TERM_CODE",
    "SUBJECT_ID",
    "SUBJECT_TITLE_SUM" if "SUBJECT_TITLE_SUM" in biology_subjects.columns else "SUBJECT_TITLE",
    "MASTER_SUBJECT_ID",
    "CLUSTER_TYPE",
    "CLUSTER_TYPE_DESC",
    "CLUSTER_LIST",
    "SUBJECT_ENROLLMENT_NUMBER" if "SUBJECT_ENROLLMENT_NUMBER" in biology_subjects.columns else (
        "NUM_ENROLLED_STUDENTS_SUM" if "NUM_ENROLLED_STUDENTS_SUM" in biology_subjects.columns else "NUM_ENROLLED_STUDENTS"
    ),
    "NUM_ENROLLED_STUDENTS_TIP" if "NUM_ENROLLED_STUDENTS_TIP" in biology_subjects.columns else (
        "NUM_ENROLLED_STUDENTS" if "NUM_ENROLLED_STUDENTS" in biology_subjects.columns else None
    ),
    "OFFER_DEPT_CODE_SUM" if "OFFER_DEPT_CODE_SUM" in biology_subjects.columns else "OFFER_DEPT_CODE",
    "OFFER_DEPT_NAME_SUM" if "OFFER_DEPT_NAME_SUM" in biology_subjects.columns else "OFFER_DEPT_NAME",
    "RESPONSIBLE_FACULTY_NAME",
]
final_cols = [c for c in final_cols if c in biology_subjects.columns]
biology_subjects_enrollment_cluster = biology_subjects[final_cols].drop_duplicates().reset_index(drop=True)

# Unified enrollment metric
if "SUBJECT_ENROLLMENT_NUMBER" in biology_subjects_enrollment_cluster.columns:
    biology_subjects_enrollment_cluster["ENROLLMENT"] = biology_subjects_enrollment_cluster["SUBJECT_ENROLLMENT_NUMBER"]
else:
    enroll_cols = [c for c in ["NUM_ENROLLED_STUDENTS", "NUM_ENROLLED_STUDENTS_TIP", "NUM_ENROLLED_STUDENTS_SUM"] if c in biology_subjects_enrollment_cluster.columns]
    if enroll_cols:
        biology_subjects_enrollment_cluster["ENROLLMENT"] = biology_subjects_enrollment_cluster[enroll_cols[0]]
    else:
        biology_subjects_enrollment_cluster["ENROLLMENT"] = np.nan

# Join with SUBJECT_OFFERED to bring COURSE_NUMBER/level and OFFER_DEPT_NAME
needed_so_cols = ["TERM_CODE", "SUBJECT_ID", "COURSE_NUMBER", "COURSE_NUMBER_SORT", "OFFER_DEPT_NAME", "OFFER_DEPT_CODE"]
so_min = subject_offered[[c for c in needed_so_cols if c in subject_offered.columns]].copy()
so_min = so_min.drop_duplicates(subset=["TERM_CODE", "SUBJECT_ID"])

bio_with_course = biology_subjects_enrollment_cluster.merge(
    so_min,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="left",
    suffixes=("", "_SO")
)

# Compute course level
def extract_level(course_number, course_number_sort):
    if pd.notna(course_number_sort):
        s = str(course_number_sort)
        m = re.search(r'(\d{2,3})', s)
        if m:
            num = int(m.group(1))
            if num < 100:
                return "0xx"
            return f"{str(num)[0]}xx"
    if pd.notna(course_number):
        s = str(course_number)
        m = re.search(r'(\d{2,3})', s)
        if m:
            num = int(m.group(1))
            if num < 100:
                return "0xx"
            return f"{str(num)[0]}xx"
    return "unknown"

bio_with_course["COURSE_LEVEL"] = bio_with_course.apply(
    lambda r: extract_level(r.get("COURSE_NUMBER"), r.get("COURSE_NUMBER_SORT")),
    axis=1
)

# Clean CLUSTER_TYPE
if "CLUSTER_TYPE" not in bio_with_course.columns:
    bio_with_course["CLUSTER_TYPE"] = "Unknown"
bio_with_course["CLUSTER_TYPE"] = bio_with_course["CLUSTER_TYPE"].fillna("Unknown")
bio_with_course["ENROLLMENT"] = pd.to_numeric(bio_with_course["ENROLLMENT"], errors="coerce")

# Prepare department name and subject title fields
dept_name_col = "OFFER_DEPT_NAME_SUM" if "OFFER_DEPT_NAME_SUM" in bio_with_course.columns else ("OFFER_DEPT_NAME" if "OFFER_DEPT_NAME" in bio_with_course.columns else None)
if dept_name_col is None and "OFFER_DEPT_NAME_SO" in bio_with_course.columns:
    dept_name_col = "OFFER_DEPT_NAME_SO"
elif dept_name_col is None:
    bio_with_course["OFFER_DEPT_NAME_SO"] = ""
    dept_name_col = "OFFER_DEPT_NAME_SO"

title_col = "SUBJECT_TITLE_SUM" if "SUBJECT_TITLE_SUM" in bio_with_course.columns else ("SUBJECT_TITLE" if "SUBJECT_TITLE" in bio_with_course.columns else None)
if title_col is None:
    bio_with_course["SUBJECT_TITLE_FALLBACK"] = ""
    title_col = "SUBJECT_TITLE_FALLBACK"

# TIP materials metrics (from TIP_DETAIL and TIP_MATERIAL)
# Normalize keys possibly needed
for df in (tip_detail, tip_material):
    to_str_cols(df, ["TERM_CODE", "SUBJECT_ID", "TIP_SUBJECT_OFFERED_KEY", "ISBN_10", "ISBN_13", "TITLE"])

# Aggregate TIP detail/material per subject-term
# Unique material count from TIP_DETAIL per subject-term
tip_detail_subj = tip_detail.copy()
# Define a material identifier: prefer TIP_MATERIAL_KEY if exists, else ISBN or TITLE where available
mat_id_cols = [c for c in ["TIP_MATERIAL_KEY", "MATERIAL_KEY", "ISBN_13", "ISBN_10", "TITLE"] if c in tip_detail_subj.columns]
if mat_id_cols:
    tip_detail_subj["MAT_ID"] = tip_detail_subj[mat_id_cols].astype(str).agg("|".join, axis=1)
else:
    tip_detail_subj["MAT_ID"] = tip_detail_subj.index.astype(str)

tip_detail_agg = (
    tip_detail_subj.groupby(["TERM_CODE", "SUBJECT_ID"], dropna=False)
    .agg(
        unique_tip_materials=("MAT_ID", "nunique"),
        tip_record_count=("MAT_ID", "size")
    )
    .reset_index()
)

# Average new/used prices from TIP_MATERIAL per subject-term
tip_material_subj = tip_material.copy()
price_cols = []
if "NEW_PRICE" in tip_material_subj.columns:
    price_cols.append("NEW_PRICE")
if "USED_PRICE" in tip_material_subj.columns:
    price_cols.append("USED_PRICE")
for c in price_cols:
    tip_material_subj[c] = pd.to_numeric(tip_material_subj[c], errors="coerce")

# Derive a material identifier in TIP_MATERIAL as well for de-duplication
mat_id_cols_tm = [c for c in ["TIP_MATERIAL_KEY", "MATERIAL_KEY", "ISBN_13", "ISBN_10", "TITLE"] if c in tip_material_subj.columns]
if mat_id_cols_tm:
    tip_material_subj["MAT_ID"] = tip_material_subj[mat_id_cols_tm].astype(str).agg("|".join, axis=1)
else:
    tip_material_subj["MAT_ID"] = tip_material_subj.index.astype(str)

tip_material_agg = (
    tip_material_subj.groupby(["TERM_CODE", "SUBJECT_ID"], dropna=False)
    .agg(
        avg_new_price=("NEW_PRICE", "mean") if "NEW_PRICE" in tip_material_subj.columns else ("MAT_ID", "size"),
        avg_used_price=("USED_PRICE", "mean") if "USED_PRICE" in tip_material_subj.columns else ("MAT_ID", "size"),
    )
    .reset_index()
)

# Library metrics from TIP_DETAIL: unique library titles and ISBNs
lib_cols_title = [c for c in ["LIBRARY_TITLE", "TITLE"] if c in tip_detail_subj.columns]
lib_cols_isbn = [c for c in ["LIBRARY_ISBN", "ISBN_13", "ISBN_10"] if c in tip_detail_subj.columns]

td_lib = tip_detail_subj.copy()
if lib_cols_title:
    td_lib["LIB_TITLE"] = td_lib[lib_cols_title[0]].astype(str)
else:
    td_lib["LIB_TITLE"] = ""
if lib_cols_isbn:
    # prefer ISBN_13 then ISBN_10
    if "ISBN_13" in td_lib.columns:
        td_lib["LIB_ISBN"] = td_lib["ISBN_13"].astype(str)
    elif "LIBRARY_ISBN" in td_lib.columns:
        td_lib["LIB_ISBN"] = td_lib["LIBRARY_ISBN"].astype(str)
    else:
        td_lib["LIB_ISBN"] = td_lib[lib_cols_isbn[0]].astype(str)
else:
    td_lib["LIB_ISBN"] = ""

lib_agg = (
    td_lib.groupby(["TERM_CODE", "SUBJECT_ID"], dropna=False)
    .agg(
        unique_library_titles=("LIB_TITLE", lambda x: x.replace("", np.nan).dropna().nunique()),
        unique_library_isbns=("LIB_ISBN", lambda x: x.replace("", np.nan).dropna().nunique()),
    )
    .reset_index()
)

# Merge all enrichment back to bio_with_course
bio_enriched = bio_with_course.merge(tip_detail_agg, on=["TERM_CODE", "SUBJECT_ID"], how="left")
bio_enriched = bio_enriched.merge(tip_material_agg, on=["TERM_CODE", "SUBJECT_ID"], how="left")
bio_enriched = bio_enriched.merge(lib_agg, on=["TERM_CODE", "SUBJECT_ID"], how="left")

# Compute cluster-level average enrollment for the course's cluster within same cluster type
cluster_avg = (
    bio_enriched.groupby(["CLUSTER_TYPE"])
    .agg(cluster_avg_enrollment=("ENROLLMENT", "mean"))
    .reset_index()
)
bio_enriched = bio_enriched.merge(cluster_avg, on="CLUSTER_TYPE", how="left")

# Prepare final per-course rows with requested fields
final_courses = bio_enriched.copy()

# Select output columns
final_courses["DEPARTMENT_NAME"] = final_courses[dept_name_col]
final_courses["COURSE_TITLE"] = final_courses[title_col]

out_cols = [
    "TERM_CODE",
    "SUBJECT_ID",
    "DEPARTMENT_NAME",
    "COURSE_TITLE",
    "CLUSTER_TYPE",
    "ENROLLMENT",                     # total enrollments (per course instance)
    "cluster_avg_enrollment",         # average enrollment within its cluster type
    "COURSE_LEVEL",
    "unique_tip_materials",           # number of unique course materials
    "avg_new_price",                  # average new price for TIP materials
    "avg_used_price",                 # average used price for TIP materials
    "tip_record_count",               # total material record count for TIP materials
    "unique_library_titles",          # number of unique library titles
    "unique_library_isbns",           # number of unique library ISBNs
]

# Ensure columns exist
for c in out_cols:
    if c not in final_courses.columns:
        final_courses[c] = np.nan

final_courses_out = final_courses[out_cols].copy()

# Also provide an aggregation by (CLUSTER_TYPE, COURSE_LEVEL) if desired by question phrasing
agg_by_cluster_level = (
    final_courses_out
    .groupby(["CLUSTER_TYPE", "COURSE_LEVEL"], dropna=False)
    .agg(
        courses=("SUBJECT_ID", "nunique"),
        total_enrollment=("ENROLLMENT", "sum"),
        avg_enrollment_in_group=("ENROLLMENT", "mean"),
        avg_of_cluster_avg=("cluster_avg_enrollment", "mean"),
        total_unique_tip_materials=("unique_tip_materials", "sum"),
        avg_new_price=("avg_new_price", "mean"),
        avg_used_price=("avg_used_price", "mean"),
        total_tip_records=("tip_record_count", "sum"),
        total_unique_library_titles=("unique_library_titles", "sum"),
        total_unique_library_isbns=("unique_library_isbns", "sum"),
    )
    .reset_index()
)

# Package result
result = {
    "biology_courses_by_cluster_and_level_detail": final_courses_out,
    "biology_courses_by_cluster_and_level_agg": agg_by_cluster_level
}