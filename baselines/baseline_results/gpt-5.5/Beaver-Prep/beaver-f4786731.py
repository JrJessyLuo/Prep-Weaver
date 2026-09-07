import pandas as pd

course_instructors = tables["table_1"].copy()
materials = tables["table_2"].copy()

# Normalize key fields
course_instructors["LIBRARY_COURSE_INSTRUCTOR_KEY"] = course_instructors["LIBRARY_COURSE_INSTRUCTOR_KEY"].astype(str).str.strip()
materials["LIBRARY_COURSE_INSTRUCTOR_KEY"] = materials["LIBRARY_COURSE_INSTRUCTOR_KEY"].astype(str).str.strip()
materials["LIBRARY_SUBJECT_OFFERED_KEY"] = materials["LIBRARY_SUBJECT_OFFERED_KEY"].astype(str).str.strip()

# Count amount of material per course instructor key and subject offered key
material_counts = (
    materials
    .dropna(subset=["LIBRARY_COURSE_INSTRUCTOR_KEY", "LIBRARY_SUBJECT_OFFERED_KEY"])
    .groupby(
        ["LIBRARY_COURSE_INSTRUCTOR_KEY", "LIBRARY_SUBJECT_OFFERED_KEY"],
        as_index=False
    )
    .agg(amount_of_material=("LIBRARY_RESERVE_CATALOG_KEY", "nunique"))
)

# Keep unique instructor/course title information
instructor_info = (
    course_instructors[
        ["LIBRARY_COURSE_INSTRUCTOR_KEY", "INSTRUCTOR_NAME", "COURSE_NAME"]
    ]
    .dropna(subset=["LIBRARY_COURSE_INSTRUCTOR_KEY"])
    .drop_duplicates()
)

# Join and format final answer
final_df = (
    material_counts
    .merge(instructor_info, on="LIBRARY_COURSE_INSTRUCTOR_KEY", how="left")
    .rename(columns={
        "INSTRUCTOR_NAME": "course_instructor_name",
        "COURSE_NAME": "course_title",
        "LIBRARY_COURSE_INSTRUCTOR_KEY": "course_instructor_key",
        "LIBRARY_SUBJECT_OFFERED_KEY": "subject_offered_key"
    })
    [
        [
            "course_instructor_key",
            "subject_offered_key",
            "course_instructor_name",
            "course_title",
            "amount_of_material"
        ]
    ]
    .drop_duplicates()
    .sort_values(
        ["course_instructor_key", "subject_offered_key", "course_instructor_name", "course_title"],
        na_position="last"
    )
    .reset_index(drop=True)
)

result = {
    "course_instructor_materials": final_df
}
