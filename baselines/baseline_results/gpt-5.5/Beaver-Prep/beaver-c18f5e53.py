import pandas as pd

def norm_text_key(s):
    return s.astype("string").str.strip().str.upper()

material_status = tables["table_1"].copy()
course_materials = tables["table_3"].copy()
subjects = tables["table_4"].copy()
catalog = tables["table_6"].copy()

catalog["CATALOG_YEAR_NUM"] = pd.to_numeric(catalog["CATALOG_YEAR"], errors="coerce")
catalog_recent = (
    catalog.loc[catalog["CATALOG_YEAR_NUM"] >= 2000, ["library_reserve_catalog_key"]]
    .drop_duplicates()
)

course_materials["catalog_key"] = course_materials["LIBRARY_RESERVE_CATALOG_KEY"]
course_materials["subject_offered_key_norm"] = norm_text_key(course_materials["LIBRARY_SUBJECT_OFFERED_KEY"])
course_materials["material_status_key_norm"] = norm_text_key(course_materials["LIBRARY_MATERIAL_STATUS_KEY"])

subjects["subject_offered_key_norm"] = norm_text_key(subjects["LIBRARY_SUBJECT_OFFERED_KEY"])
subjects_dim = (
    subjects[
        ["subject_offered_key_norm", "OFFER_DEPT_NAME", "NUM_ENROLLED_STUDENTS"]
    ]
    .drop_duplicates(subset=["subject_offered_key_norm"])
)

material_status["material_status_key_norm"] = norm_text_key(material_status["LIBRARY_MATERIAL_STATUS_KEY"])
status_dim = (
    material_status[
        ["material_status_key_norm", "LIBRARY_MATERIAL_STATUS"]
    ]
    .drop_duplicates(subset=["material_status_key_norm"])
)

joined = (
    course_materials
    .merge(
        catalog_recent,
        left_on="catalog_key",
        right_on="library_reserve_catalog_key",
        how="inner"
    )
    .merge(status_dim, on="material_status_key_norm", how="left")
    .merge(subjects_dim, on="subject_offered_key_norm", how="left")
)

detail = (
    joined
    .groupby(["LIBRARY_MATERIAL_STATUS", "OFFER_DEPT_NAME"], dropna=False, as_index=False)
    .agg(
        number_of_associated_catalog_items=("catalog_key", "count"),
        total_num_enrolled_students=("NUM_ENROLLED_STUDENTS", "sum")
    )
    .rename(columns={
        "LIBRARY_MATERIAL_STATUS": "material_status",
        "OFFER_DEPT_NAME": "department_name"
    })
)

status_subtotals = (
    joined
    .groupby(["LIBRARY_MATERIAL_STATUS"], dropna=False, as_index=False)
    .agg(
        number_of_associated_catalog_items=("catalog_key", "count"),
        total_num_enrolled_students=("NUM_ENROLLED_STUDENTS", "sum")
    )
    .rename(columns={"LIBRARY_MATERIAL_STATUS": "material_status"})
)
status_subtotals["department_name"] = "All Departments"

grand_total = pd.DataFrame([{
    "material_status": "Grand Total",
    "department_name": "All Departments",
    "number_of_associated_catalog_items": joined["catalog_key"].count(),
    "total_num_enrolled_students": joined["NUM_ENROLLED_STUDENTS"].sum()
}])

detail["_row_type"] = 0
status_subtotals["_row_type"] = 1
grand_total["_row_type"] = 2

final = pd.concat(
    [detail, status_subtotals, grand_total],
    ignore_index=True,
    sort=False
)

final["_status_sort"] = final["material_status"].astype("string").fillna("")
final["_dept_sort"] = final["department_name"].astype("string").fillna("")
final = (
    final
    .sort_values(["_row_type", "_status_sort", "_dept_sort"], kind="stable")
    .drop(columns=["_row_type", "_status_sort", "_dept_sort"])
    [[
        "material_status",
        "department_name",
        "number_of_associated_catalog_items",
        "total_num_enrolled_students"
    ]]
    .reset_index(drop=True)
)

result = {
    "material_status_department_summary": final
}
