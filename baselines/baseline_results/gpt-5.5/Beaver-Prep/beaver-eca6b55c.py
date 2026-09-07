import pandas as pd

materials = tables["table_1"].copy()
courses = tables["table_3"][["LIBRARY_COURSE_INSTRUCTOR_KEY", "COURSE_NAME"]].drop_duplicates()
catalog = (
    tables["table_6"][["library_reserve_catalog_key", "CATALOG_YEAR"]]
    .drop_duplicates(subset=["library_reserve_catalog_key"])
    .rename(columns={"library_reserve_catalog_key": "LIBRARY_RESERVE_CATALOG_KEY"})
)

df = (
    materials
    .merge(courses, on="LIBRARY_COURSE_INSTRUCTOR_KEY", how="inner")
    .merge(catalog, on="LIBRARY_RESERVE_CATALOG_KEY", how="left")
)

df["CATALOG_YEAR"] = pd.to_numeric(df["CATALOG_YEAR"], errors="coerce")

answer = (
    df.groupby("COURSE_NAME", as_index=False)
    .agg(
        total_number_of_library_materials=("LIBRARY_RESERVE_CATALOG_KEY", "count"),
        minimum_publication_year=("CATALOG_YEAR", "min"),
        maximum_publication_year=("CATALOG_YEAR", "max"),
        total_number_of_materials_status=("LIBRARY_MATERIAL_STATUS_KEY", "count"),
    )
    .sort_values("COURSE_NAME")
    .reset_index(drop=True)
)

result = {"course_library_material_summary": answer}
