import pandas as pd
import numpy as np

term_code = "2023FA"

def _clean_str(s):
    return s.astype("string").str.strip()

def _first_nonnull(x):
    x = x.dropna()
    x = x[x.astype(str).str.strip() != ""]
    return x.iloc[0] if len(x) else pd.NA

def _unique_join(x):
    vals = pd.Series(x).dropna().astype(str).str.strip()
    vals = vals[vals != ""].drop_duplicates()
    return ", ".join(vals) if len(vals) else pd.NA

# Term descriptions
terms = tables["table_5"].copy()
terms["term_code"] = _clean_str(terms["term_code"]).str.upper()
term_desc = (
    terms.loc[terms["term_code"].eq(term_code), ["term_code", "TERM_DESCRIPTION"]]
    .drop_duplicates()
    .rename(columns={"term_code": "TERM_CODE"})
)

# Subject details/prerequisites from subject offering/catalog table
subj_detail_src = tables["table_4"].copy()
subj_detail_src["SO_TERM_CODE"] = _clean_str(subj_detail_src["SO_TERM_CODE"]).str.upper()
subj_detail_src["SUBJECT_ID"] = _clean_str(subj_detail_src["SUBJECT_ID"])

subj_details = (
    subj_detail_src.loc[subj_detail_src["SO_TERM_CODE"].eq(term_code)]
    .groupby("SUBJECT_ID", as_index=False)
    .agg(
        subject_title=("SUBJECT_TITLE", _first_nonnull),
        prerequisites=("PREREQUISITES", _first_nonnull),
        so_term_description=("SO_TERM_DESCRIPTION", _unique_join),
    )
)

# Offerings and instructors
off = tables["table_6"].copy()
off["TERM_CODE"] = _clean_str(off["TERM_CODE"]).str.upper()
off["SUBJECT_ID"] = _clean_str(off["SUBJECT_ID"])
off["RESPONSIBLE_FACULTY_NAME"] = _clean_str(off["RESPONSIBLE_FACULTY_NAME"])
off["COURSE_NUMBER"] = _clean_str(off["COURSE_NUMBER"])

off_2023fa = (
    off.loc[off["TERM_CODE"].eq(term_code), [
        "TERM_CODE",
        "SUBJECT_ID",
        "SUBJECT_TITLE",
        "COURSE_NUMBER",
        "COURSE_NUMBER_DESC",
        "RESPONSIBLE_FACULTY_NAME",
        "RESPONSIBLE_FACULTY_MIT_ID",
    ]]
    .drop_duplicates()
    .rename(columns={
        "SUBJECT_TITLE": "offered_subject_title",
        "COURSE_NUMBER": "course_number",
        "COURSE_NUMBER_DESC": "course_number_description",
        "RESPONSIBLE_FACULTY_NAME": "instructor",
        "RESPONSIBLE_FACULTY_MIT_ID": "instructor_mit_id",
    })
)

# Count distinct subject types per term code
subjects_per_term = (
    off.dropna(subset=["SUBJECT_ID"])
    .groupby("TERM_CODE", as_index=False)["SUBJECT_ID"]
    .nunique()
    .rename(columns={"SUBJECT_ID": "total_subject_types_per_term_code"})
)

# Count distinct course-number types ever taught by each instructor
course_types_by_instructor = (
    off.dropna(subset=["RESPONSIBLE_FACULTY_NAME", "COURSE_NUMBER"])
    .loc[lambda d: d["RESPONSIBLE_FACULTY_NAME"].ne("")]
    .groupby("RESPONSIBLE_FACULTY_NAME", as_index=False)["COURSE_NUMBER"]
    .nunique()
    .rename(columns={
        "RESPONSIBLE_FACULTY_NAME": "instructor",
        "COURSE_NUMBER": "course_types_ever_taught_by_instructor",
    })
)

answer = (
    off_2023fa
    .merge(term_desc, on="TERM_CODE", how="left")
    .merge(subjects_per_term, on="TERM_CODE", how="left")
    .merge(subj_details, on="SUBJECT_ID", how="left")
    .merge(course_types_by_instructor, on="instructor", how="left")
)

answer["term_description"] = answer["TERM_DESCRIPTION"].combine_first(answer["so_term_description"])
answer["subject_title"] = answer["subject_title"].combine_first(answer["offered_subject_title"])

answer = (
    answer[[
        "TERM_CODE",
        "term_description",
        "SUBJECT_ID",
        "subject_title",
        "prerequisites",
        "total_subject_types_per_term_code",
        "instructor",
        "instructor_mit_id",
        "course_types_ever_taught_by_instructor",
    ]]
    .drop_duplicates()
    .sort_values(["SUBJECT_ID", "instructor"], na_position="last")
    .reset_index(drop=True)
)

result = {"fall_2023_subjects_instructors_and_counts": answer}
