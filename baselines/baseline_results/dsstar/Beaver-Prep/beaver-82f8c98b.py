import pandas as pd
import numpy as np

# The input tables are provided in a dict named `tables`
tip_subject_offered = tables['table_1'].copy()
tip_detail = tables['table_2'].copy()
tip_material = tables['table_5'].copy()

# Minimal checks for required columns
required_tso = {"TIP_SUBJECT_OFFERED_KEY", "TERM_CODE", "OFFER_DEPT_NAME", "NUM_ENROLLED_STUDENTS", "SUBJECT_ID"}
required_tm = {"TIP_MATERIAL_KEY", "RENTAL_NEW_PRICE", "RENTAL_USED_PRICE", "NEW_SHELF_PRICE", "USED_SHELF_PRICE"}
required_td = {"TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY"}

missing_tso = list(required_tso - set(tip_subject_offered.columns))
missing_tm = list(required_tm - set(tip_material.columns))
missing_td = list(required_td - set(tip_detail.columns))
if missing_tso or missing_tm or missing_td:
    raise ValueError(f"Missing columns - TSO: {missing_tso}, TM: {missing_tm}, TD: {missing_td}")

# Clean keys to consistent string to avoid merge mismatches
def to_str(s):
    return s.astype(str)

tip_subject_offered["TIP_SUBJECT_OFFERED_KEY"] = to_str(tip_subject_offered["TIP_SUBJECT_OFFERED_KEY"])
tip_detail["TIP_SUBJECT_OFFERED_KEY"] = to_str(tip_detail["TIP_SUBJECT_OFFERED_KEY"])
tip_detail["TIP_MATERIAL_KEY"] = to_str(tip_detail["TIP_MATERIAL_KEY"])
tip_material["TIP_MATERIAL_KEY"] = to_str(tip_material["TIP_MATERIAL_KEY"])

# Join TIP_DETAIL -> TIP_SUBJECT_OFFERED
td_tso = tip_detail.merge(
    tip_subject_offered[
        ["TIP_SUBJECT_OFFERED_KEY", "TERM_CODE", "OFFER_DEPT_NAME", "NUM_ENROLLED_STUDENTS", "SUBJECT_ID"]
    ].rename(columns={"SUBJECT_ID": "TSO_SUBJECT_ID"}),
    on="TIP_SUBJECT_OFFERED_KEY",
    how="left",
    validate="m:1"
)

# Join the result -> TIP_MATERIAL
full_df = td_tso.merge(
    tip_material[
        ["TIP_MATERIAL_KEY", "ISBN", "TITLE", "RENTAL_NEW_PRICE", "RENTAL_USED_PRICE", "NEW_SHELF_PRICE", "USED_SHELF_PRICE"]
    ],
    on="TIP_MATERIAL_KEY",
    how="left",
    validate="m:1"
)

# Coerce numeric prices
price_cols = ["RENTAL_NEW_PRICE", "RENTAL_USED_PRICE", "NEW_SHELF_PRICE", "USED_SHELF_PRICE"]
for c in price_cols:
    full_df[c] = pd.to_numeric(full_df[c], errors="coerce")

# Build analytic dataset
analytic_cols = [
    "TIP_SUBJECT_OFFERED_KEY",
    "TIP_MATERIAL_KEY",
    "TERM_CODE",
    "OFFER_DEPT_NAME",
    "TSO_SUBJECT_ID",
    "NUM_ENROLLED_STUDENTS",
    "ISBN",
    "TITLE",
    "RENTAL_NEW_PRICE",
    "RENTAL_USED_PRICE",
    "NEW_SHELF_PRICE",
    "USED_SHELF_PRICE",
]
analytic = full_df[analytic_cols].copy()

# Aggregation per department:
# - total number of types of TIP subjects (distinct TIP_SUBJECT_OFFERED_KEY)
# - total number of enrolled students (sum NUM_ENROLLED_STUDENTS; deduplicate at subject level to avoid double counting)
# - min and max rental new price (over all materials linked to the department)
# First, compute subject-level enrolled to avoid double counting when multiple materials map to the same subject
subject_level = (
    analytic.groupby(["OFFER_DEPT_NAME", "TIP_SUBJECT_OFFERED_KEY"], dropna=False)
    .agg(enrolled=("NUM_ENROLLED_STUDENTS", "max"))
    .reset_index()
)

dept_enrollment = (
    subject_level.groupby("OFFER_DEPT_NAME", dropna=False)
    .agg(
        total_subject_types=("TIP_SUBJECT_OFFERED_KEY", pd.Series.nunique),
        total_enrolled_students=("enrolled", "sum"),
    )
    .reset_index()
)

dept_price = (
    analytic.groupby("OFFER_DEPT_NAME", dropna=False)
    .agg(
        min_rental_new_price=("RENTAL_NEW_PRICE", "min"),
        max_rental_new_price=("RENTAL_NEW_PRICE", "max"),
    )
    .reset_index()
)

final_df = dept_enrollment.merge(dept_price, on="OFFER_DEPT_NAME", how="left")

# Arrange columns and sort by department name for readability
final_df = final_df.rename(columns={"OFFER_DEPT_NAME": "department_name"})
final_df = final_df[
    ["department_name", "total_subject_types", "total_enrolled_students", "min_rental_new_price", "max_rental_new_price"]
].sort_values(by="department_name", kind="stable")

# Assign to result dict as required
result = {"department_summary": final_df}