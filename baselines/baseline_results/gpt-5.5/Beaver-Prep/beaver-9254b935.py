import pandas as pd
import numpy as np

def normalize_term(series):
    return series.astype("string").str.strip().str.upper()

def term_year(term_series):
    return pd.to_numeric(term_series.astype("string").str.extract(r"^(\d{4})", expand=False), errors="coerce")

def term_suffix(term_series):
    return term_series.astype("string").str.extract(r"(\D{2})$", expand=False).str.upper()

season_order_map = {"JA": 1, "SP": 2, "SU": 3, "FA": 4}
season_desc_map = {
    "JA": "January",
    "SP": "Spring",
    "SU": "Summer",
    "FA": "Fall"
}

# TIP subjects offered / enrollment / schools
tip_subjects = tables["table_3"].copy()
tip_subjects["TERM_CODE"] = normalize_term(tip_subjects["TERM_CODE"])
tip_subjects = tip_subjects[tip_subjects["TERM_CODE"].notna() & (tip_subjects["TERM_CODE"] != "")]

subjects_agg = (
    tip_subjects
    .groupby("TERM_CODE", dropna=False)
    .agg(
        total_tip_subjects_offered=("TIP_SUBJECT_OFFERED_KEY", "nunique"),
        min_num_enrolled_students=("NUM_ENROLLED_STUDENTS", "min"),
        max_num_enrolled_students=("NUM_ENROLLED_STUDENTS", "max"),
        total_schools_offering_subjects=("OFFER_SCHOOL_NAME", "nunique")
    )
    .reset_index()
)

# TIP materials / record counts
tip_materials = tables["table_1"].copy()
tip_materials["TERM_CODE"] = normalize_term(tip_materials["TERM_CODE"])
tip_materials = tip_materials[tip_materials["TERM_CODE"].notna() & (tip_materials["TERM_CODE"] != "")]

record_agg = (
    tip_materials
    .groupby("TERM_CODE", dropna=False)
    .agg(total_records=("RECORD_COUNT", "sum"))
    .reset_index()
)

material_key = tip_materials["TIP_MATERIAL_KEY"].astype("string").str.strip()
material_status = tip_materials["TIP_MATERIAL_STATUS_KEY"].astype("string").str.strip().str.upper()

has_real_material = (
    material_key.notna()
    & (material_key != "")
    & ~material_key.str.contains("NO MATERIAL", case=False, na=False)
    & (material_status != "NM")
)

materials_agg = (
    tip_materials.loc[has_real_material]
    .groupby("TERM_CODE", dropna=False)
    .agg(total_materials_needed=("TIP_MATERIAL_KEY", "nunique"))
    .reset_index()
)

# Combine all term-level aggregates
all_terms = pd.DataFrame({
    "TERM_CODE": pd.concat(
        [
            subjects_agg["TERM_CODE"],
            record_agg["TERM_CODE"],
            materials_agg["TERM_CODE"]
        ],
        ignore_index=True
    ).drop_duplicates()
})

out = (
    all_terms
    .merge(subjects_agg, on="TERM_CODE", how="left")
    .merge(materials_agg, on="TERM_CODE", how="left")
    .merge(record_agg, on="TERM_CODE", how="left")
)

# Term description and current-term flag inferred from TERM_CODE
out["_term_year"] = term_year(out["TERM_CODE"])
out["_term_suffix"] = term_suffix(out["TERM_CODE"])
out["_term_order"] = out["_term_suffix"].map(season_order_map)

out["term_description"] = (
    out["_term_suffix"].map(season_desc_map).fillna(out["_term_suffix"].astype("string"))
    + " "
    + out["_term_year"].astype("Int64").astype("string")
)

max_sort_value = out[["_term_year", "_term_order"]].dropna().sort_values(
    ["_term_year", "_term_order"]
).tail(1)

if len(max_sort_value):
    max_year = max_sort_value["_term_year"].iloc[0]
    max_order = max_sort_value["_term_order"].iloc[0]
    out["is_current_term"] = np.where(
        (out["_term_year"] == max_year) & (out["_term_order"] == max_order),
        "Y",
        "N"
    )
else:
    out["is_current_term"] = "N"

count_cols = [
    "total_tip_subjects_offered",
    "total_materials_needed",
    "total_schools_offering_subjects",
    "total_records"
]
out[count_cols] = out[count_cols].fillna(0).astype("int64")

result_df = (
    out
    .sort_values(["_term_year", "_term_order", "TERM_CODE"], na_position="last")
    [[
        "TERM_CODE",
        "term_description",
        "is_current_term",
        "total_tip_subjects_offered",
        "total_materials_needed",
        "min_num_enrolled_students",
        "max_num_enrolled_students",
        "total_schools_offering_subjects",
        "total_records"
    ]]
    .reset_index(drop=True)
)

result = {
    "term_tip_subject_material_summary": result_df
}
