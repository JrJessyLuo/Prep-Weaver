import pandas as pd

iap = tables["table_1"].copy()
terms = tables["table_2"].copy()

# Standardize join keys
iap["TERM_CODE"] = iap["TERM_CODE"].astype(str).str.strip()
terms["term_code"] = terms["term_code"].astype(str).str.strip()

# Deduplicate to the IAP session level to avoid double-counting sessions repeated by category/sponsor/person
session_level = (
    iap.groupby(["TERM_CODE", "IAP_SUBJECT_SESSION_KEY"], as_index=False)
       .agg(
           FEE=("FEE", "first"),
           MAX_ENROLLMENT=("MAX_ENROLLMENT", "first")
       )
)

# Aggregate by term
agg = (
    session_level.groupby("TERM_CODE", as_index=False)
    .agg(
        total_number_of_iap_sessions=("IAP_SUBJECT_SESSION_KEY", "nunique"),
        total_fee_collected=("FEE", lambda s: s.fillna(0).sum()),
        minimum_enrollment=("MAX_ENROLLMENT", "min"),
        maximum_enrollment=("MAX_ENROLLMENT", "max")
    )
)

# Add term descriptions
term_desc = terms[["term_code", "TERM_DESCRIPTION"]].drop_duplicates()

out = (
    agg.merge(term_desc, left_on="TERM_CODE", right_on="term_code", how="left")
       .drop(columns=["term_code"])
       .rename(columns={
           "TERM_CODE": "term_code",
           "TERM_DESCRIPTION": "term_description"
       })
)

out = out[
    [
        "term_code",
        "term_description",
        "total_number_of_iap_sessions",
        "total_fee_collected",
        "minimum_enrollment",
        "maximum_enrollment"
    ]
].sort_values("term_code").reset_index(drop=True)

result = {"iap_sessions_by_term": out}
