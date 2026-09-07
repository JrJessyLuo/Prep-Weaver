import pandas as pd
import numpy as np

# 1) Load DataFrames from provided `tables` dict
iap_detail = tables['table_1'].copy()
iap_category = tables['table_2'].copy()
iap_sponsor = tables['table_3'].copy()

# 2) Standardize join key dtypes (fix potential category join mismatch)
detail_cat_key = "IAP_SUBJECT_CATEGORY_KEY"
detail_sponsor_key = "IAP_SUBJECT_SPONSOR_KEY"
cat_key = "IAP_SUBJECT_CATEGORY_KEY"
sponsor_key = "IAP_SUBJECT_SPONSOR_KEY"

for df, cols in [(iap_detail, [detail_cat_key, detail_sponsor_key]),
                 (iap_category, [cat_key]),
                 (iap_sponsor, [sponsor_key])]:
    for c in cols:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip()

# Ensure FEE is numeric where possible
if "FEE" in iap_detail.columns:
    iap_detail["FEE_NUM"] = pd.to_numeric(iap_detail["FEE"], errors="coerce")
else:
    iap_detail["FEE_NUM"] = np.nan

# 3) Left join DETAIL -> CATEGORY -> SPONSOR
join_cols_detail = [c for c in ["ACTIVITY_TITLE","TERM_CODE","FEE","FEE_NUM","FEE_REASON",detail_cat_key,detail_sponsor_key] if c in iap_detail.columns]
cat_keep = [col for col in [cat_key, "IAP_CATEGORY_NAME"] if col in iap_category.columns]
sponsor_keep = [col for col in [sponsor_key, "SPONSOR_NAME", "SPONSOR_TYPE"] if col in iap_sponsor.columns]

joined = (
    iap_detail[join_cols_detail]
    .merge(iap_category[cat_keep], left_on=detail_cat_key, right_on=cat_key, how="left")
    .merge(iap_sponsor[sponsor_keep], left_on=detail_sponsor_key, right_on=sponsor_key, how="left")
)

# 4) Compute metrics per (IAP_CATEGORY_NAME, SPONSOR_NAME)
group_cols = ["IAP_CATEGORY_NAME", "SPONSOR_NAME"]
for g in group_cols:
    if g not in joined.columns:
        joined[g] = np.nan

# Normalize ACTIVITY_TITLE for distinct counting
if "ACTIVITY_TITLE" in joined.columns:
    joined["_ACTIVITY_TITLE_NORM"] = joined["ACTIVITY_TITLE"].astype(str).str.strip()
else:
    joined["_ACTIVITY_TITLE_NORM"] = ""

agg_df = (
    joined
    .groupby(group_cols, dropna=False)
    .agg(
        activities_count=("_ACTIVITY_TITLE_NORM", lambda s: s.dropna().nunique()),
        avg_fee=("FEE_NUM", "mean"),
    )
    .reset_index()
)

# Sort by activities_count descending, then by avg_fee descending
agg_df = agg_df.sort_values(["activities_count", "avg_fee"], ascending=[False, False])

# Prepare final result mapping
result = {
    "iap_category_sponsor_activity_counts_and_avg_fee": agg_df
}