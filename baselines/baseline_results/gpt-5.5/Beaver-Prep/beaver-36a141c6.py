import pandas as pd
import numpy as np

tip = tables["table_1"].copy()
subjects = tables["table_7"].copy()
materials = tables["table_4"].copy()

def clean_string(s):
    return s.astype("string").str.strip()

# Course-material fact rows, excluding "course has no materials" records
tip["subject_offered_key"] = clean_string(tip["TIP_SUBJECT_OFFERED_KEY"])
tip["material_key"] = clean_string(tip["TIP_MATERIAL_KEY"])
tip["material_status_key"] = clean_string(tip["TIP_MATERIAL_STATUS_KEY"])
tip["record_count"] = pd.to_numeric(tip["RECORD_COUNT"], errors="coerce").fillna(0)

has_material_key = tip["material_key"].notna() & tip["material_key"].ne("")
has_course_key = tip["subject_offered_key"].notna() & tip["subject_offered_key"].ne("")
is_no_material = (
    tip["material_status_key"].fillna("").eq("NM")
    | tip["material_key"].fillna("").str.contains("course has no materials", case=False, regex=False)
)

tip = tip.loc[has_course_key & has_material_key & ~is_no_material].copy()

# Subject offering / department-school attributes
subjects["subject_offered_key"] = clean_string(subjects["TIP_SUBJECT_OFFERED_KEY"])
subjects["dept_code"] = clean_string(subjects["OFFER_DEPT_CODE"])
subjects["department_name"] = clean_string(subjects["OFFER_DEPT_NAME"])
subjects["school_name"] = clean_string(subjects["OFFER_SCHOOL_NAME"])

for c in ["department_name", "school_name", "dept_code"]:
    subjects[c] = subjects[c].mask(subjects[c].eq(""))

subject_cols = ["subject_offered_key", "dept_code", "department_name", "school_name"]
subject_dim = subjects.loc[subjects["subject_offered_key"].notna(), subject_cols].drop_duplicates("subject_offered_key")

# Optional department dimension fallback
if "table_9" in tables:
    dept_dim = tables["table_9"].copy()
    dept_dim["dept_code"] = clean_string(dept_dim["DEPARTMENT_CODE"])
    dept_dim["dept_department_name"] = clean_string(dept_dim["DEPARTMENT_NAME"])
    dept_dim["dept_school_name"] = clean_string(dept_dim["SCHOOL_NAME"])
    dept_dim = dept_dim[["dept_code", "dept_department_name", "dept_school_name"]].drop_duplicates("dept_code")

    subject_dim = subject_dim.merge(dept_dim, on="dept_code", how="left")
    subject_dim["department_name"] = subject_dim["department_name"].combine_first(subject_dim["dept_department_name"])
    subject_dim["school_name"] = subject_dim["school_name"].combine_first(subject_dim["dept_school_name"])
    subject_dim = subject_dim[["subject_offered_key", "department_name", "school_name"]]
else:
    subject_dim = subject_dim[["subject_offered_key", "department_name", "school_name"]]

# Material prices
materials["material_key"] = clean_string(materials["TIP_MATERIAL_KEY"])
materials["NEW_SHELF_PRICE"] = pd.to_numeric(materials["NEW_SHELF_PRICE"], errors="coerce")
materials["USED_SHELF_PRICE"] = pd.to_numeric(materials["USED_SHELF_PRICE"], errors="coerce")

material_dim = (
    materials.loc[materials["material_key"].notna() & materials["material_key"].ne("")]
    .groupby("material_key", as_index=False)
    .agg(
        NEW_SHELF_PRICE=("NEW_SHELF_PRICE", "mean"),
        USED_SHELF_PRICE=("USED_SHELF_PRICE", "mean"),
    )
)

df = (
    tip.merge(subject_dim, on="subject_offered_key", how="inner")
       .merge(material_dim, on="material_key", how="left")
)

df = df.loc[df["department_name"].notna() & df["school_name"].notna()].copy()

# Weighted averages using RECORD_COUNT as the record weight
df["new_price_weight"] = np.where(df["NEW_SHELF_PRICE"].notna(), df["record_count"], 0)
df["used_price_weight"] = np.where(df["USED_SHELF_PRICE"].notna(), df["record_count"], 0)
df["new_price_weighted_sum"] = df["NEW_SHELF_PRICE"].fillna(0) * df["new_price_weight"]
df["used_price_weighted_sum"] = df["USED_SHELF_PRICE"].fillna(0) * df["used_price_weight"]

grouped = (
    df.groupby(["department_name", "school_name"], dropna=False)
      .agg(
          unique_course_materials=("material_key", "nunique"),
          number_of_courses=("subject_offered_key", "nunique"),
          total_material_records=("record_count", "sum"),
          distinct_material_statuses=("material_status_key", "nunique"),
          new_price_weighted_sum=("new_price_weighted_sum", "sum"),
          new_price_weight=("new_price_weight", "sum"),
          used_price_weighted_sum=("used_price_weighted_sum", "sum"),
          used_price_weight=("used_price_weight", "sum"),
      )
      .reset_index()
)

grouped["avg_new_shelf_price"] = grouped["new_price_weighted_sum"] / grouped["new_price_weight"].replace(0, np.nan)
grouped["avg_used_shelf_price"] = grouped["used_price_weighted_sum"] / grouped["used_price_weight"].replace(0, np.nan)

final_cols = [
    "department_name",
    "school_name",
    "unique_course_materials",
    "number_of_courses",
    "avg_new_shelf_price",
    "avg_used_shelf_price",
    "total_material_records",
    "distinct_material_statuses",
]

grouped = grouped[final_cols].sort_values(["school_name", "department_name"], na_position="last").reset_index(drop=True)

total_new_weight = df["new_price_weight"].sum()
total_used_weight = df["used_price_weight"].sum()

grand_total = pd.DataFrame([{
    "department_name": pd.NA,
    "school_name": pd.NA,
    "unique_course_materials": df["material_key"].nunique(),
    "number_of_courses": df["subject_offered_key"].nunique(),
    "avg_new_shelf_price": (
        df["new_price_weighted_sum"].sum() / total_new_weight if total_new_weight else np.nan
    ),
    "avg_used_shelf_price": (
        df["used_price_weighted_sum"].sum() / total_used_weight if total_used_weight else np.nan
    ),
    "total_material_records": df["record_count"].sum(),
    "distinct_material_statuses": df["material_status_key"].nunique(),
}])

out = pd.concat([grouped, grand_total], ignore_index=True)

result = {
    "department_school_course_material_summary": out
}
