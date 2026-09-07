import pandas as pd
import numpy as np

subjects = tables["table_5"].copy()

# Standardize key/text columns
for col in ["TERM_CODE", "SUBJECT_ID", "DEPARTMENT_CODE", "DEPARTMENT_NAME", "HASS_ATTRIBUTE_DESC", "HASS_ATTRIBUTE"]:
    if col in subjects.columns:
        subjects[col] = subjects[col].astype("string").str.strip()

# Keep Humanities, Arts, and Social Sciences attribute-bearing subjects
hass = subjects[
    subjects["HASS_ATTRIBUTE_DESC"].notna()
    & (subjects["HASS_ATTRIBUTE_DESC"] != "")
].copy()

# Add school name from term/subject offering table where available
offer_cols = ["TERM_CODE", "SUBJECT_ID", "OFFER_SCHOOL_NAME", "OFFER_DEPT_NAME"]
offers = tables["table_7"][offer_cols].copy()
for col in offer_cols:
    offers[col] = offers[col].astype("string").str.strip()

offers = offers.drop_duplicates(subset=["TERM_CODE", "SUBJECT_ID"])

hass = hass.merge(
    offers,
    on=["TERM_CODE", "SUBJECT_ID"],
    how="left"
)

# Add school name from department lookup as fallback
dept_lookup = tables["table_9"][["DEPARTMENT_CODE", "SCHOOL_NAME"]].copy()
dept_lookup["DEPARTMENT_CODE"] = dept_lookup["DEPARTMENT_CODE"].astype("string").str.strip()
dept_lookup["SCHOOL_NAME"] = dept_lookup["SCHOOL_NAME"].astype("string").str.strip()
dept_lookup = dept_lookup.drop_duplicates(subset=["DEPARTMENT_CODE"])

hass = hass.merge(
    dept_lookup,
    on="DEPARTMENT_CODE",
    how="left",
    suffixes=("", "_DEPT_LOOKUP")
)

hass["SCHOOL_NAME_FINAL"] = hass["OFFER_SCHOOL_NAME"].combine_first(hass["SCHOOL_NAME"])
hass["DEPARTMENT_NAME_FINAL"] = hass["DEPARTMENT_NAME"].combine_first(hass["OFFER_DEPT_NAME"])

def make_term_description(term_code):
    if pd.isna(term_code):
        return pd.NA
    
    code = str(term_code).strip()
    if code == "000000":
        return "Beginning of Time"
    if code == "999999":
        return "End of Time"
    if len(code) < 6 or not code[:4].isdigit():
        return pd.NA
    
    year = int(code[:4])
    suffix = code[4:].upper()
    academic_year = f"{year - 1}-{year}"
    
    term_name_map = {
        "FA": "Fall Term",
        "SP": "Spring Term",
        "SU": "Summer Term",
        "JA": "Independent Activities Period",
        "IAP": "Independent Activities Period",
    }
    
    term_name = term_name_map.get(suffix, suffix)
    return f"{term_name} {academic_year}"

hass["TERM_DESCRIPTION"] = hass["TERM_CODE"].apply(make_term_description)

answer = (
    hass
    .drop_duplicates(subset=[
        "TERM_CODE",
        "SUBJECT_ID",
        "HASS_ATTRIBUTE_DESC",
        "DEPARTMENT_NAME_FINAL",
        "SCHOOL_NAME_FINAL"
    ])
    .groupby(
        [
            "TERM_CODE",
            "TERM_DESCRIPTION",
            "HASS_ATTRIBUTE_DESC",
            "DEPARTMENT_NAME_FINAL",
            "SCHOOL_NAME_FINAL"
        ],
        dropna=False,
        as_index=False
    )
    .agg(NUMBER_OF_SUBJECTS=("SUBJECT_ID", "nunique"))
    .rename(columns={
        "HASS_ATTRIBUTE_DESC": "ATTRIBUTE_DESCRIPTION",
        "DEPARTMENT_NAME_FINAL": "DEPARTMENT_NAME",
        "SCHOOL_NAME_FINAL": "SCHOOL_NAME"
    })
    .sort_values(
        ["TERM_CODE", "ATTRIBUTE_DESCRIPTION", "DEPARTMENT_NAME", "SCHOOL_NAME"],
        na_position="last"
    )
    .reset_index(drop=True)
)

result = {
    "hass_subject_counts_by_term": answer
}
