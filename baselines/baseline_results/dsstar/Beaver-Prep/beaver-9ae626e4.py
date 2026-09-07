import pandas as pd

# Source input tables from the provided `tables` dict
detail = tables['table_1']
sponsor = tables['table_2']

# Defensive checks for required columns
required_detail_cols = ["IAP_SUBJECT_SPONSOR_KEY", "IAP_SUBJECT_SESSION_KEY", "ACTIVITY_TITLE"]
missing_detail = [c for c in required_detail_cols if c not in detail.columns]
if missing_detail:
    raise KeyError(f"Missing required columns in IAP_SUBJECT_DETAIL: {missing_detail}")

if "IAP_SUBJECT_SPONSOR_KEY" not in sponsor.columns:
    raise KeyError("Missing IAP_SUBJECT_SPONSOR_KEY in IAP_SUBJECT_SPONSOR")

# Compute aggregations by sponsor key (sessions and unique subjects)
summary = (
    detail.groupby("IAP_SUBJECT_SPONSOR_KEY", dropna=False)
    .agg(
        sessions_per_sponsor=("IAP_SUBJECT_SESSION_KEY", pd.Series.nunique),
        subjects_per_sponsor=("ACTIVITY_TITLE", pd.Series.nunique),
        detail_rows=("IAP_SUBJECT_SESSION_KEY", "size"),
    )
    .reset_index()
)

# Join to sponsor to attach sponsor information
answer_df = (
    summary.merge(
        sponsor[["IAP_SUBJECT_SPONSOR_KEY", "SPONSOR_NAME", "SPONSOR_TYPE"]],
        on="IAP_SUBJECT_SPONSOR_KEY",
        how="left",
    )
    .sort_values(["sessions_per_sponsor", "subjects_per_sponsor"], ascending=False)
    .reset_index(drop=True)
)

# Select and rename columns to match the question: sponsor name, number of IAP sessions, number of unique subjects
final_table = answer_df.loc[:, ["SPONSOR_NAME", "sessions_per_sponsor", "subjects_per_sponsor"]]

# Assign final answer as a dict[str, DataFrame]
result = {
    "iap_sessions_and_subjects_per_sponsor": final_table
}