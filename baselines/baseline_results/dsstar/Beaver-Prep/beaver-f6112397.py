import pandas as pd

# Input tables (already provided): tables dict
detail_df = tables['table_1'].copy()
category_df = tables['table_2'].copy()

# Normalize join keys as in reference logic
def normalize_key(s):
    s = s.astype("string")
    s = s.str.strip()
    s = s.str.replace(r"\s+", " ", regex=True)
    s = s.str.lower()
    return s

detail_df["IAP_SUBJECT_CATEGORY_KEY__norm"] = normalize_key(detail_df["IAP_SUBJECT_CATEGORY_KEY"].astype("string"))
category_df["IAP_SUBJECT_CATEGORY_KEY__norm"] = normalize_key(category_df["IAP_SUBJECT_CATEGORY_KEY"].astype("string"))

# Join to bring category name
enriched = detail_df.merge(
    category_df[["IAP_SUBJECT_CATEGORY_KEY__norm", "IAP_CATEGORY_NAME"]],
    how="left",
    on="IAP_SUBJECT_CATEGORY_KEY__norm",
)

# Derive academic year from TERM_CODE (e.g., '2021JA' -> '2021')
enriched["ACADEMIC_YEAR"] = enriched["TERM_CODE"].astype("string").str[:4]

# Ensure numeric fields for aggregation
fee_num = pd.to_numeric(enriched.get("FEE"), errors="coerce")
max_enr_num = pd.to_numeric(enriched.get("MAX_ENROLLMENT"), errors="coerce")

enriched["FEE_NUM"] = fee_num
enriched["MAX_ENROLLMENT_NUM"] = max_enr_num

# Group and aggregate:
# - total fee collected: sum of FEE (NaNs ignored)
# - total number of IAP subjects: count of rows (subject occurrences) per group
# - min and max enrollment: min/max of MAX_ENROLLMENT
group_cols = ["IAP_CATEGORY_NAME", "ACADEMIC_YEAR"]

agg_df = (
    enriched.groupby(group_cols, dropna=False)
    .agg(
        total_fee_collected=("FEE_NUM", "sum"),
        total_iap_subjects=("IAP_SUBJECT_CATEGORY_KEY__norm", "size"),
        min_enrollment=("MAX_ENROLLMENT_NUM", "min"),
        max_enrollment=("MAX_ENROLLMENT_NUM", "max"),
    )
    .reset_index()
)

# Optionally sort for readability
agg_df = agg_df.sort_values(group_cols, kind="stable").reset_index(drop=True)

# Final result dict
result = {
    "iap_category_year_summary": agg_df
}