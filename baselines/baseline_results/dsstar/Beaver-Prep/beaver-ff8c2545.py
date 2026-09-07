import pandas as pd

# Source input DataFrames from the provided 'tables' dict
df_detail = tables['table_1']
df_catalog = tables['table_2']

# Normalize key column names for merge
left_key = "LIBRARY_RESERVE_CATALOG_KEY"
right_key = "library_reserve_catalog_key"

# Select only necessary columns from catalog
catalog_cols = [right_key, "CATALOG_YEAR", "CATALOG_TITLE"]
df_catalog_slim = df_catalog[catalog_cols].copy()

# Perform inner merge
df_merged = df_detail.merge(
    df_catalog_slim,
    how="inner",
    left_on=left_key,
    right_on=right_key
)

# Drop the duplicate key column from catalog side
df_merged = df_merged.drop(columns=[right_key])

# Compute per CATALOG_YEAR aggregates
# - total count of records
# - average title length (len of CATALOG_TITLE)
# - distinct count of LIBRARY_MATERIAL_STATUS_KEY
# - distinct count of SUBJECT_ID
df_merged["TITLE_LEN"] = df_merged["CATALOG_TITLE"].fillna("").astype(str).str.len()

agg_df = (
    df_merged.groupby("CATALOG_YEAR", dropna=False)
    .agg(
        total_records=("CATALOG_TITLE", "size"),
        avg_title_length=("TITLE_LEN", "mean"),
        distinct_material_status=("LIBRARY_MATERIAL_STATUS_KEY", "nunique"),
        distinct_subject_id=("SUBJECT_ID", "nunique"),
    )
    .reset_index()
)

# Ensure CATALOG_YEAR is numeric for proper sorting if needed
if not pd.api.types.is_numeric_dtype(agg_df["CATALOG_YEAR"]):
    agg_df["CATALOG_YEAR"] = pd.to_numeric(agg_df["CATALOG_YEAR"], errors="coerce")

# Sort by CATALOG_YEAR descending (placing NaN at the end)
agg_df = agg_df.sort_values(by="CATALOG_YEAR", ascending=False, na_position="last").reset_index(drop=True)

# Prepare final answer
final_cols = ["CATALOG_YEAR", "total_records", "avg_title_length", "distinct_material_status", "distinct_subject_id"]
answer_df = agg_df[final_cols].copy()

# Assign to result as required
result = {"yearly_reserve_materials_summary": answer_df}