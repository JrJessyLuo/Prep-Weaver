import pandas as pd
import numpy as np

# Source input tables from provided `tables` dict
tip_material = tables['table_1']
tip_detail = tables['table_2']
tip_subject_offered = tables['table_4']

# Keep only needed columns
needed_tm_cols = [
    "TIP_MATERIAL_KEY", "ISBN", "TITLE", "AUTHOR", "EDITION", "PUBLISHER",
    "YEAR", "NEW_SHELF_PRICE", "USED_SHELF_PRICE", "RENTAL_NEW_PRICE",
    "RENTAL_USED_PRICE", "MATERIAL_INFO_SOURCE"
]
needed_td_cols = [
    "TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY", "TIP_MATERIAL_STATUS_KEY",
    "TERM_CODE", "subject_id", "ISBN", "RECORD_COUNT", "WAREHOUSE_LOAD_DATE"
]
needed_tso_cols = [
    "TIP_SUBJECT_OFFERED_KEY", "TERM_CODE", "IS_NO_COURSE_MATERIAL",
    "MASTER_COURSE_NUMBER", "MASTER_COURSE_NUMBER_SORT", "MASTER_COURSE_NUMBER_DESC",
    "MASTER_SUBJECT_ID", "MASTER_SUBJECT_ID_SORT", "COURSE_NUMBER", "COURSE_NUMBER_SORT",
    "COURSE_NUMBER_DESC", "SUBJECT_ID", "SUBJECT_ID_SORT", "SUBJECT_TITLE",
    "OFFER_DEPT_CODE", "OFFER_DEPT_NAME", "OFFER_SCHOOL_NAME", "RESPONSIBLE_FACULTY_NAME",
    "RESPONSIBLE_FACULTY_MIT_ID", "NUM_ENROLLED_STUDENTS", "WAREHOUSE_LOAD_DATE"
]

tm = tip_material.loc[:, [c for c in needed_tm_cols if c in tip_material.columns]].copy()
td = tip_detail.loc[:, [c for c in needed_td_cols if c in tip_detail.columns]].copy()
tso = tip_subject_offered.loc[:, [c for c in needed_tso_cols if c in tip_subject_offered.columns]].copy()

# 2) Clean "no materials" records from TIP_MATERIAL and flag-only "no material" in TSO
no_material_mask_tm = (
    tm["TITLE"].astype(str).str.contains("Course has no materials", case=False, na=False)
    | tm["TIP_MATERIAL_KEY"].astype(str).str.contains("Course has no materials", case=False, na=False)
)
tm_clean = tm.loc[~no_material_mask_tm].copy()

if "IS_NO_COURSE_MATERIAL" in tso.columns:
    tso_no_mat_mask = tso["IS_NO_COURSE_MATERIAL"].astype(str).str.upper().isin(["Y", "YES", "TRUE", "T", "1"])
    tso_clean = tso.loc[~tso_no_mat_mask].copy()
else:
    tso_clean = tso.copy()

# Prepare helper: standardized ISBN (strip, remove hyphens/spaces) for better ISBN merge
def norm_isbn(s):
    if pd.isna(s):
        return np.nan
    s = str(s)
    s = s.replace("-", "").replace(" ", "")
    return s if len(s) > 0 else np.nan

td["ISBN_NORM"] = td["ISBN"].map(norm_isbn) if "ISBN" in td.columns else np.nan
tm_clean["ISBN_NORM"] = tm_clean["ISBN"].map(norm_isbn) if "ISBN" in tm_clean.columns else np.nan

# 3) Left merge TIP_DETAIL → TIP_MATERIAL on TIP_MATERIAL_KEY
td_tm_key = td.merge(
    tm_clean,
    on="TIP_MATERIAL_KEY",
    how="left",
    suffixes=("_TD", "_TMKEY")
)

# 4) Separately merge TIP_DETAIL → TIP_MATERIAL on normalized ISBN
merge_cols_for_isbn = [c for c in tm_clean.columns if c not in ["TIP_MATERIAL_KEY", "ISBN_NORM"]]
td_tm_isbn = td.merge(
    tm_clean[["ISBN_NORM"] + merge_cols_for_isbn],
    on="ISBN_NORM",
    how="left",
    suffixes=("_TD", "_TMISBN")
)

# 5) Coalesce fields: prefer key-join fields, then fallback to ISBN-join fields
td_tm_key = td_tm_key.reset_index(drop=True)
td_tm_isbn = td_tm_isbn.reset_index(drop=True)

material_cols = [
    "ISBN", "TITLE", "AUTHOR", "EDITION", "PUBLISHER", "YEAR",
    "NEW_SHELF_PRICE", "USED_SHELF_PRICE", "RENTAL_NEW_PRICE", "RENTAL_USED_PRICE", "MATERIAL_INFO_SOURCE"
]

coalesced_material = {}
for c in material_cols:
    key_name = c if c in td_tm_key.columns else (f"{c}_TMKEY" if f"{c}_TMKEY" in td_tm_key.columns else None)
    isbn_name = f"{c}_TMISBN" if f"{c}_TMISBN" in td_tm_isbn.columns else (c if c in td_tm_isbn.columns else None)
    left_series = td_tm_key[key_name] if key_name else pd.Series(index=td_tm_key.index, dtype=object)
    right_series = td_tm_isbn[isbn_name] if isbn_name else pd.Series(index=td_tm_isbn.index, dtype=object)
    coalesced_material[c] = pd.Series(left_series).combine_first(pd.Series(right_series))

coalesced_material_df = pd.DataFrame(coalesced_material)

# Build base merged frame starting from TIP_DETAIL columns
base_cols = [c for c in td.columns] + ["ISBN_NORM"]
merged_base = td_tm_key[[c for c in base_cols if c in td_tm_key.columns]].copy()

# Attach coalesced material columns
merged_with_material = pd.concat([merged_base, coalesced_material_df], axis=1)

# 6) Merge with TIP_SUBJECT_OFFERED to bring course metadata
tso_subset_cols = ["TIP_SUBJECT_OFFERED_KEY", "SUBJECT_TITLE", "SUBJECT_ID", "COURSE_NUMBER", "TERM_CODE"]
tso_subset_cols = [c for c in tso_subset_cols if c in tso_clean.columns]
merged_all = merged_with_material.merge(
    tso_clean[tso_subset_cols],
    on="TIP_SUBJECT_OFFERED_KEY",
    how="left",
    suffixes=("", "_TSO")
)

# 7) Filtering: remove rows where both TITLE and ISBN are missing; and where any price > 0
def safe_num(x):
    try:
        return float(x)
    except Exception:
        return np.nan

id_mask = merged_all["TITLE"].astype(str).str.strip().ne("").fillna(False) | merged_all["ISBN"].astype(str).str.strip().ne("").fillna(False)

price_cols = ["NEW_SHELF_PRICE", "USED_SHELF_PRICE", "RENTAL_NEW_PRICE", "RENTAL_USED_PRICE"]
for pc in price_cols:
    if pc not in merged_all.columns:
        merged_all[pc] = np.nan

price_gt0_mask = (
    merged_all[price_cols]
    .applymap(safe_num)
    .gt(0)
    .any(axis=1)
)

final_df = merged_all.loc[id_mask & price_gt0_mask].copy()

# 8) Build final answer to the question:
# - For each subject title, list material title, ISBN, new shelf price
# - Compute total cost of new materials per subject title
# - Sort by individual item new shelf price ascending
final_df["NEW_SHELF_PRICE_NUM"] = final_df["NEW_SHELF_PRICE"].map(safe_num)

# Compute total new material cost per subject title
total_new_by_subject = (
    final_df.groupby("SUBJECT_TITLE", dropna=False)["NEW_SHELF_PRICE_NUM"]
    .sum(min_count=1)
    .reset_index()
    .rename(columns={"NEW_SHELF_PRICE_NUM": "TOTAL_NEW_MATERIAL_COST"})
)

answer = final_df.merge(
    total_new_by_subject,
    on="SUBJECT_TITLE",
    how="left"
)

# Select and sort columns
answer_cols = [
    "SUBJECT_TITLE",
    "TITLE",
    "ISBN",
    "NEW_SHELF_PRICE_NUM",
    "TOTAL_NEW_MATERIAL_COST"
]
answer = answer[answer_cols].rename(columns={"NEW_SHELF_PRICE_NUM": "NEW_SHELF_PRICE"}).sort_values(by=["NEW_SHELF_PRICE", "SUBJECT_TITLE", "TITLE"], ascending=[True, True, True]).reset_index(drop=True)

# Package final result
result = {
    "subject_material_prices_and_totals": answer
}