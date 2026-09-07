import pandas as pd
import numpy as np

def clean_str(s):
    return s.astype("string").str.strip()

def school_from_subject(subject_series):
    s = clean_str(subject_series)
    return s.str.extract(r"^([A-Za-z0-9]+[A-Za-z0-9]*)(?:\.|$)", expand=False)

frames = []

# TIP materials/statuses
tip_fact = tables["table_3"].copy()
tip_status = tables["table_2"].copy()
tip_material = tables["table_8"].copy()

tip_fact["_status_key"] = clean_str(tip_fact["TIP_MATERIAL_STATUS_KEY"])
tip_fact["_material_key"] = clean_str(tip_fact["TIP_MATERIAL_KEY"])
tip_fact["_isbn"] = clean_str(tip_fact["ISBN"])
tip_fact["_subject_id"] = clean_str(tip_fact["subject_id"])
tip_fact["_school_code"] = school_from_subject(tip_fact["subject_id"])

tip_status["_status_key"] = clean_str(tip_status["tip_material_status_key"])
tip_status["_status_label"] = clean_str(tip_status["TIP_MATERIAL_STATUS"])
tip_status["_status_code"] = clean_str(tip_status["TIP_MATERIAL_STATUS_CODE"])
tip_status["_status_label"] = (
    tip_status["_status_label"]
    .replace("", pd.NA)
    .fillna(tip_status["_status_code"].replace("", pd.NA))
    .fillna(tip_status["_status_key"].replace("", pd.NA))
    .fillna("(blank)")
)

tip_material["_material_key"] = clean_str(tip_material["TIP_MATERIAL_KEY"])
tip_material["_isbn"] = clean_str(tip_material["ISBN"])
tip_material["_publication_year"] = pd.to_numeric(tip_material["YEAR"], errors="coerce")
tip_material.loc[tip_material["_publication_year"] <= 0, "_publication_year"] = np.nan

tip_year_by_key = (
    tip_material.dropna(subset=["_material_key"])
    .groupby("_material_key", as_index=False)["_publication_year"]
    .max()
)
tip_year_by_isbn = (
    tip_material.dropna(subset=["_isbn"])
    .groupby("_isbn")["_publication_year"]
    .max()
)

tip = tip_fact.merge(
    tip_status[["_status_key", "_status_label"]],
    on="_status_key",
    how="left"
).merge(
    tip_year_by_key,
    on="_material_key",
    how="left"
)

tip["_publication_year"] = tip["_publication_year"].fillna(tip["_isbn"].map(tip_year_by_isbn))
tip["material_status"] = tip["_status_label"].fillna(tip["_status_key"]).fillna("(unknown)")
tip["material_id"] = "TIP:" + tip["_material_key"].fillna("")
tip["subject_id"] = tip["_subject_id"]
tip["school_code"] = tip["_school_code"]

frames.append(tip[["material_status", "material_id", "subject_id", "school_code", "_publication_year"]])

# Library reserve materials/statuses
lib_fact = tables["table_1"].copy()
lib_status = tables["table_4"].copy()
lib_catalog = tables["table_7"].copy()

lib_fact["_status_key"] = clean_str(lib_fact["LIBRARY_MATERIAL_STATUS_KEY"])
lib_fact["_material_key"] = lib_fact["LIBRARY_RESERVE_CATALOG_KEY"].astype("Int64").astype("string")
lib_fact["_subject_id"] = clean_str(lib_fact["SUBJECT_ID"])
lib_fact["_school_code"] = school_from_subject(lib_fact["SUBJECT_ID"])

lib_status["_status_key"] = clean_str(lib_status["LIBRARY_MATERIAL_STATUS_KEY"])
lib_status["_status_label"] = clean_str(lib_status["LIBRARY_MATERIAL_STATUS"])
lib_status["_status_code"] = clean_str(lib_status["LIBRARY_MATERIAL_STATUS_CODE"])
lib_status["_status_label"] = (
    lib_status["_status_label"]
    .replace("", pd.NA)
    .fillna(lib_status["_status_code"].replace("", pd.NA))
    .fillna(lib_status["_status_key"].replace("", pd.NA))
    .fillna("(blank)")
)

lib_catalog["_material_key"] = lib_catalog["library_reserve_catalog_key"].astype("Int64").astype("string")
lib_catalog["_publication_year"] = pd.to_numeric(lib_catalog["CATALOG_YEAR"], errors="coerce")
lib_catalog.loc[lib_catalog["_publication_year"] <= 0, "_publication_year"] = np.nan

lib_year_by_key = (
    lib_catalog.dropna(subset=["_material_key"])
    .groupby("_material_key", as_index=False)["_publication_year"]
    .max()
)

lib = lib_fact.merge(
    lib_status[["_status_key", "_status_label"]],
    on="_status_key",
    how="left"
).merge(
    lib_year_by_key,
    on="_material_key",
    how="left"
)

lib["material_status"] = lib["_status_label"].fillna(lib["_status_key"]).fillna("(unknown)")
lib["material_id"] = "LIB:" + lib["_material_key"].fillna("")
lib["subject_id"] = lib["_subject_id"]
lib["school_code"] = lib["_school_code"]

frames.append(lib[["material_status", "material_id", "subject_id", "school_code", "_publication_year"]])

combined = pd.concat(frames, ignore_index=True)

answer = (
    combined.groupby("material_status", dropna=False)
    .agg(
        total_number_of_materials=("material_id", "nunique"),
        total_number_of_subjects=("subject_id", "nunique"),
        total_number_of_schools=("school_code", "nunique"),
        most_recent_publication_year=("_publication_year", "max"),
    )
    .reset_index()
)

answer["most_recent_publication_year"] = answer["most_recent_publication_year"].round().astype("Int64")
answer = answer.sort_values("material_status").reset_index(drop=True)

result = {"material_status_summary": answer}
