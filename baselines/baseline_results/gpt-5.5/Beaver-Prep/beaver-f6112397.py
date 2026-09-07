import pandas as pd

iap = tables["table_1"].copy()
cat = tables["table_2"].copy()

# Normalize join keys
iap["IAP_SUBJECT_CATEGORY_KEY"] = iap["IAP_SUBJECT_CATEGORY_KEY"].astype(str).str.strip()
cat["IAP_SUBJECT_CATEGORY_KEY"] = cat["IAP_SUBJECT_CATEGORY_KEY"].astype(str).str.strip()

# Derive academic year from IAP term code, e.g. 2021JA -> 2021
iap["ACADEMIC_YEAR"] = pd.to_numeric(
    iap["TERM_CODE"].astype(str).str.extract(r"(\d{4})")[0],
    errors="coerce"
).astype("Int64")

# Treat missing fees as 0
iap["FEE"] = pd.to_numeric(iap["FEE"], errors="coerce").fillna(0)
iap["MAX_ENROLLMENT"] = pd.to_numeric(iap["MAX_ENROLLMENT"], errors="coerce")

# Exclude cancelled activities when the flag is available
if "IS_CANCELLED" in iap.columns:
    iap = iap[iap["IS_CANCELLED"].fillna("N").astype(str).str.strip().str.upper() != "Y"]

# Deduplicate category-subject-year rows to avoid double counting from multiple sponsors/people
subject_level = (
    iap.groupby(
        ["IAP_SUBJECT_CATEGORY_KEY", "ACADEMIC_YEAR", "IAP_SUBJECT_SESSION_KEY"],
        as_index=False
    )
    .agg(
        FEE=("FEE", "max"),
        MAX_ENROLLMENT=("MAX_ENROLLMENT", "max")
    )
)

# Join category names
merged = subject_level.merge(
    cat[["IAP_SUBJECT_CATEGORY_KEY", "IAP_CATEGORY_NAME"]].drop_duplicates(),
    on="IAP_SUBJECT_CATEGORY_KEY",
    how="left"
)

# Aggregate by category and academic year
out = (
    merged.groupby(["IAP_CATEGORY_NAME", "ACADEMIC_YEAR"], dropna=False, as_index=False)
    .agg(
        total_fee_collected=("FEE", "sum"),
        total_number_of_iap_subjects=("IAP_SUBJECT_SESSION_KEY", "nunique"),
        minimum_enrollment=("MAX_ENROLLMENT", "min"),
        maximum_enrollment=("MAX_ENROLLMENT", "max")
    )
    .rename(columns={
        "IAP_CATEGORY_NAME": "category_name",
        "ACADEMIC_YEAR": "academic_year"
    })
    .sort_values(["category_name", "academic_year"], na_position="last")
    .reset_index(drop=True)
)

result = {"iap_category_academic_year_summary": out}
