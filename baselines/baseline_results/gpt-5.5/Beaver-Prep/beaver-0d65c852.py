import pandas as pd
import numpy as np
import re

def first_nonnull(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else np.nan

def distinct_instructor_count(x):
    if pd.isna(x):
        return 0
    s = str(x).strip()
    if not s or s.lower() == "nan":
        return 0
    instructors = [p.strip() for p in re.split(r"\s*,\s*", s) if p.strip()]
    return len({p.lower() for p in instructors})

subjects = tables["table_4"].copy()

subjects["SO_TERM_CODE"] = subjects["SO_TERM_CODE"].astype(str).str.upper()
subjects["term"] = np.select(
    [subjects["SO_TERM_CODE"].str.endswith("SP"), subjects["SO_TERM_CODE"].str.endswith("FA")],
    ["Spring", "Fall"],
    default=np.nan
)

mask = (
    subjects["IS_OFFERED_THIS_YEAR"].eq("Y")
    & (
        (subjects["term"].eq("Fall") & subjects["IS_OFFERED_FALL_TERM"].eq("Y"))
        | (subjects["term"].eq("Spring") & subjects["IS_OFFERED_SPRING_TERM"].eq("Y"))
    )
)

subjects = subjects.loc[mask].copy()

subjects["fall_distinct_instructors"] = np.where(
    subjects["IS_OFFERED_FALL_TERM"].eq("Y"),
    subjects["FALL_INSTRUCTORS"].apply(distinct_instructor_count),
    0
)

subjects["spring_distinct_instructors"] = np.where(
    subjects["IS_OFFERED_SPRING_TERM"].eq("Y"),
    subjects["SPRING_INSTRUCTORS"].apply(distinct_instructor_count),
    0
)

school_maps = []

if "table_3" in tables and not tables["table_3"].empty:
    m3 = tables["table_3"].copy()
    m3["TERM_CODE"] = m3["TERM_CODE"].astype(str).str.upper()
    m3 = (
        m3.groupby(["TERM_CODE", "SUBJECT_ID"], as_index=False)
        .agg(
            school_name=("OFFER_SCHOOL_NAME", first_nonnull),
            offer_department_name=("OFFER_DEPT_NAME", first_nonnull)
        )
    )
    school_maps.append(m3)

if "table_5" in tables and not tables["table_5"].empty:
    m5 = tables["table_5"].copy()
    m5["TERM_CODE"] = m5["TERM_CODE"].astype(str).str.upper()
    m5 = (
        m5.groupby(["TERM_CODE", "SUBJECT_ID"], as_index=False)
        .agg(
            school_name=("OFFER_SCHOOL_NAME", first_nonnull),
            offer_department_name=("OFFER_DEPT_NAME", first_nonnull)
        )
    )
    school_maps.append(m5)

if school_maps:
    school_map = (
        pd.concat(school_maps, ignore_index=True)
        .groupby(["TERM_CODE", "SUBJECT_ID"], as_index=False)
        .agg(
            school_name=("school_name", first_nonnull),
            offer_department_name=("offer_department_name", first_nonnull)
        )
    )
    subjects = subjects.merge(
        school_map,
        how="left",
        left_on=["SO_TERM_CODE", "SUBJECT_ID"],
        right_on=["TERM_CODE", "SUBJECT_ID"]
    )
else:
    subjects["school_name"] = np.nan
    subjects["offer_department_name"] = np.nan

if "table_8" in tables and not tables["table_8"].empty:
    dept_school = (
        tables["table_8"]
        .groupby("DEPARTMENT", as_index=False)
        .agg(fallback_school_name=("SCHOOL_NAME", first_nonnull))
    )
    subjects = subjects.merge(
        dept_school,
        how="left",
        left_on="DEPARTMENT_CODE",
        right_on="DEPARTMENT"
    )
    subjects["school_name"] = subjects["school_name"].combine_first(subjects["fallback_school_name"])

subjects["department_name"] = subjects["DEPARTMENT_NAME"].combine_first(subjects["offer_department_name"])

answer = subjects[
    [
        "department_name",
        "school_name",
        "SUBJECT_ID",
        "SUBJECT_TITLE",
        "HGN_DESC",
        "TOTAL_UNITS",
        "term",
        "SO_TERM_DESCRIPTION",
        "fall_distinct_instructors",
        "spring_distinct_instructors",
        "SO_TERM_CODE"
    ]
].rename(columns={
    "SUBJECT_ID": "subject_id",
    "SUBJECT_TITLE": "subject_title",
    "HGN_DESC": "course_level",
    "TOTAL_UNITS": "total_units",
    "SO_TERM_DESCRIPTION": "term_description"
})

answer = (
    answer
    .drop_duplicates()
    .sort_values(["SO_TERM_CODE", "department_name", "subject_id", "term"], na_position="last")
    .drop(columns=["SO_TERM_CODE"])
    .reset_index(drop=True)
)

result = {"subjects_offered_fall_or_spring": answer}
