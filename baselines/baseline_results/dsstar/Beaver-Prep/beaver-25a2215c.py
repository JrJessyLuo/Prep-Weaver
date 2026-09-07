import pandas as pd

# Helper to coerce fee to numeric
def coerce_fee_to_numeric(series: pd.Series) -> pd.Series:
    s = series.astype(str)
    s = s.str.replace(r"[,$]", "", regex=True).str.strip()
    s = s.replace({"": None, "nan": None, "None": None})
    return pd.to_numeric(s, errors="coerce")

# Source tables from the provided dict `tables`
person = tables['table_1']  # IAP_SUBJECT_PERSON.pkl
detail = tables['table_2']  # IAP_SUBJECT_DETAIL.pkl
category = tables['table_3']  # IAP_SUBJECT_CATEGORY.pkl

# Prepare person and category columns to use in merge
merge_person_cols = ["iap_subject_person_key", "PERSON_ROLE", "PERSON_NAME"]
merge_category_cols = ["IAP_SUBJECT_CATEGORY_KEY", "IAP_CATEGORY_NAME"]

# Join detail → person → category
df = (
    detail
    .merge(person[merge_person_cols], how="left",
           left_on="IAP_SUBJECT_PERSON_KEY", right_on="iap_subject_person_key")
    .merge(category[merge_category_cols], how="left", on="IAP_SUBJECT_CATEGORY_KEY")
)

# Coerce FEE to numeric for averaging
if "FEE" in df.columns:
    df["FEE_NUM"] = coerce_fee_to_numeric(df["FEE"])
else:
    df["FEE_NUM"] = pd.Series([pd.NA] * len(df), index=df.index)

# Build a helper unique key column prioritizing person key, else name
unique_person_id = df["iap_subject_person_key"].where(df["iap_subject_person_key"].notna(), df["PERSON_NAME"])

# Group and aggregate
grouped = (
    df.groupby(["PERSON_ROLE", "IAP_CATEGORY_NAME"], dropna=False)
      .agg(
          role_count=("iap_subject_person_key", lambda s: unique_person_id.loc[s.index].nunique(dropna=True)),
          avg_fee=("FEE_NUM", "mean"),
          rows=("FEE_NUM", "size")
      )
      .reset_index()
)

# Sort by role_count desc, then by PERSON_ROLE/IAP_CATEGORY_NAME for stability
final_df = grouped.sort_values(["role_count", "PERSON_ROLE", "IAP_CATEGORY_NAME"], ascending=[False, True, True])

# Assign to result dict as required
result = {"iap_role_category_summary": final_df}