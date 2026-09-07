import pandas as pd
import numpy as np

def _clean_str(s):
    return s.astype("string").str.strip().replace("", pd.NA)

def _mode_or_first(s):
    s = s.dropna()
    if s.empty:
        return pd.NA
    m = s.mode()
    return m.iloc[0] if not m.empty else s.iloc[0]

lib = tables["table_1"].copy()
for col in [
    "LIBRARY_MATERIAL_STATUS_KEY",
    "TERM_CODE",
    "SUBJECT_ID",
    "LIBRARY_SUBJECT_OFFERED_KEY",
    "LIBRARY_COURSE_INSTRUCTOR_KEY",
]:
    lib[col] = _clean_str(lib[col])

fallback_course_key = (
    lib["TERM_CODE"].fillna("UNKNOWN_TERM")
    + "|"
    + lib["SUBJECT_ID"].fillna("UNKNOWN_SUBJECT")
)
lib["course_instance_key"] = lib["LIBRARY_SUBJECT_OFFERED_KEY"].fillna(fallback_course_key)

status_dim = tables["table_3"].copy()
status_dim["LIBRARY_MATERIAL_STATUS_KEY"] = _clean_str(status_dim["LIBRARY_MATERIAL_STATUS_KEY"])
status_dim["LIBRARY_MATERIAL_STATUS_CODE"] = _clean_str(status_dim["LIBRARY_MATERIAL_STATUS_CODE"])
status_dim["LIBRARY_MATERIAL_STATUS"] = status_dim["LIBRARY_MATERIAL_STATUS"].astype("string")
status_dim = status_dim[
    ["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS_CODE", "LIBRARY_MATERIAL_STATUS"]
].drop_duplicates("LIBRARY_MATERIAL_STATUS_KEY")

term_dim = tables["table_6"].copy()
term_dim["TERM_CODE"] = _clean_str(term_dim["term_code"])
term_dim["TERM_DESCRIPTION"] = term_dim["TERM_DESCRIPTION"].astype("string")
term_dim = term_dim[["TERM_CODE", "TERM_DESCRIPTION"]].drop_duplicates("TERM_CODE")

offering_parts = []

if "table_4" in tables:
    f4_cols = ["TERM_CODE", "SUBJECT_ID", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME"]
    f4 = tables["table_4"].copy()
    f4 = f4[[c for c in f4_cols if c in f4.columns]].copy()
    for c in f4_cols:
        if c not in f4.columns:
            f4[c] = pd.NA
        f4[c] = _clean_str(f4[c])
    f4["source_priority"] = 0
    offering_parts.append(f4[f4_cols + ["source_priority"]])

if "table_5" in tables:
    f5 = tables["table_5"].copy()
    f5_cols = ["TERM_CODE", "SUBJECT_ID", "DEPARTMENT_CODE", "DEPARTMENT_NAME"]
    f5 = f5[[c for c in f5_cols if c in f5.columns]].copy()
    for c in f5_cols:
        if c not in f5.columns:
            f5[c] = pd.NA
        f5[c] = _clean_str(f5[c])
    f5 = f5.rename(
        columns={
            "DEPARTMENT_CODE": "OFFER_DEPT_CODE",
            "DEPARTMENT_NAME": "OFFER_DEPT_NAME",
        }
    )

    if "table_8" in tables:
        dept_school_term = tables["table_8"].copy()
        dept_school_term["TERM_CODE"] = _clean_str(dept_school_term["TERM_CODE"])
        dept_school_term["OFFER_DEPT_CODE"] = _clean_str(dept_school_term["DEPARTMENT_CODE"])
        dept_school_term["OFFER_SCHOOL_NAME"] = _clean_str(dept_school_term["SCHOOL_NAME"])
        dept_school_term = (
            dept_school_term.dropna(subset=["TERM_CODE", "OFFER_DEPT_CODE", "OFFER_SCHOOL_NAME"])
            .groupby(["TERM_CODE", "OFFER_DEPT_CODE"], as_index=False)["OFFER_SCHOOL_NAME"]
            .agg(_mode_or_first)
        )
        f5 = f5.merge(dept_school_term, on=["TERM_CODE", "OFFER_DEPT_CODE"], how="left")
    else:
        f5["OFFER_SCHOOL_NAME"] = pd.NA

    if "table_9" in tables:
        dept_school = tables["table_9"].copy()
        dept_school["OFFER_DEPT_CODE"] = _clean_str(dept_school["DEPARTMENT"])
        dept_school["SCHOOL_FALLBACK"] = _clean_str(dept_school["SCHOOL_NAME"])
        dept_school = (
            dept_school.dropna(subset=["OFFER_DEPT_CODE", "SCHOOL_FALLBACK"])
            .groupby("OFFER_DEPT_CODE", as_index=False)["SCHOOL_FALLBACK"]
            .agg(_mode_or_first)
        )
        f5 = f5.merge(dept_school, on="OFFER_DEPT_CODE", how="left")
        f5["OFFER_SCHOOL_NAME"] = f5["OFFER_SCHOOL_NAME"].fillna(f5["SCHOOL_FALLBACK"])
        f5 = f5.drop(columns=["SCHOOL_FALLBACK"])

    f5["source_priority"] = 1
    offering_parts.append(
        f5[["TERM_CODE", "SUBJECT_ID", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME", "source_priority"]]
    )

if offering_parts:
    offering_dim = pd.concat(offering_parts, ignore_index=True)
    offering_dim = offering_dim.dropna(subset=["TERM_CODE", "SUBJECT_ID"])
    offering_dim["_has_school"] = offering_dim["OFFER_SCHOOL_NAME"].notna()
    offering_dim = (
        offering_dim.sort_values(
            ["TERM_CODE", "SUBJECT_ID", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "_has_school", "source_priority"],
            ascending=[True, True, True, True, False, True],
            na_position="last",
        )
        .drop_duplicates(["TERM_CODE", "SUBJECT_ID", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME"], keep="first")
        [["TERM_CODE", "SUBJECT_ID", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME"]]
    )
else:
    offering_dim = pd.DataFrame(
        columns=["TERM_CODE", "SUBJECT_ID", "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME"]
    )

group_keys = ["LIBRARY_MATERIAL_STATUS_KEY", "TERM_CODE"]

summary = (
    lib.groupby(group_keys, dropna=False)
    .agg(
        TOTAL_NUMBER_OF_COURSES=("course_instance_key", "nunique"),
        TOTAL_NUMBER_OF_MATERIALS=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"),
        TOTAL_NUMBER_OF_INSTRUCTORS=("LIBRARY_COURSE_INSTRUCTOR_KEY", "nunique"),
    )
    .reset_index()
)

course_level = lib[group_keys + ["SUBJECT_ID", "course_instance_key"]].drop_duplicates()
course_level = course_level.merge(offering_dim, on=["TERM_CODE", "SUBJECT_ID"], how="left")

course_level["DEPARTMENT_LABEL"] = (
    course_level["OFFER_DEPT_NAME"].fillna(course_level["OFFER_DEPT_CODE"]).fillna("Unknown")
)
course_level["SCHOOL_LABEL"] = course_level["OFFER_SCHOOL_NAME"].fillna("Unknown")

dept_base = course_level.drop_duplicates(group_keys + ["course_instance_key", "DEPARTMENT_LABEL"])
school_base = course_level.drop_duplicates(group_keys + ["course_instance_key", "SCHOOL_LABEL"])

dept_occurrences = (
    dept_base.groupby(group_keys, dropna=False)
    .size()
    .reset_index(name="DEPARTMENT_OCCURRENCES")
)

school_occurrences = (
    school_base.groupby(group_keys, dropna=False)
    .size()
    .reset_index(name="SCHOOL_OCCURRENCES")
)

dept_detail_counts = (
    dept_base.groupby(group_keys + ["DEPARTMENT_LABEL"], dropna=False)
    .size()
    .reset_index(name="n")
)
dept_detail_counts["DEPARTMENT_OCCURRENCE_DETAIL_PART"] = (
    dept_detail_counts["DEPARTMENT_LABEL"].astype("string").fillna("Unknown")
    + " ("
    + dept_detail_counts["n"].astype("string")
    + ")"
)
dept_detail = (
    dept_detail_counts.sort_values(group_keys + ["n", "DEPARTMENT_LABEL"], ascending=[True, True, False, True])
    .groupby(group_keys, dropna=False)["DEPARTMENT_OCCURRENCE_DETAIL_PART"]
    .agg(lambda x: "; ".join(x.astype(str)))
    .reset_index(name="DEPARTMENT_OCCURRENCE_DETAIL")
)

school_detail_counts = (
    school_base.groupby(group_keys + ["SCHOOL_LABEL"], dropna=False)
    .size()
    .reset_index(name="n")
)
school_detail_counts["SCHOOL_OCCURRENCE_DETAIL_PART"] = (
    school_detail_counts["SCHOOL_LABEL"].astype("string").fillna("Unknown")
    + " ("
    + school_detail_counts["n"].astype("string")
    + ")"
)
school_detail = (
    school_detail_counts.sort_values(group_keys + ["n", "SCHOOL_LABEL"], ascending=[True, True, False, True])
    .groupby(group_keys, dropna=False)["SCHOOL_OCCURRENCE_DETAIL_PART"]
    .agg(lambda x: "; ".join(x.astype(str)))
    .reset_index(name="SCHOOL_OCCURRENCE_DETAIL")
)

out = summary.merge(dept_occurrences, on=group_keys, how="left")
out = out.merge(school_occurrences, on=group_keys, how="left")
out = out.merge(dept_detail, on=group_keys, how="left")
out = out.merge(school_detail, on=group_keys, how="left")
out = out.merge(status_dim, on="LIBRARY_MATERIAL_STATUS_KEY", how="left")
out = out.merge(term_dim, on="TERM_CODE", how="left")

out["LIBRARY_MATERIAL_STATUS_CODE"] = out["LIBRARY_MATERIAL_STATUS_CODE"].fillna(out["LIBRARY_MATERIAL_STATUS_KEY"])
out["LIBRARY_MATERIAL_STATUS"] = out["LIBRARY_MATERIAL_STATUS"].fillna(out["LIBRARY_MATERIAL_STATUS_CODE"])
out["DEPARTMENT_OCCURRENCES"] = out["DEPARTMENT_OCCURRENCES"].fillna(0).astype("int64")
out["SCHOOL_OCCURRENCES"] = out["SCHOOL_OCCURRENCES"].fillna(0).astype("int64")
out["DEPARTMENT_OCCURRENCE_DETAIL"] = out["DEPARTMENT_OCCURRENCE_DETAIL"].fillna("")
out["SCHOOL_OCCURRENCE_DETAIL"] = out["SCHOOL_OCCURRENCE_DETAIL"].fillna("")

out = out[
    [
        "LIBRARY_MATERIAL_STATUS_CODE",
        "LIBRARY_MATERIAL_STATUS",
        "TERM_CODE",
        "TERM_DESCRIPTION",
        "TOTAL_NUMBER_OF_COURSES",
        "TOTAL_NUMBER_OF_MATERIALS",
        "DEPARTMENT_OCCURRENCES",
        "DEPARTMENT_OCCURRENCE_DETAIL",
        "SCHOOL_OCCURRENCES",
        "SCHOOL_OCCURRENCE_DETAIL",
        "TOTAL_NUMBER_OF_INSTRUCTORS",
    ]
].sort_values(["LIBRARY_MATERIAL_STATUS_CODE", "TERM_CODE"], na_position="last").reset_index(drop=True)

result = {"library_material_status_term_summary": out}
