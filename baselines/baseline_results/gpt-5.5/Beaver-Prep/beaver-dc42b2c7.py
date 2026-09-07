import pandas as pd
import numpy as np

def norm(s):
    return s.astype("string").str.strip().str.upper()

def clean_vals(x):
    vals = pd.Series(x).dropna().astype(str).str.strip()
    vals = vals[(vals != "") & (vals.str.lower() != "nan") & (vals.str.lower() != "<na>")]
    return vals

def join_unique(x):
    vals = clean_vals(x)
    return ", ".join(sorted(vals.unique()))

def first_nonnull(x):
    vals = clean_vals(x)
    return vals.iloc[0] if len(vals) else pd.NA

courses = tables["table_3"].copy()
subject_codes = tables["table_6"].copy()
hass_lookup_raw = tables["table_4"].copy()
attr_lookup_raw = tables["table_5"].copy()
enrollments = tables["table_7"].copy()
degree_courses = tables["table_8"].copy()

subject_codes["subject_code_key"] = norm(subject_codes["SUBJECT_CODE"])
pol_mask = (
    subject_codes["SUBJECT_CODE_DESC"].astype("string").str.contains("Political Science", case=False, na=False)
    | subject_codes["DEPARTMENT_NAME"].astype("string").str.contains("Political Science", case=False, na=False)
    | subject_codes["subject_code_key"].eq("17")
)
pol_subject_codes = set(subject_codes.loc[pol_mask, "subject_code_key"].dropna())
if not pol_subject_codes:
    pol_subject_codes = {"17"}

courses["subject_code_key"] = norm(courses["SUBJECT_CODE"])
courses["dept_name_key"] = courses["DEPARTMENT_NAME"].astype("string")

pol_courses = courses[
    courses["subject_code_key"].isin(pol_subject_codes)
    | courses["dept_name_key"].str.contains("Political Science", case=False, na=False)
].copy()

hass_lookup_raw["hass_attribute_key"] = norm(hass_lookup_raw["hass_attribute"])
known_hass_codes = set(hass_lookup_raw["hass_attribute_key"].dropna())

base_cols = [
    "ACADEMIC_YEAR", "SUBJECT_ID", "SUBJECT_CODE", "DEPARTMENT_CODE", "DEPARTMENT_NAME",
    "SUBJECT_TITLE", "TOTAL_UNITS", "SO_TERM_CODE", "HASS_ATTRIBUTE", "HASS_ATTRIBUTE_DESC",
    "GIR_ATTRIBUTE", "GIR_ATTRIBUTE_DESC"
]
base_cols = [c for c in base_cols if c in pol_courses.columns]

def make_attr_long(df, code_col, desc_col, restrict_to_known_hass=False):
    cols = base_cols.copy()
    if code_col not in df.columns:
        return pd.DataFrame(columns=cols + ["hass_attribute", "source_attribute_desc"])
    tmp = df[cols].copy()
    tmp["hass_attribute"] = df[code_col].astype("string").str.strip()
    tmp["source_attribute_desc"] = df[desc_col].astype("string").str.strip() if desc_col in df.columns else pd.NA
    tmp = tmp[tmp["hass_attribute"].notna() & tmp["hass_attribute"].ne("")]
    tmp["hass_attribute"] = tmp["hass_attribute"].str.split(r"\s*[,;]\s*")
    tmp = tmp.explode("hass_attribute")
    tmp["hass_attribute"] = norm(tmp["hass_attribute"])
    tmp = tmp[tmp["hass_attribute"].notna() & tmp["hass_attribute"].ne("")]
    if restrict_to_known_hass and known_hass_codes:
        tmp = tmp[tmp["hass_attribute"].isin(known_hass_codes)]
    return tmp

hass_rows = make_attr_long(pol_courses, "HASS_ATTRIBUTE", "HASS_ATTRIBUTE_DESC", restrict_to_known_hass=False)
gir_hass_rows = make_attr_long(pol_courses, "GIR_ATTRIBUTE", "GIR_ATTRIBUTE_DESC", restrict_to_known_hass=True)
course_attrs = pd.concat([hass_rows, gir_hass_rows], ignore_index=True)

final_columns = [
    "hass_attribute",
    "attribute_name",
    "attribute_description",
    "number_of_unique_subjects",
    "average_units",
    "total_enrollment",
    "number_of_degree_granting_departments",
    "subject_code_description",
]

if course_attrs.empty:
    out = pd.DataFrame(columns=final_columns)
else:
    dedup_keys = [c for c in ["SUBJECT_ID", "SO_TERM_CODE", "hass_attribute"] if c in course_attrs.columns]
    if dedup_keys:
        course_attrs = course_attrs.drop_duplicates(dedup_keys).copy()

    course_attrs["subject_id_key"] = norm(course_attrs["SUBJECT_ID"])
    course_attrs["term_code_key"] = norm(course_attrs["SO_TERM_CODE"])
    course_attrs["subject_code_key"] = norm(course_attrs["SUBJECT_CODE"])
    course_attrs["dept_code_key"] = norm(course_attrs["DEPARTMENT_CODE"])
    course_attrs["TOTAL_UNITS_NUM"] = pd.to_numeric(course_attrs["TOTAL_UNITS"], errors="coerce")

    sc_agg = (
        subject_codes.groupby("subject_code_key", as_index=False)
        .agg(
            subject_code_description=("SUBJECT_CODE_DESC", join_unique),
            subject_code_department=("DEPARTMENT_CODE", first_nonnull),
        )
    )
    sc_agg["subject_code_department_key"] = norm(sc_agg["subject_code_department"])
    course_attrs = course_attrs.merge(sc_agg, on="subject_code_key", how="left")
    course_attrs["dept_code_key"] = course_attrs["dept_code_key"].fillna(course_attrs["subject_code_department_key"])

    degree_rows = degree_courses[
        degree_courses["IS_DEGREE_GRANTING"].astype("string").str.strip().str.upper().eq("Y")
    ].copy()
    degree_dept_keys = set()
    if "DEPARTMENT" in degree_rows.columns:
        degree_dept_keys |= set(norm(degree_rows["DEPARTMENT"]).dropna())
    if "COURSE" in degree_rows.columns:
        degree_dept_keys |= set(norm(degree_rows["COURSE"].astype("string").str.split().str[0]).dropna())

    course_attrs["degree_granting_dept_key"] = course_attrs["dept_code_key"].where(
        course_attrs["dept_code_key"].isin(degree_dept_keys),
        pd.NA,
    )

    enr = enrollments.copy()
    enr["subject_id_key"] = norm(enr["SUBJECT_ID"])
    enr["term_code_key"] = norm(enr["TERM_CODE"])
    enrollment_col = "SUBJECT_ENROLLMENT_NUMBER" if "SUBJECT_ENROLLMENT_NUMBER" in enr.columns else "NUM_ENROLLED_STUDENTS"
    enr["enrollment_number"] = pd.to_numeric(enr[enrollment_col], errors="coerce").fillna(0)
    enr_agg = (
        enr.groupby(["subject_id_key", "term_code_key"], as_index=False)
        .agg(enrollment_number=("enrollment_number", "max"))
    )

    course_attrs = course_attrs.merge(enr_agg, on=["subject_id_key", "term_code_key"], how="left")
    course_attrs["enrollment_number"] = course_attrs["enrollment_number"].fillna(0)

    subject_units = (
        course_attrs.groupby(["hass_attribute", "subject_id_key"], as_index=False)
        .agg(subject_average_units=("TOTAL_UNITS_NUM", "mean"))
    )
    subject_summary = (
        subject_units.groupby("hass_attribute", as_index=False)
        .agg(
            number_of_unique_subjects=("subject_id_key", "nunique"),
            average_units=("subject_average_units", "mean"),
        )
    )

    enrollment_summary = (
        course_attrs.groupby("hass_attribute", as_index=False)
        .agg(total_enrollment=("enrollment_number", "sum"))
    )

    dept_summary = (
        course_attrs.groupby("hass_attribute", as_index=False)
        .agg(number_of_degree_granting_departments=("degree_granting_dept_key", "nunique"))
    )

    subj_code_summary = (
        course_attrs.groupby("hass_attribute", as_index=False)
        .agg(subject_code_description=("subject_code_description", join_unique))
    )

    source_desc_summary = (
        course_attrs.groupby("hass_attribute", as_index=False)
        .agg(source_attribute_desc=("source_attribute_desc", join_unique))
    )

    hass_meta = pd.DataFrame({
        "hass_attribute": hass_lookup_raw["hass_attribute_key"],
        "hass_attribute_name": hass_lookup_raw["DESCRIPTION_ON_FORM"],
        "hass_attribute_description": hass_lookup_raw["DESCRIPTION_IN_BULLETIN"],
    }).drop_duplicates("hass_attribute")

    attr_meta = pd.DataFrame({
        "hass_attribute": norm(attr_lookup_raw["SUBJECT_ATTRIBUTE_CODE"]),
        "subject_attribute_short_desc": attr_lookup_raw["SUBJECT_ATTRIBUTE_SHORT_DESC"],
        "subject_attribute_desc": attr_lookup_raw["SUBJECT_ATTRIBUTE_DESC"],
    }).drop_duplicates("hass_attribute")

    meta = hass_meta.merge(attr_meta, on="hass_attribute", how="outer")
    meta["attribute_name"] = meta["hass_attribute_name"].combine_first(meta["subject_attribute_short_desc"])
    meta["attribute_description"] = meta["hass_attribute_description"].combine_first(meta["subject_attribute_desc"])
    meta = meta[["hass_attribute", "attribute_name", "attribute_description"]]

    out = (
        subject_summary
        .merge(enrollment_summary, on="hass_attribute", how="left")
        .merge(dept_summary, on="hass_attribute", how="left")
        .merge(subj_code_summary, on="hass_attribute", how="left")
        .merge(source_desc_summary, on="hass_attribute", how="left")
        .merge(meta, on="hass_attribute", how="left")
    )

    out["attribute_name"] = out["attribute_name"].combine_first(out["source_attribute_desc"])
    out["attribute_name"] = out["attribute_name"].fillna(out["hass_attribute"])
    out["attribute_description"] = out["attribute_description"].combine_first(out["source_attribute_desc"])

    out["total_enrollment"] = out["total_enrollment"].fillna(0).astype(int)
    out["number_of_degree_granting_departments"] = out["number_of_degree_granting_departments"].fillna(0).astype(int)
    out["number_of_unique_subjects"] = out["number_of_unique_subjects"].astype(int)

    out = out[final_columns].sort_values("hass_attribute").reset_index(drop=True)

result = {"political_science_hass_attributes": out}
