import pandas as pd

# Access input tables from provided `tables` dict
iap_df = tables['table_1'].copy()
terms_df = tables['table_2'].copy()

# Standardize key names and types for join
def norm_term_code(s):
    if pd.isna(s):
        return pd.NA
    return str(s).strip().upper()

# Normalize term codes
iap_df['TERM_CODE_NORM'] = iap_df['TERM_CODE'].apply(norm_term_code)
terms_df['term_code_NORM'] = terms_df['term_code'].apply(norm_term_code)

# Prepare a slimmed terms lookup with description
terms_lu = terms_df[['term_code_NORM', 'TERM_DESCRIPTION']].drop_duplicates()

# Coerce numerics
iap_df['FEE_NUM'] = pd.to_numeric(iap_df['FEE'], errors='coerce')
iap_df['MAX_ENROLLMENT_NUM'] = pd.to_numeric(iap_df['MAX_ENROLLMENT'], errors='coerce')

# Determine whether to use session key count or row count
session_key = 'IAP_SUBJECT_SESSION_KEY'
use_row_count = session_key not in iap_df.columns or iap_df[session_key].isna().all()

group_cols = ['TERM_CODE_NORM']

# Aggregate metrics
if not use_row_count:
    iap_grouped = (
        iap_df
        .groupby(group_cols, dropna=False)
        .agg(
            total_sessions=(session_key, 'count'),
            total_fee_collected=('FEE_NUM', 'sum'),
            min_enrollment=('MAX_ENROLLMENT_NUM', 'min'),
            max_enrollment=('MAX_ENROLLMENT_NUM', 'max')
        )
        .reset_index()
    )
else:
    iap_grouped = (
        iap_df
        .groupby(group_cols, dropna=False)
        .agg(
            total_fee_collected=('FEE_NUM', 'sum'),
            min_enrollment=('MAX_ENROLLMENT_NUM', 'min'),
            max_enrollment=('MAX_ENROLLMENT_NUM', 'max')
        )
        .reset_index()
    )
    row_counts = (
        iap_df.groupby(group_cols, dropna=False)
        .size()
        .reset_index(name='total_sessions')
    )
    iap_grouped = iap_grouped.merge(row_counts, on='TERM_CODE_NORM', how='left')

# Fill NaNs appropriately
iap_grouped['total_fee_collected'] = iap_grouped['total_fee_collected'].fillna(0)

# Enrich with term description
iap_grouped_enriched = iap_grouped.merge(
    terms_lu,
    how='left',
    left_on='TERM_CODE_NORM',
    right_on='term_code_NORM'
).drop(columns=['term_code_NORM'])

# Arrange final columns
final_cols = ['TERM_CODE_NORM', 'TERM_DESCRIPTION', 'total_sessions', 'total_fee_collected', 'min_enrollment', 'max_enrollment']
final_df = iap_grouped_enriched[final_cols].sort_values(['TERM_CODE_NORM'])

# Package result
result = {
    'iap_term_metrics': final_df
}