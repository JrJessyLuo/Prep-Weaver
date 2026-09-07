import pandas as pd
import numpy as np

iap = tables["table_1"].copy()
people = tables["table_2"].copy()

def norm_key(s):
    return s.astype("string").str.strip().str.upper()

def norm_name(s):
    return (
        s.astype("string")
        .str.strip()
        .str.upper()
        .str.replace(r"[^A-Z0-9]+", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

iap["person_key"] = norm_key(iap["IAP_SUBJECT_PERSON_KEY"])
iap["academic_year"] = pd.to_numeric(
    iap["TERM_CODE"].astype("string").str.extract(r"(\d{4})", expand=False),
    errors="coerce"
).astype("Int64")

iap["subject_key"] = iap["IAP_SUBJECT_SESSION_KEY"].astype("string").str.strip()
title_fallback = "TITLE:" + iap["ACTIVITY_TITLE"].astype("string").str.strip()
row_fallback = pd.Series("ROW:" + iap.index.to_series().astype("string"), index=iap.index, dtype="string")
iap["subject_key"] = iap["subject_key"].combine_first(title_fallback).combine_first(row_fallback)

iap_subjects = (
    iap.groupby(["person_key", "academic_year", "subject_key"], dropna=False, as_index=False)
       .agg(
           fee=("FEE", "max"),
           course_enrollment=("MAX_ENROLLMENT", "max")
       )
)

people["person_key"] = norm_key(people["iap_subject_person_key"])
people["person_name"] = people["PERSON_NAME"].astype("string").str.strip()
people["person_email"] = people["PERSON_EMAIL"].replace(r"^\s*$", pd.NA, regex=True).astype("string").str.strip()

if "table_8" in tables and not tables["table_8"].empty:
    directory = tables["table_8"].copy()
    directory["dir_name_norm"] = norm_name(
        directory["FIRST_NAME"].fillna("").astype("string") + " " + directory["LAST_NAME"].fillna("").astype("string")
    )
    directory["dir_email"] = directory["EMAIL_ADDRESS"].replace(r"^\s*$", pd.NA, regex=True).astype("string").str.strip()
    directory = (
        directory.dropna(subset=["dir_name_norm", "dir_email"])
                 .drop_duplicates("dir_name_norm")[["dir_name_norm", "dir_email"]]
    )

    people["person_name_norm"] = norm_name(people["person_name"])
    people = people.merge(
        directory,
        left_on="person_name_norm",
        right_on="dir_name_norm",
        how="left"
    )
    people["person_email"] = people["person_email"].combine_first(people["dir_email"])

people_unique = people[["person_key", "person_name", "person_email"]].drop_duplicates()

joined = iap_subjects.merge(people_unique, on="person_key", how="left")

joined = joined.drop_duplicates(
    subset=["person_name", "person_email", "academic_year", "subject_key"]
)

out = (
    joined.groupby(["person_email", "person_name", "academic_year"], dropna=False, as_index=False)
          .agg(
              total_number_of_iap_subjects=("subject_key", lambda s: s.nunique(dropna=False)),
              minimum_fee=("fee", "min"),
              maximum_fee=("fee", "max"),
              total_course_enrollment=("course_enrollment", lambda s: s.sum(min_count=1))
          )
          .rename(columns={
              "person_email": "individual_email",
              "person_name": "individual_name"
          })
          .sort_values(["individual_name", "academic_year"], na_position="last")
          .reset_index(drop=True)
)

result = {
    "individual_iap_summary": out
}
