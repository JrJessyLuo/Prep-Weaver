import pandas as pd
import re

courses = tables["table_5"].copy()
buildings = tables["table_1"].copy()

# Filter courses offered by the Center for International Studies
dept_mask = courses["OFFER_DEPT_NAME"].astype(str).str.contains(
    r"Center for International Studies", case=False, na=False
)
cis_courses = courses.loc[dept_mask].copy()

# Extract building keys from meeting places such as "26-247D", "E51-350", etc.
valid_building_keys = set(buildings["BUILDING_KEY"].dropna().astype(str))

def extract_building_keys(meet_place):
    if pd.isna(meet_place):
        return []
    text = str(meet_place).upper()
    matches = re.findall(r"\b([A-Z]*\d+[A-Z]*)-", text)
    return [m for m in matches if m in valid_building_keys]

cis_courses["BUILDING_KEY"] = cis_courses["MEET_PLACE"].apply(extract_building_keys)
cis_courses = cis_courses.explode("BUILDING_KEY").dropna(subset=["BUILDING_KEY"])

# Count distinct course offerings per building
course_counts = (
    cis_courses
    .drop_duplicates(["BUILDING_KEY", "SUBJECT_OFFERED_SUMMARY_KEY"])
    .groupby("BUILDING_KEY", as_index=False)
    .agg(number_of_courses_offered=("SUBJECT_OFFERED_SUMMARY_KEY", "nunique"))
)

answer = (
    course_counts
    .merge(
        buildings[["BUILDING_KEY", "BUILDING_NAME"]].drop_duplicates(),
        on="BUILDING_KEY",
        how="left"
    )
    [["BUILDING_KEY", "BUILDING_NAME", "number_of_courses_offered"]]
    .sort_values("BUILDING_KEY")
    .reset_index(drop=True)
)

result = {"courses_by_building_for_center_for_international_studies": answer}
