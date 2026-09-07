import pandas as pd
import numpy as np
import re

assignments = tables["table_1"].copy()
instructors = tables["table_2"].copy()

key_col = "LIBRARY_COURSE_INSTRUCTOR_KEY"

def first_valid(s):
    s = s.dropna()
    return s.iloc[0] if len(s) else pd.NA

def parse_subject_from_key(s):
    return s.astype(str).str.split(":", n=1).str[-1].replace({"nan": pd.NA})

instructors["course_identifier"] = instructors["COURSE_NAME"]
instructors["course_identifier"] = instructors["course_identifier"].where(
    instructors["course_identifier"].notna(),
    parse_subject_from_key(instructors[key_col])
)

course_counts = (
    instructors.dropna(subset=["INSTRUCTOR_NAME"])
    .groupby("INSTRUCTOR_NAME", as_index=False)
    .agg(unique_courses_taught=("course_identifier", "nunique"))
)

key_lookup = (
    instructors.dropna(subset=[key_col])
    .groupby(key_col, as_index=False)
    .agg(INSTRUCTOR_NAME=("INSTRUCTOR_NAME", first_valid))
)

assignments_with_instructor = assignments.merge(
    key_lookup,
    on=key_col,
    how="left"
)

def extract_year(series):
    numeric = pd.to_numeric(series, errors="coerce")
    extracted = pd.to_numeric(
        series.astype(str).str.extract(r"((?:18|19|20)\d{2})", expand=False),
        errors="coerce"
    )
    return numeric.where(numeric.between(1000, 2100), extracted)

publication_year_added = False
catalog_key = "LIBRARY_RESERVE_CATALOG_KEY"

for _, df in tables.items():
    pub_cols = [
        c for c in df.columns
        if re.search(
            r"(publication|publish|pub).*year|year.*(publication|publish|pub)|"
            r"(publication|publish|pub).*date|date.*(publication|publish|pub)",
            c,
            flags=re.IGNORECASE
        )
        and not re.search(r"warehouse", c, flags=re.IGNORECASE)
    ]
    
    if catalog_key in df.columns and pub_cols:
        pub_col = pub_cols[0]
        pub_year = df[[catalog_key, pub_col]].copy()
        pub_year["publication_year"] = extract_year(pub_year[pub_col])
        pub_year = (
            pub_year.dropna(subset=[catalog_key])
            .groupby(catalog_key, as_index=False)
            .agg(publication_year=("publication_year", first_valid))
        )
        assignments_with_instructor = assignments_with_instructor.merge(
            pub_year,
            on=catalog_key,
            how="left"
        )
        publication_year_added = True
        break

if not publication_year_added:
    assignments_with_instructor["publication_year"] = np.nan

material_stats = (
    assignments_with_instructor.dropna(subset=["INSTRUCTOR_NAME"])
    .groupby("INSTRUCTOR_NAME", as_index=False)
    .agg(
        total_material_assignments=(catalog_key, "size"),
        average_publication_year=("publication_year", "mean"),
        distinct_status_count=("LIBRARY_MATERIAL_STATUS_KEY", "nunique")
    )
)

final = course_counts.merge(
    material_stats,
    on="INSTRUCTOR_NAME",
    how="left"
)

final["total_material_assignments"] = final["total_material_assignments"].fillna(0).astype(int)
final["distinct_status_count"] = final["distinct_status_count"].fillna(0).astype(int)

final = (
    final.rename(columns={"INSTRUCTOR_NAME": "instructor_name"})
    [[
        "instructor_name",
        "unique_courses_taught",
        "total_material_assignments",
        "average_publication_year",
        "distinct_status_count"
    ]]
    .sort_values(
        ["unique_courses_taught", "instructor_name"],
        ascending=[False, True]
    )
    .reset_index(drop=True)
)

result = {"instructor_course_material_summary": final}
