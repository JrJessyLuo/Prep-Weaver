import pandas as pd
import numpy as np

courses = tables["table_9"].copy()

courses["course_start_date"] = pd.to_datetime(
    courses["DATE_FROM"].astype(str).str.strip(),
    format="%d-%b-%y",
    errors="coerce"
)
courses["course_end_date"] = pd.to_datetime(
    courses["DATE_TO"].astype(str).str.strip(),
    format="%d-%b-%y",
    errors="coerce"
)

courses["duration_days"] = (courses["course_end_date"] - courses["course_start_date"]).dt.days
courses["course_title"] = courses["COURSE_NAME"].astype("string").str.strip()
courses["building_name"] = courses["UNIT"].astype("string").str.strip()

calendar = tables["table_10"][["CALENDAR_DATE", "ACADEMIC_YEAR"]].copy()
calendar["course_start_date"] = pd.to_datetime(
    calendar["CALENDAR_DATE"].astype(str).str.strip(),
    format="%d-%b-%y",
    errors="coerce"
)
calendar = (
    calendar
    .dropna(subset=["course_start_date"])
    .drop_duplicates(subset=["course_start_date"])
    [["course_start_date", "ACADEMIC_YEAR"]]
)

courses = courses.merge(calendar, on="course_start_date", how="left")

fallback_academic_year = np.where(
    courses["course_start_date"].dt.month >= 9,
    courses["course_start_date"].dt.year + 1,
    courses["course_start_date"].dt.year
)
courses["ACADEMIC_YEAR"] = courses["ACADEMIC_YEAR"].fillna(
    pd.Series(fallback_academic_year, index=courses.index)
).astype("Int64")

course_instances = (
    courses
    .dropna(subset=["course_start_date", "course_end_date", "duration_days", "ACADEMIC_YEAR"])
    .drop_duplicates(
        subset=[
            "ACADEMIC_YEAR",
            "course_title",
            "building_name",
            "course_start_date",
            "course_end_date"
        ]
    )
    .sort_values(
        ["ACADEMIC_YEAR", "course_start_date", "course_title", "building_name"],
        kind="mergesort"
    )
    .reset_index(drop=True)
)

course_instances["running_avg_duration_days"] = (
    course_instances
    .groupby("ACADEMIC_YEAR")["duration_days"]
    .transform(lambda s: s.rolling(window=5, center=True, min_periods=1).mean())
)

answer = course_instances[
    [
        "course_title",
        "building_name",
        "duration_days",
        "running_avg_duration_days"
    ]
].reset_index(drop=True)

result = {"course_duration_running_average": answer}
