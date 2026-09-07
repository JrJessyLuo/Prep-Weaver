import pandas as pd

# Access input tables from the provided `tables` dict
df_detail = tables['table_1']  # LIBRARY_RESERVE_MATRL_DETAIL.pkl
df_catalog = tables['table_6']  # LIBRARY_RESERVE_CATALOG.pkl

# Select only columns needed from catalog to reduce memory and align column name
df_catalog_small = df_catalog[["library_reserve_catalog_key", "CATALOG_TITLE"]].rename(
    columns={"library_reserve_catalog_key": "LIBRARY_RESERVE_CATALOG_KEY"}
)

# Ensure key types are aligned for merge
if df_detail["LIBRARY_RESERVE_CATALOG_KEY"].dtype != df_catalog_small["LIBRARY_RESERVE_CATALOG_KEY"].dtype:
    df_catalog_small["LIBRARY_RESERVE_CATALOG_KEY"] = df_catalog_small["LIBRARY_RESERVE_CATALOG_KEY"].astype(
        df_detail["LIBRARY_RESERVE_CATALOG_KEY"].dtype, errors="ignore"
    )

# Merge to bring CATALOG_TITLE into detail
df_merged = df_detail.merge(df_catalog_small, on="LIBRARY_RESERVE_CATALOG_KEY", how="left")

# Group by CATALOG_TITLE and aggregate as specified
agg_df = (
    df_merged.groupby("CATALOG_TITLE", dropna=False)
    .agg(
        total_reserved=("LIBRARY_RESERVE_CATALOG_KEY", "size"),
        distinct_status_count=("LIBRARY_MATERIAL_STATUS_KEY", pd.Series.nunique),
    )
    .reset_index()
    .sort_values(by="total_reserved", ascending=False)
)

# Assign final result as required
result = {"agg_by_course_title": agg_df}