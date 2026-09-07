import pandas as pd

df = tables["table_2"].copy()

# Standardize subject id column name
if "subject_id" in df.columns and "SUBJECT_ID" not in df.columns:
    df = df.rename(columns={"subject_id": "SUBJECT_ID"})

# Keep courses offered in academic year 2022
df_2022 = df[
    (df["ACADEMIC_YEAR"] == 2022)
    & (df["IS_OFFERED_THIS_YEAR"].astype(str).str.upper() == "Y")
].copy()

# Build one instructor-course row per offered fall/spring course
parts = []

if "FALL_INSTRUCTORS" in df_2022.columns:
    fall = df_2022[df_2022["IS_OFFERED_FALL_TERM"].astype(str).str.upper() == "Y"][
        ["ACADEMIC_YEAR", "SUBJECT_ID", "FALL_INSTRUCTORS"]
    ].rename(columns={"FALL_INSTRUCTORS": "INSTRUCTOR_NAME"})
    parts.append(fall)

if "SPRING_INSTRUCTORS" in df_2022.columns:
    spring = df_2022[df_2022["IS_OFFERED_SPRING_TERM"].astype(str).str.upper() == "Y"][
        ["ACADEMIC_YEAR", "SUBJECT_ID", "SPRING_INSTRUCTORS"]
    ].rename(columns={"SPRING_INSTRUCTORS": "INSTRUCTOR_NAME"})
    parts.append(spring)

instructor_courses = pd.concat(parts, ignore_index=True)

# Split comma-separated instructor lists into individual instructor names
instructor_courses = instructor_courses.dropna(subset=["INSTRUCTOR_NAME"]).copy()
instructor_courses["INSTRUCTOR_NAME"] = instructor_courses["INSTRUCTOR_NAME"].astype(str)
instructor_courses = instructor_courses.assign(
    INSTRUCTOR_NAME=instructor_courses["INSTRUCTOR_NAME"].str.split(r"\s*,\s*")
).explode("INSTRUCTOR_NAME")

instructor_courses["INSTRUCTOR_NAME"] = instructor_courses["INSTRUCTOR_NAME"].str.strip()
instructor_courses = instructor_courses[
    instructor_courses["INSTRUCTOR_NAME"].ne("")
    & instructor_courses["INSTRUCTOR_NAME"].str.lower().ne("nan")
]

# Count distinct course types/subjects per instructor
answer = (
    instructor_courses.drop_duplicates(["ACADEMIC_YEAR", "INSTRUCTOR_NAME", "SUBJECT_ID"])
    .groupby(["ACADEMIC_YEAR", "INSTRUCTOR_NAME"], as_index=False)
    .agg(total_number_of_course_types=("SUBJECT_ID", "nunique"))
    .rename(columns={
        "ACADEMIC_YEAR": "academic_year",
        "INSTRUCTOR_NAME": "instructor_name"
    })
    .sort_values(["academic_year", "total_number_of_course_types", "instructor_name"],
                 ascending=[True, False, True])
    .reset_index(drop=True)
)

result = {
    "instructor_course_type_counts_2022": answer
}
