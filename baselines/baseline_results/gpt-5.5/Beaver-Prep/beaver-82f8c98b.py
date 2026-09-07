import pandas as pd
import numpy as np

def clean_str(s):
    return s.astype("string").str.strip().replace("", pd.NA)

tip_subjects = tables["table_1"].copy()
tip_subject_materials = tables["table_2"].copy()
materials = tables["table_5"].copy()

tip_subjects["TIP_KEY_N"] = clean_str(tip_subjects["TIP_SUBJECT_OFFERED_KEY"])
tip_subjects["SUBJECT_ID_N"] = clean_str(tip_subjects["SUBJECT_ID"])
tip_subjects["OFFER_DEPT_NAME_N"] = clean_str(tip_subjects["OFFER_DEPT_NAME"])
tip_subjects["NUM_ENROLLED_STUDENTS"] = pd.to_numeric(
    tip_subjects["NUM_ENROLLED_STUDENTS"], errors="coerce"
).fillna(0)

tip_subjects_unique = pd.concat(
    [
        tip_subjects[tip_subjects["TIP_KEY_N"].notna()].drop_duplicates("TIP_KEY_N"),
        tip_subjects[tip_subjects["TIP_KEY_N"].isna()],
    ],
    ignore_index=True,
)

subject_summary = (
    tip_subjects_unique
    .dropna(subset=["OFFER_DEPT_NAME_N"])
    .groupby("OFFER_DEPT_NAME_N", as_index=False)
    .agg(
        total_number_of_tip_subject_types=("SUBJECT_ID_N", "nunique"),
        total_number_of_enrolled_students=("NUM_ENROLLED_STUDENTS", "sum"),
    )
)

tip_subject_materials["TIP_KEY_N"] = clean_str(tip_subject_materials["TIP_SUBJECT_OFFERED_KEY"])
tip_subject_materials["SUBJECT_ID_N"] = clean_str(tip_subject_materials["subject_id"])
tip_subject_materials["MAT_KEY_N"] = clean_str(tip_subject_materials["TIP_MATERIAL_KEY"])
tip_subject_materials["ISBN_N"] = clean_str(tip_subject_materials["ISBN"])

materials["MAT_KEY_N"] = clean_str(materials["TIP_MATERIAL_KEY"])
materials["ISBN_N"] = clean_str(materials["ISBN"])
materials["RENTAL_NEW_PRICE"] = pd.to_numeric(materials["RENTAL_NEW_PRICE"], errors="coerce")

mat_price_by_key = (
    materials
    .dropna(subset=["MAT_KEY_N"])
    .groupby("MAT_KEY_N", as_index=False)
    .agg(
        key_min_rental_new_price=("RENTAL_NEW_PRICE", "min"),
        key_max_rental_new_price=("RENTAL_NEW_PRICE", "max"),
    )
)

mat_price_by_isbn = (
    materials
    .dropna(subset=["ISBN_N"])
    .groupby("ISBN_N", as_index=False)
    .agg(
        isbn_min_rental_new_price=("RENTAL_NEW_PRICE", "min"),
        isbn_max_rental_new_price=("RENTAL_NEW_PRICE", "max"),
    )
)

links_with_prices = (
    tip_subject_materials
    .merge(mat_price_by_key, on="MAT_KEY_N", how="left")
    .merge(mat_price_by_isbn, on="ISBN_N", how="left")
)

links_with_prices["min_rental_new_price"] = links_with_prices["key_min_rental_new_price"].combine_first(
    links_with_prices["isbn_min_rental_new_price"]
)
links_with_prices["max_rental_new_price"] = links_with_prices["key_max_rental_new_price"].combine_first(
    links_with_prices["isbn_max_rental_new_price"]
)

no_material_mask = (
    clean_str(links_with_prices["TIP_MATERIAL_STATUS_KEY"]).eq("NM")
    | links_with_prices["MAT_KEY_N"].str.contains("no materials", case=False, na=False)
)
links_with_prices.loc[no_material_mask, ["min_rental_new_price", "max_rental_new_price"]] = (
    links_with_prices.loc[no_material_mask, ["min_rental_new_price", "max_rental_new_price"]]
    .fillna(0)
)

tip_key_to_dept = (
    tip_subjects_unique[["TIP_KEY_N", "OFFER_DEPT_NAME_N"]]
    .dropna(subset=["TIP_KEY_N", "OFFER_DEPT_NAME_N"])
    .drop_duplicates("TIP_KEY_N")
)

subject_to_dept = (
    tip_subjects_unique[["SUBJECT_ID_N", "OFFER_DEPT_NAME_N"]]
    .dropna(subset=["SUBJECT_ID_N", "OFFER_DEPT_NAME_N"])
    .drop_duplicates()
)

links_exact_dept = links_with_prices.merge(tip_key_to_dept, on="TIP_KEY_N", how="left")

links_fallback_dept = (
    links_exact_dept[links_exact_dept["OFFER_DEPT_NAME_N"].isna()]
    .drop(columns=["OFFER_DEPT_NAME_N"])
    .merge(subject_to_dept, on="SUBJECT_ID_N", how="left")
)

links_priced_by_dept = pd.concat(
    [
        links_exact_dept[links_exact_dept["OFFER_DEPT_NAME_N"].notna()],
        links_fallback_dept,
    ],
    ignore_index=True,
)

price_summary = (
    links_priced_by_dept
    .dropna(subset=["OFFER_DEPT_NAME_N"])
    .groupby("OFFER_DEPT_NAME_N", as_index=False)
    .agg(
        minimum_rental_new_price=("min_rental_new_price", "min"),
        maximum_rental_new_price=("max_rental_new_price", "max"),
    )
)

final_df = (
    subject_summary
    .merge(price_summary, on="OFFER_DEPT_NAME_N", how="left")
    .rename(columns={"OFFER_DEPT_NAME_N": "department_name"})
    .sort_values("department_name")
    .reset_index(drop=True)
)

result = {
    "department_tip_subject_summary": final_df
}
