import pandas as pd

activities = tables["table_1"].copy()
categories = tables["table_2"].copy()
sponsors = tables["table_3"].copy()

# Normalize join keys
for df, cols in [
    (activities, ["IAP_SUBJECT_CATEGORY_KEY", "IAP_SUBJECT_SPONSOR_KEY", "IAP_SUBJECT_SESSION_KEY", "IS_CANCELLED"]),
    (categories, ["IAP_SUBJECT_CATEGORY_KEY"]),
    (sponsors, ["IAP_SUBJECT_SPONSOR_KEY"]),
]:
    for col in cols:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

# Keep non-cancelled activities, treating null cancellation flags as not cancelled
activities = activities[
    activities["IS_CANCELLED"].isna() | (activities["IS_CANCELLED"].str.upper() != "Y")
].copy()

# Treat missing fees as zero-fee activities
activities["FEE"] = activities["FEE"].fillna(0)

# Join category and sponsor names
df = (
    activities
    .merge(
        categories[["IAP_SUBJECT_CATEGORY_KEY", "IAP_CATEGORY_NAME"]].drop_duplicates(),
        on="IAP_SUBJECT_CATEGORY_KEY",
        how="left"
    )
    .merge(
        sponsors[["IAP_SUBJECT_SPONSOR_KEY", "SPONSOR_NAME"]].drop_duplicates(),
        on="IAP_SUBJECT_SPONSOR_KEY",
        how="left"
    )
)

# Deduplicate so an activity is counted once per category-sponsor pair
activity_key = "IAP_SUBJECT_SESSION_KEY"
df_unique = df.drop_duplicates(
    subset=["IAP_SUBJECT_CATEGORY_KEY", "IAP_SUBJECT_SPONSOR_KEY", activity_key]
)

summary = (
    df_unique
    .groupby(["IAP_CATEGORY_NAME", "SPONSOR_NAME"], dropna=False, as_index=False)
    .agg(
        number_of_activities_offered=(activity_key, "nunique"),
        average_fee_per_activity=("FEE", "mean")
    )
    .sort_values("number_of_activities_offered", ascending=False)
    .reset_index(drop=True)
)

result = {
    "iap_category_activity_summary": summary
}
