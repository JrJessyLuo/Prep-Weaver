import pandas as pd

reserve = tables["table_1"].copy()
courses = tables["table_7"].copy()

# Normalize join keys to handle padded spaces / case differences
reserve["_subject_offered_key_norm"] = (
    reserve["LIBRARY_SUBJECT_OFFERED_KEY"].astype("string").str.strip().str.upper()
)
courses["_subject_offered_key_norm"] = (
    courses["LIBRARY_SUBJECT_OFFERED_KEY"].astype("string").str.strip().str.upper()
)

course_titles = courses[["_subject_offered_key_norm", "SUBJECT_TITLE"]].drop_duplicates()

merged = reserve.merge(
    course_titles,
    on="_subject_offered_key_norm",
    how="inner"
)

out = (
    merged.dropna(subset=["SUBJECT_TITLE"])
    .groupby("SUBJECT_TITLE", as_index=False)
    .agg(
        total_reserved_materials=("LIBRARY_RESERVE_CATALOG_KEY", "count"),
        distinct_material_status_count=("LIBRARY_MATERIAL_STATUS_KEY", pd.Series.nunique),
    )
    .rename(columns={"SUBJECT_TITLE": "course_title"})
    .sort_values("total_reserved_materials", ascending=False)
    .reset_index(drop=True)
)

result = {"course_reserved_material_summary": out}
