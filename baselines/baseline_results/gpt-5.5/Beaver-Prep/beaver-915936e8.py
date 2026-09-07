import pandas as pd

df = tables["table_9"].copy()

# Parse dates
df["course_start_date"] = pd.to_datetime(df["DATE_FROM"], format="%d-%b-%y", errors="coerce")

# Extract term code from the library course instructor key when available
df["term_code"] = (
    df["LIBRARY_COURSE_INSTRUCTOR_KEY"]
    .astype(str)
    .str.extract(r"(\d{4}(?:FA|JA|SP|SU))", expand=False)
)

# Academic year is encoded in the MIT term code; fall terms already carry the following academic year
df["academic_year"] = pd.to_numeric(df["term_code"].str[:4], errors="coerce")

# Fallback academic year from start date if term code is missing
fallback_academic_year = df["course_start_date"].dt.year + (df["course_start_date"].dt.month >= 9).astype(int)
df["academic_year"] = df["academic_year"].fillna(fallback_academic_year).astype("Int64")

# Extract a course identifier to help collapse multiple instructor rows for the same course offering
df["course_identifier"] = (
    df["LIBRARY_COURSE_INSTRUCTOR_KEY"]
    .astype(str)
    .str.extract(r":([^:]+)$", expand=False)
)
df["course_identifier"] = df["course_identifier"].fillna(
    df["LIBRARY_COURSE_INSTRUCTOR_KEY"].astype(str).str.extract(r"^([^-]+)", expand=False)
)

# Building/location name
df["building_name"] = df["UNIT"].fillna(df["UNIT_CODE"])

# Clean text fields
for col in ["COURSE_NAME", "building_name", "course_identifier", "term_code"]:
    df[col] = df[col].astype("string").str.strip()

# One row per course offering/location, avoiding duplicate instructor rows
courses = (
    df.dropna(subset=["COURSE_NAME", "course_start_date", "academic_year"])
      .drop_duplicates(
          subset=[
              "academic_year",
              "term_code",
              "course_identifier",
              "COURSE_NAME",
              "DATE_FROM",
              "DATE_TO",
              "building_name",
          ]
      )
      .sort_values(
          ["academic_year", "course_start_date", "COURSE_NAME", "building_name", "course_identifier"],
          ascending=True,
          na_position="last",
      )
      .reset_index(drop=True)
)

# Cumulative count within each academic year, ordered by course start date
courses["cumulative_number_of_courses"] = (
    courses.groupby("academic_year").cumcount() + 1
)

final_df = courses.rename(columns={"COURSE_NAME": "course_name"})[
    ["course_name", "building_name", "cumulative_number_of_courses"]
].reset_index(drop=True)

result = {
    "course_building_cumulative_counts": final_df
}
