import pandas as pd

courses = tables["table_1"].copy()

cip_frames = []

if "table_3" in tables:
    cip3 = tables["table_3"][["PROGRAM_CODE", "CATEGORY_CODE", "CATEGORY_TITLE", "VERSION"]].copy()
    cip3["PROGRAM_CODE"] = pd.to_numeric(cip3["PROGRAM_CODE"], errors="coerce")
    cip_frames.append(cip3)

if "table_4" in tables:
    cip4 = tables["table_4"][["PROGRAM_CODE", "CATEGORY_CODE", "CATEGORY_TITLE", "VERSION"]].copy()
    cip4["PROGRAM_CODE"] = pd.to_numeric(cip4["PROGRAM_CODE"], errors="coerce")
    cip_frames.append(cip4)

cip = (
    pd.concat(cip_frames, ignore_index=True)
    .dropna(subset=["PROGRAM_CODE"])
    .drop_duplicates(["PROGRAM_CODE", "CATEGORY_CODE", "CATEGORY_TITLE", "VERSION"])
)

courses["CIP_PROGRAM_CODE"] = pd.to_numeric(courses["CIP_PROGRAM_CODE"], errors="coerce")

merged = courses.merge(
    cip,
    left_on="CIP_PROGRAM_CODE",
    right_on="PROGRAM_CODE",
    how="left"
)

course_key = "SIS_COURSE_DESCRIPTION_KEY"
merged["DEGREE_GRANTING_COURSE_KEY"] = merged[course_key].where(
    merged["IS_DEGREE_GRANTING"].astype(str).str.upper().eq("Y")
)

answer = (
    merged
    .groupby(
        [
            "CATEGORY_CODE",
            "CATEGORY_TITLE",
            "VERSION",
            "DEPARTMENT_NAME",
            "SCHOOL_NAME",
            "COURSE_LEVEL",
        ],
        dropna=False,
        as_index=False
    )
    .agg(
        TOTAL_NUMBER_OF_COURSES=(course_key, "nunique"),
        TOTAL_NUMBER_OF_DEGREE_GRANTING_COURSES=("DEGREE_GRANTING_COURSE_KEY", "nunique")
    )
    .sort_values(
        ["CATEGORY_CODE", "VERSION", "CATEGORY_TITLE", "DEPARTMENT_NAME", "SCHOOL_NAME", "COURSE_LEVEL"],
        na_position="last"
    )
    .reset_index(drop=True)
)

result = {
    "cip_category_course_level_summary": answer
}
