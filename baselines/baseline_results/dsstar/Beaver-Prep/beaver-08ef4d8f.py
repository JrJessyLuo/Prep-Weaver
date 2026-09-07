import pandas as pd
import numpy as np

# Source tables from provided `tables` dict
TIP_MATERIAL = tables['table_1']
TIP_DETAIL = tables['table_2']
TIP_SUBJECT_OFFERED = tables['table_3']
TIP_MATERIAL_STATUS = tables['table_4']

# Select only columns we need from each side to keep the result tidy
detail_cols_keep = [
    "TIP_SUBJECT_OFFERED_KEY",
    "TIP_MATERIAL_KEY",
    "TIP_MATERIAL_STATUS_KEY",
    "TERM_CODE",
    "subject_id",
    "ISBN",
    "RECORD_COUNT"
]

subj_cols_keep = [
    "TIP_SUBJECT_OFFERED_KEY",
    "COURSE_NUMBER",
    "SUBJECT_TITLE",
    "OFFER_SCHOOL_NAME"
]

status_cols_keep = [
    "tip_material_status_key",
    "TIP_MATERIAL_STATUS_CODE",
    "TIP_MATERIAL_STATUS"
]

material_cols_keep = [
    "TIP_MATERIAL_KEY",
    "NEW_SHELF_PRICE",
    "USED_SHELF_PRICE",
    "RENTAL_NEW_PRICE",
    "RENTAL_USED_PRICE"
]

# Defensive column intersection to avoid KeyErrors if schemas differ slightly
detail_cols_keep = [c for c in detail_cols_keep if c in TIP_DETAIL.columns]
subj_cols_keep = [c for c in subj_cols_keep if c in TIP_SUBJECT_OFFERED.columns]
status_cols_keep = [c for c in status_cols_keep if c in TIP_MATERIAL_STATUS.columns]
material_cols_keep = [c for c in material_cols_keep if c in TIP_MATERIAL.columns]

detail_slim = TIP_DETAIL[detail_cols_keep].copy()
subj_slim = TIP_SUBJECT_OFFERED[subj_cols_keep].copy()
status_slim = TIP_MATERIAL_STATUS[status_cols_keep].copy()
material_slim = TIP_MATERIAL[material_cols_keep].copy()

# Perform joins to reproduce the same logic as the reference
joined_df = (
    detail_slim
    .merge(subj_slim, on="TIP_SUBJECT_OFFERED_KEY", how="left")
    .merge(status_slim, left_on="TIP_MATERIAL_STATUS_KEY", right_on="tip_material_status_key", how="left")
    .merge(material_slim, on="TIP_MATERIAL_KEY", how="left")
)

# Ensure price columns are numeric for aggregations
for col in ["NEW_SHELF_PRICE", "USED_SHELF_PRICE"]:
    if col in joined_df.columns:
        joined_df[col] = pd.to_numeric(joined_df[col], errors="coerce")

# Build aggregation asked by the question:
# For each TIP subject and material status:
# - course number
# - subject title
# - material status
# - total, min, max new shelf price
# - total, min, max used shelf price
# - total number of schools
# - total number of materials
group_keys = []
if "COURSE_NUMBER" in joined_df.columns:
    group_keys.append("COURSE_NUMBER")
if "SUBJECT_TITLE" in joined_df.columns:
    group_keys.append("SUBJECT_TITLE")
if "TIP_MATERIAL_STATUS" in joined_df.columns:
    group_keys.append("TIP_MATERIAL_STATUS")

# Helper for distinct schools and materials
# Distinct schools: count nunique of OFFER_SCHOOL_NAME per group
# Total number of materials: count nunique of TIP_MATERIAL_KEY per group
agg_dict = {}
if "NEW_SHELF_PRICE" in joined_df.columns:
    agg_dict["NEW_SHELF_PRICE"] = ["sum", "min", "max"]
if "USED_SHELF_PRICE" in joined_df.columns:
    agg_dict["USED_SHELF_PRICE"] = ["sum", "min", "max"]

# Perform aggregation
grp = joined_df.groupby(group_keys, dropna=False)

agg_prices = grp.agg(agg_dict) if agg_dict else pd.DataFrame(index=grp.size().index)
if not agg_prices.empty:
    # Flatten columns
    agg_prices.columns = [
        f"{col[0]}_{col[1]}".lower() for col in agg_prices.columns.to_flat_index()
    ]
    agg_prices = agg_prices.reset_index()
else:
    agg_prices = grp.size().reset_index(name="row_count")

# Distinct schools and materials
schools = grp["OFFER_SCHOOL_NAME"].nunique(dropna=True).reset_index(name="total_num_schools") if "OFFER_SCHOOL_NAME" in joined_df.columns else grp.size().reset_index(name="total_num_schools")
materials = grp["TIP_MATERIAL_KEY"].nunique(dropna=True).reset_index(name="total_num_materials") if "TIP_MATERIAL_KEY" in joined_df.columns else grp.size().reset_index(name="total_num_materials")

# Merge all parts
final = agg_prices.merge(schools, on=group_keys, how="left").merge(materials, on=group_keys, how="left")

# Rename columns to match question phrasing
rename_map = {
    "COURSE_NUMBER": "course_number",
    "SUBJECT_TITLE": "subject_title",
    "TIP_MATERIAL_STATUS": "material_status",
    "new_shelf_price_sum": "total_new_shelf_price",
    "new_shelf_price_min": "min_new_shelf_price",
    "new_shelf_price_max": "max_new_shelf_price",
    "used_shelf_price_sum": "total_used_shelf_price",
    "used_shelf_price_min": "min_used_shelf_price",
    "used_shelf_price_max": "max_used_shelf_price",
}
final = final.rename(columns=rename_map)

# Order columns
ordered_cols = [
    "course_number",
    "subject_title",
    "material_status",
    "total_new_shelf_price",
    "min_new_shelf_price",
    "max_new_shelf_price",
    "total_used_shelf_price",
    "min_used_shelf_price",
    "max_used_shelf_price",
    "total_num_schools",
    "total_num_materials",
]
# Keep existing ones in proper order
final_cols = [c for c in ordered_cols if c in final.columns] + [c for c in final.columns if c not in ordered_cols]
final = final[final_cols]

# Assign to result dict as required
result = {
    "tip_subject_material_status_agg": final
}