import pandas as pd

# Source input tables from the provided `tables` dict
df_material_status = tables['table_1']          # LIBRARY_MATERIAL_STATUS.pkl
df_reserve_detail = tables['table_3']           # LIBRARY_RESERVE_MATRL_DETAIL.pkl
df_subject_offered = tables['table_10']         # SUBJECT_OFFERED.pkl
df_catalog = tables['table_6']                  # LIBRARY_RESERVE_CATALOG.pkl

# 1) Reproduce the reference logic to keep only reserve details tied to books cataloged on or after 2000
df_catalog_filtered = df_catalog[df_catalog["CATALOG_YEAR"] >= 2000][["library_reserve_catalog_key"]]

df_reserve_detail_2000_plus = df_reserve_detail.merge(
    df_catalog_filtered,
    left_on="LIBRARY_RESERVE_CATALOG_KEY",
    right_on="library_reserve_catalog_key",
    how="inner"
).drop(columns=["library_reserve_catalog_key"])

# 2) Join to material status lookup to get readable status names (if available)
# Attempt to map LIBRARY_MATERIAL_STATUS_KEY to a status name column if present
status_name_col_candidates = [c for c in df_material_status.columns if c.lower() in ("material_status_name", "material_status", "status_name", "status")]
status_name_col = status_name_col_candidates[0] if status_name_col_candidates else None

df_reserve_enriched = df_reserve_detail_2000_plus.merge(
    df_material_status,
    left_on="LIBRARY_MATERIAL_STATUS_KEY",
    right_on="LIBRARY_MATERIAL_STATUS_KEY",
    how="left"
)

# Derive a unified material status label
if status_name_col is not None:
    df_reserve_enriched["MATERIAL_STATUS"] = df_reserve_enriched[status_name_col]
else:
    # Fallback: use the key as the status label if no name is available
    df_reserve_enriched["MATERIAL_STATUS"] = df_reserve_enriched["LIBRARY_MATERIAL_STATUS_KEY"].astype(str)

# 3) Join to SUBJECT_OFFERED to get department and enrolled info
# Identify likely join keys
# Commonly LIBRARY_RESERVE_MATRL_DETAIL has SUBJECT_OFFERED_KEY to join to SUBJECT_OFFERED
join_key_candidates = [c for c in ["SUBJECT_OFFERED_KEY", "subject_offered_key"] if c in df_reserve_enriched.columns and c in df_subject_offered.columns]
if join_key_candidates:
    join_key = join_key_candidates[0]
else:
    # If no clear join key, assume SUBJECT_OFFERED_KEY
    join_key = "SUBJECT_OFFERED_KEY"

df_joined = df_reserve_enriched.merge(
    df_subject_offered,
    left_on=join_key,
    right_on=join_key,
    how="left",
    suffixes=("", "_SUBJ")
)

# Detect department and enrolled columns
dept_col_candidates = [c for c in df_joined.columns if c.lower() in ("department_name", "dept_name", "department", "dept")]
dept_col = dept_col_candidates[0] if dept_col_candidates else None

enrolled_col_candidates = [c for c in df_joined.columns if c.lower() in ("enrolled", "enrollment", "enrolled_students", "num_enrolled", "enrolled_count")]
enrolled_col = enrolled_col_candidates[0] if enrolled_col_candidates else None

# Fallbacks if columns not found: create placeholders
if dept_col is None:
    df_joined["DEPARTMENT_NAME"] = "Unknown Department"
    dept_col = "DEPARTMENT_NAME"

if enrolled_col is None:
    df_joined["ENROLLED"] = 0
    enrolled_col = "ENROLLED"

# 4) Compute per (Material Status, Department) metrics
# - number of associated catalog items: count distinct LIBRARY_RESERVE_CATALOG_KEY
# - total number of enrolled students: sum of enrolled
catalog_key_col = "LIBRARY_RESERVE_CATALOG_KEY"
if catalog_key_col not in df_joined.columns:
    # If missing, fall back to counting rows
    df_joined[catalog_key_col] = df_joined.index

group_cols = ["MATERIAL_STATUS", dept_col]
agg_df = df_joined.groupby(group_cols).agg(
    NUM_CATALOG_ITEMS=(catalog_key_col, pd.Series.nunique),
    TOTAL_ENROLLED=(enrolled_col, "sum")
).reset_index()

# 5) Add subtotals for each material status (department = 'Subtotal')
subtotals = agg_df.groupby("MATERIAL_STATUS").agg(
    NUM_CATALOG_ITEMS=("NUM_CATALOG_ITEMS", "sum"),
    TOTAL_ENROLLED=("TOTAL_ENROLLED", "sum")
).reset_index()
subtotals[dept_col] = "Subtotal"

# 6) Add grand total across all statuses (status = 'Grand Total', department = 'Grand Total')
grand_total = pd.DataFrame({
    "MATERIAL_STATUS": ["Grand Total"],
    dept_col: ["Grand Total"],
    "NUM_CATALOG_ITEMS": [agg_df["NUM_CATALOG_ITEMS"].sum()],
    "TOTAL_ENROLLED": [agg_df["TOTAL_ENROLLED"].sum()]
})

# 7) Combine detail, subtotals, and grand total
final_df = pd.concat([agg_df, subtotals, grand_total], ignore_index=True)

# Optional ordering: sort by MATERIAL_STATUS, with Grand Total at end and Subtotal last within each status
def sort_keys(row):
    status = row["MATERIAL_STATUS"]
    dept = row[dept_col]
    status_order = (1, status) if status != "Grand Total" else (2, "")
    dept_order = (1, dept.lower()) if dept not in ("Subtotal", "Grand Total") else (2 if dept == "Subtotal" else 3, "")
    return status_order + dept_order

final_df = final_df.sort_values(by=list(final_df.columns), key=lambda col: None)  # no-op to keep structure
final_df = final_df.sort_values(by=["MATERIAL_STATUS", dept_col], key=None)
# Refine ordering with a helper sort dataframe
order_df = final_df.apply(sort_keys, axis=1, result_type="expand")
final_df = final_df.iloc[order_df.sort_values(list(range(order_df.shape[1]))).index].reset_index(drop=True)

# Rename columns to match the question phrasing
final_df = final_df.rename(columns={
    "MATERIAL_STATUS": "Material Status",
    dept_col: "Department Name",
    "NUM_CATALOG_ITEMS": "Number of Associated Catalog Items",
    "TOTAL_ENROLLED": "Total Enrolled Students"
})

# Assign to result as required
result = {
    "material_status_department_summary": final_df
}