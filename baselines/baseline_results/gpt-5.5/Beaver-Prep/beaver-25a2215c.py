import pandas as pd

people = tables["table_1"].copy()
activities = tables["table_2"].copy()
categories = tables["table_3"].copy()

people["person_key"] = people["iap_subject_person_key"].astype(str).str.strip()
activities["person_key"] = activities["IAP_SUBJECT_PERSON_KEY"].astype(str).str.strip()
activities["category_key"] = activities["IAP_SUBJECT_CATEGORY_KEY"].astype(str).str.strip()
categories["category_key"] = categories["IAP_SUBJECT_CATEGORY_KEY"].astype(str).str.strip()

activity_categories = activities[
    ["person_key", "category_key", "FEE"]
].drop_duplicates()

joined = (
    people.merge(activity_categories, on="person_key", how="inner")
    .merge(categories[["category_key", "IAP_CATEGORY_NAME"]].drop_duplicates(), on="category_key", how="inner")
)

answer = (
    joined.groupby(["PERSON_ROLE", "IAP_CATEGORY_NAME"], dropna=False)
    .agg(
        role_count=("PERSON_NAME", "count"),
        average_fee=("FEE", "mean")
    )
    .reset_index()
    .rename(columns={
        "PERSON_ROLE": "role",
        "IAP_CATEGORY_NAME": "category_name"
    })
    .sort_values("role_count", ascending=False)
    .reset_index(drop=True)
)

result = {"role_category_summary": answer}
