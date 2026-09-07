import pandas as pd
import numpy as np

def norm_str(s):
    return s.astype("string").str.strip().str.upper().mask(lambda x: x.eq(""))

def norm_isbn(s):
    out = s.astype("string").str.upper().str.replace(r"[^0-9X]", "", regex=True)
    return out.mask(out.eq(""))

def first_non_null(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else pd.NA

def clean_text(s):
    return s.astype("string").str.strip().mask(lambda x: x.eq(""))

tip_fact = tables["table_1"].copy()
tip_subjects = tables["table_6"].copy()
tip_materials = tables["table_4"].copy()

tip_fact["_tip_subject_key_norm"] = norm_str(tip_fact["TIP_SUBJECT_OFFERED_KEY"])
tip_fact["_tip_material_key_norm"] = norm_str(tip_fact["TIP_MATERIAL_KEY"])
tip_fact["_subject_norm"] = norm_str(tip_fact["subject_id"])
tip_fact["_term_norm"] = norm_str(tip_fact["TERM_CODE"])
tip_fact["_isbn_norm"] = norm_isbn(tip_fact["ISBN"])

tip_subjects["_tip_subject_key_norm"] = norm_str(tip_subjects["TIP_SUBJECT_OFFERED_KEY"])
tip_subjects["_subject_norm"] = norm_str(tip_subjects["SUBJECT_ID"])
tip_subjects["_term_norm"] = norm_str(tip_subjects["TERM_CODE"])

tip_dept_by_key = (
    tip_subjects[
        ["_tip_subject_key_norm", "OFFER_DEPT_NAME", "OFFER_DEPT_CODE", "SUBJECT_ID", "TERM_CODE"]
    ]
    .dropna(subset=["_tip_subject_key_norm"])
    .drop_duplicates("_tip_subject_key_norm")
    .rename(
        columns={
            "OFFER_DEPT_NAME": "department_name",
            "OFFER_DEPT_CODE": "department_code",
            "SUBJECT_ID": "tip_subject_id_from_dim",
            "TERM_CODE": "tip_term_code_from_dim",
        }
    )
)

tip = tip_fact.merge(tip_dept_by_key, on="_tip_subject_key_norm", how="left")

tip_dept_by_subject_term = (
    tip_subjects[["_subject_norm", "_term_norm", "OFFER_DEPT_NAME", "OFFER_DEPT_CODE"]]
    .dropna(subset=["_subject_norm", "_term_norm"])
    .drop_duplicates(["_subject_norm", "_term_norm"])
    .rename(
        columns={
            "OFFER_DEPT_NAME": "department_name_fallback",
            "OFFER_DEPT_CODE": "department_code_fallback",
        }
    )
)

tip = tip.merge(tip_dept_by_subject_term, on=["_subject_norm", "_term_norm"], how="left")
tip["department_name"] = tip["department_name"].combine_first(tip["department_name_fallback"])
tip["department_code"] = tip["department_code"].combine_first(tip["department_code_fallback"])

tip_materials["_tip_material_key_norm"] = norm_str(tip_materials["TIP_MATERIAL_KEY"])
tip_materials["_isbn_norm"] = norm_isbn(tip_materials["ISBN"])

mat_by_key = (
    tip_materials.rename(
        columns={
            "ISBN": "material_isbn",
            "TITLE": "tip_material_title",
            "AUTHOR": "tip_material_author",
        }
    )[
        [
            "_tip_material_key_norm",
            "material_isbn",
            "tip_material_title",
            "tip_material_author",
            "_isbn_norm",
        ]
    ]
    .dropna(subset=["_tip_material_key_norm"])
    .groupby("_tip_material_key_norm", as_index=False)
    .agg(
        {
            "material_isbn": first_non_null,
            "tip_material_title": first_non_null,
            "tip_material_author": first_non_null,
            "_isbn_norm": first_non_null,
        }
    )
    .rename(columns={"_isbn_norm": "_isbn_norm_from_material"})
)

tip = tip.merge(mat_by_key, on="_tip_material_key_norm", how="left")
tip["_isbn_norm_final"] = tip["_isbn_norm"].combine_first(tip["_isbn_norm_from_material"])

mat_by_isbn = (
    tip_materials.dropna(subset=["_isbn_norm"])
    .rename(
        columns={
            "ISBN": "material_isbn_by_isbn",
            "TITLE": "tip_material_title_by_isbn",
            "AUTHOR": "tip_material_author_by_isbn",
        }
    )[
        [
            "_isbn_norm",
            "material_isbn_by_isbn",
            "tip_material_title_by_isbn",
            "tip_material_author_by_isbn",
        ]
    ]
    .groupby("_isbn_norm", as_index=False)
    .agg(
        {
            "material_isbn_by_isbn": first_non_null,
            "tip_material_title_by_isbn": first_non_null,
            "tip_material_author_by_isbn": first_non_null,
        }
    )
    .rename(columns={"_isbn_norm": "_isbn_norm_final"})
)

tip = tip.merge(mat_by_isbn, on="_isbn_norm_final", how="left")

tip["tip_material_title"] = tip["tip_material_title"].combine_first(tip["tip_material_title_by_isbn"])
tip["tip_material_author"] = tip["tip_material_author"].combine_first(tip["tip_material_author_by_isbn"])
tip["isbn"] = tip["ISBN"].combine_first(tip["material_isbn"]).combine_first(tip["material_isbn_by_isbn"])

tip["tip_material_title"] = clean_text(tip["tip_material_title"])
tip["tip_material_author"] = clean_text(tip["tip_material_author"])
tip["isbn"] = clean_text(tip["isbn"])
tip["department_name"] = clean_text(tip["department_name"])

status_nm = norm_str(tip["TIP_MATERIAL_STATUS_KEY"]).eq("NM")
title_no_material = tip["tip_material_title"].str.upper().str.contains("COURSE HAS NO MATERIAL", na=False)
key_no_material = (
    tip["TIP_MATERIAL_KEY"]
    .astype("string")
    .str.upper()
    .str.contains("COURSE HAS NO MATERIAL", na=False)
)

tip = tip[
    tip["department_name"].notna()
    & ~(status_nm | title_no_material | key_no_material)
    & (
        tip["isbn"].notna()
        | tip["tip_material_title"].notna()
        | tip["tip_material_author"].notna()
    )
].copy()

lib_fact = tables["table_2"].copy()
lib_catalog = tables["table_3"].copy()
lib_subjects = tables["table_8"].copy()

lib_fact["_library_subject_key_norm"] = norm_str(lib_fact["LIBRARY_SUBJECT_OFFERED_KEY"])
lib_fact["_subject_norm"] = norm_str(lib_fact["SUBJECT_ID"])
lib_fact["_term_norm"] = norm_str(lib_fact["TERM_CODE"])

lib_catalog["_isbn_norm"] = norm_isbn(lib_catalog["CATALOG_ISBN"])

catalog = (
    lib_catalog[
        [
            "library_reserve_catalog_key",
            "CATALOG_TITLE",
            "CATALOG_AUTHOR_NAME",
            "CATALOG_ISBN",
            "_isbn_norm",
        ]
    ]
    .drop_duplicates("library_reserve_catalog_key")
)

lib = lib_fact.merge(
    catalog,
    left_on="LIBRARY_RESERVE_CATALOG_KEY",
    right_on="library_reserve_catalog_key",
    how="left",
)

lib_subjects["_library_subject_key_norm"] = norm_str(lib_subjects["LIBRARY_SUBJECT_OFFERED_KEY"])
lib_subjects["_subject_norm"] = norm_str(lib_subjects["SUBJECT_ID"])
lib_subjects["_term_norm"] = norm_str(lib_subjects["term_code"])

lib_dept_by_key = (
    lib_subjects[["_library_subject_key_norm", "OFFER_DEPT_NAME", "OFFER_DEPT_CODE"]]
    .dropna(subset=["_library_subject_key_norm"])
    .drop_duplicates("_library_subject_key_norm")
    .rename(
        columns={
            "OFFER_DEPT_NAME": "library_department_name",
            "OFFER_DEPT_CODE": "library_department_code",
        }
    )
)

lib = lib.merge(lib_dept_by_key, on="_library_subject_key_norm", how="left")

lib_dept_by_subject_term = (
    lib_subjects[["_subject_norm", "_term_norm", "OFFER_DEPT_NAME", "OFFER_DEPT_CODE"]]
    .dropna(subset=["_subject_norm", "_term_norm"])
    .drop_duplicates(["_subject_norm", "_term_norm"])
    .rename(
        columns={
            "OFFER_DEPT_NAME": "library_department_name_fallback",
            "OFFER_DEPT_CODE": "library_department_code_fallback",
        }
    )
)

lib = lib.merge(lib_dept_by_subject_term, on=["_subject_norm", "_term_norm"], how="left")
lib["library_department_name"] = lib["library_department_name"].combine_first(
    lib["library_department_name_fallback"]
)
lib["library_department_name"] = clean_text(lib["library_department_name"])

lib_availability = (
    lib[
        lib["_isbn_norm"].notna()
        & lib["_subject_norm"].notna()
        & lib["_term_norm"].notna()
    ]
    .groupby(["_isbn_norm", "_subject_norm", "_term_norm"], as_index=False)
    .agg(
        library_term_code=("TERM_CODE", first_non_null),
        reserve_catalog_count=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"),
    )
    .rename(columns={"_isbn_norm": "_isbn_norm_final"})
)

final = tip.merge(
    lib_availability,
    on=["_isbn_norm_final", "_subject_norm", "_term_norm"],
    how="left",
)

final["available_in_library_reserves"] = np.where(
    final["reserve_catalog_count"].fillna(0).gt(0),
    "Available in Library",
    "Not Available in Library",
)

final.loc[
    final["available_in_library_reserves"].eq("Not Available in Library"),
    "library_term_code",
] = pd.NA

dept_metrics = (
    lib[lib["library_department_name"].notna()]
    .groupby("library_department_name", as_index=False)
    .agg(
        total_instructors=("LIBRARY_COURSE_INSTRUCTOR_KEY", "nunique"),
        total_library_books=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"),
    )
)

dept_metrics["total_number_of_instructors_per_library_book"] = np.where(
    dept_metrics["total_library_books"].gt(0),
    dept_metrics["total_instructors"] / dept_metrics["total_library_books"],
    0.0,
)

dept_metrics = dept_metrics.rename(
    columns={
        "library_department_name": "department_name",
        "total_library_books": "total_number_of_materials_available_in_library_for_department",
    }
)

total_available_materials = (
    int(dept_metrics["total_number_of_materials_available_in_library_for_department"].sum())
    if not dept_metrics.empty
    else 0
)

dept_metrics["total_number_of_available_materials_across_all_departments"] = total_available_materials
dept_metrics["_dept_norm"] = norm_str(dept_metrics["department_name"])

final["_dept_norm"] = norm_str(final["department_name"])

final = final.merge(
    dept_metrics[
        [
            "_dept_norm",
            "total_number_of_instructors_per_library_book",
            "total_number_of_materials_available_in_library_for_department",
            "total_number_of_available_materials_across_all_departments",
        ]
    ],
    on="_dept_norm",
    how="left",
)

final["total_number_of_instructors_per_library_book"] = (
    final["total_number_of_instructors_per_library_book"].fillna(0.0)
)
final["total_number_of_materials_available_in_library_for_department"] = (
    final["total_number_of_materials_available_in_library_for_department"].fillna(0).astype(int)
)
final["total_number_of_available_materials_across_all_departments"] = (
    final["total_number_of_available_materials_across_all_departments"]
    .fillna(total_available_materials)
    .astype(int)
)

answer_cols = [
    "department_name",
    "tip_material_title",
    "tip_material_author",
    "isbn",
    "library_term_code",
    "available_in_library_reserves",
    "total_number_of_instructors_per_library_book",
    "total_number_of_materials_available_in_library_for_department",
    "total_number_of_available_materials_across_all_departments",
]

answer = (
    final[answer_cols]
    .drop_duplicates()
    .sort_values(["department_name", "tip_material_title", "tip_material_author", "isbn"], na_position="last")
    .reset_index(drop=True)
)

result = {"department_tip_material_library_reserve_availability": answer}
