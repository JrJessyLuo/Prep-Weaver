import pandas as pd

# Load DataFrames from provided `tables` dict
lib_matrl_detail = tables['table_1']  # LIBRARY_RESERVE_MATRL_DETAIL.pkl
lib_matrl_status = tables['table_4']  # LIBRARY_MATERIAL_STATUS.pkl
lib_catalog = tables['table_7']       # LIBRARY_RESERVE_CATALOG.pkl

# Ensure key columns exist
required_cols_detail = {"LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_RESERVE_CATALOG_KEY", "SUBJECT_ID"}
required_cols_status = {"LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS"}
required_cols_catalog = {"library_reserve_catalog_key", "CATALOG_YEAR"}

missing = []
if not required_cols_detail.issubset(lib_matrl_detail.columns):
    missing += [f"LIBRARY_RESERVE_MATRL_DETAIL missing {list(required_cols_detail - set(lib_matrl_detail.columns))}"]
if not required_cols_status.issubset(lib_matrl_status.columns):
    missing += [f"LIBRARY_MATERIAL_STATUS missing {list(required_cols_status - set(lib_matrl_status.columns))}"]
if not required_cols_catalog.issubset(lib_catalog.columns):
    missing += [f"LIBRARY_RESERVE_CATALOG missing {list(required_cols_catalog - set(lib_catalog.columns))}"]
if missing:
    raise ValueError(" | ".join(missing))

# Harmonize key dtypes
lib_matrl_detail = lib_matrl_detail.copy()
lib_matrl_status = lib_matrl_status.copy()
lib_matrl_detail["LIBRARY_MATERIAL_STATUS_KEY"] = lib_matrl_detail["LIBRARY_MATERIAL_STATUS_KEY"].astype(str)
lib_matrl_status["LIBRARY_MATERIAL_STATUS_KEY"] = lib_matrl_status["LIBRARY_MATERIAL_STATUS_KEY"].astype(str)

# Join detail with status
detail_status = lib_matrl_detail.merge(
    lib_matrl_status[["LIBRARY_MATERIAL_STATUS_KEY", "LIBRARY_MATERIAL_STATUS"]],
    on="LIBRARY_MATERIAL_STATUS_KEY",
    how="left",
    validate="m:1"
)

# Harmonize catalog key name and join with catalog for year
detail_status = detail_status.rename(columns={"LIBRARY_RESERVE_CATALOG_KEY": "library_reserve_catalog_key"})
detail_status_catalog = detail_status.merge(
    lib_catalog[["library_reserve_catalog_key", "CATALOG_YEAR"]],
    on="library_reserve_catalog_key",
    how="left",
    validate="m:1"
)

# Derive school code from SUBJECT_ID (split at first dot)
def derive_school(subject_id):
    if pd.isna(subject_id):
        return pd.NA
    s = str(subject_id)
    return s.split(".", 1)[0]

detail_status_catalog["SCHOOL_CODE"] = detail_status_catalog["SUBJECT_ID"].apply(derive_school)

# Aggregate as per reference logic
agg_result = (
    detail_status_catalog
    .groupby("LIBRARY_MATERIAL_STATUS", dropna=False)
    .agg(
        total_distinct_materials=("library_reserve_catalog_key", pd.Series.nunique),
        total_distinct_subjects=("SUBJECT_ID", pd.Series.nunique),
        total_distinct_schools=("SCHOOL_CODE", pd.Series.nunique),
        max_catalog_year=("CATALOG_YEAR", "max"),
    )
    .reset_index()
    .sort_values("LIBRARY_MATERIAL_STATUS", na_position="last")
)

# Assign to result dict as required
result = {
    "material_status_summary": agg_result
}