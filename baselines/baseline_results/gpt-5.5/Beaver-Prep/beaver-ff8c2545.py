import pandas as pd

reserves = tables["table_1"].copy()
catalog = tables["table_2"].copy()

# Normalize join keys
catalog = catalog.rename(columns={"library_reserve_catalog_key": "LIBRARY_RESERVE_CATALOG_KEY"})

# Keep one catalog row per reserve catalog key to avoid duplicate inflation
catalog = catalog.drop_duplicates(subset=["LIBRARY_RESERVE_CATALOG_KEY"])

# Join reserve records to catalog metadata
df = reserves.merge(
    catalog[["LIBRARY_RESERVE_CATALOG_KEY", "CATALOG_YEAR", "CATALOG_TITLE"]],
    on="LIBRARY_RESERVE_CATALOG_KEY",
    how="inner"
)

# Compute title length; NaN titles remain NaN and are ignored by mean()
df["title_length"] = df["CATALOG_TITLE"].astype("string").str.len()

out = (
    df.groupby("CATALOG_YEAR", dropna=False)
      .agg(
          total_number_of_reserved_materials=("LIBRARY_RESERVE_CATALOG_KEY", "count"),
          average_length_of_titles=("title_length", "mean"),
          distinct_number_of_status=("LIBRARY_MATERIAL_STATUS_KEY", "nunique"),
          number_of_courses=("LIBRARY_SUBJECT_OFFERED_KEY", "nunique")
      )
      .reset_index()
      .rename(columns={"CATALOG_YEAR": "publication_year"})
      .sort_values("publication_year", ascending=False)
      .reset_index(drop=True)
)

result = {"reserved_materials_by_publication_year": out}
