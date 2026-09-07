import pandas as pd

tip_fact = tables["table_1"].copy()
subjects = tables["table_3"].copy()
materials = tables["table_6"].copy()

# Normalize join keys
for df, cols in [
    (tip_fact, ["TIP_SUBJECT_OFFERED_KEY", "TIP_MATERIAL_KEY"]),
    (subjects, ["TIP_SUBJECT_OFFERED_KEY"]),
    (materials, ["TIP_MATERIAL_KEY"]),
]:
    for col in cols:
        df[col] = df[col].astype("string").str.strip()

materials["AUTHOR"] = materials["AUTHOR"].astype("string").str.strip()
subjects["OFFER_SCHOOL_NAME"] = subjects["OFFER_SCHOOL_NAME"].astype("string").str.strip()

# Keep one row per material key and one row per subject offering key to avoid duplicate expansion
materials_dim = materials[["TIP_MATERIAL_KEY", "AUTHOR"]].drop_duplicates()
subjects_dim = subjects[
    ["TIP_SUBJECT_OFFERED_KEY", "OFFER_SCHOOL_NAME", "COURSE_NUMBER_DESC", "COURSE_NUMBER", "SUBJECT_ID"]
].drop_duplicates()

df = (
    tip_fact.merge(materials_dim, on="TIP_MATERIAL_KEY", how="left")
    .merge(subjects_dim, on="TIP_SUBJECT_OFFERED_KEY", how="left")
)

# Use course description as course type where available; fall back to course number, then subject id
df["course_type"] = (
    df["COURSE_NUMBER_DESC"]
    .astype("string")
    .str.strip()
    .fillna(df["COURSE_NUMBER"].astype("string").str.strip())
    .fillna(df["SUBJECT_ID"].astype("string").str.strip())
)

answer = (
    df.groupby(
        ["AUTHOR", "OFFER_SCHOOL_NAME", "TIP_MATERIAL_STATUS_KEY"],
        dropna=False,
        as_index=False,
    )
    .agg(
        total_record_counts=("RECORD_COUNT", "sum"),
        total_number_of_types_of_courses=("course_type", "nunique"),
    )
    .rename(
        columns={
            "AUTHOR": "author",
            "OFFER_SCHOOL_NAME": "school_name",
            "TIP_MATERIAL_STATUS_KEY": "material_status",
        }
    )
    .sort_values(["author", "school_name", "material_status"], na_position="last")
    .reset_index(drop=True)
)

result = {"author_school_material_summary": answer}
