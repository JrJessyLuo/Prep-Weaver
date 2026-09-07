import pandas as pd

# Use pre-loaded tables
df_cap = tables['table_1'].copy()
df_usage = tables['table_2'].copy()

# Infer mapping: 'wh' is a 1-based row index into capacity table
df_cap_idxed = df_cap.copy()
df_cap_idxed['wh'] = range(1, len(df_cap_idxed) + 1)

# Count items per warehouse in usage data
usage_counts = df_usage.groupby('wh', as_index=False).agg(item_count=('Code', 'count'))

# Join counts with capacity
counts_with_cap = usage_counts.merge(df_cap_idxed[['wh', 'Capacity']], on='wh', how='left')

# Warehouses over capacity
over_capacity_wh = counts_with_cap[counts_with_cap['item_count'] > counts_with_cap['Capacity']][['wh']]

# Distinct Codes for those warehouses
if not over_capacity_wh.empty:
    codes_over_capacity = (
        df_usage.merge(over_capacity_wh, on='wh', how='inner')['Code']
        .drop_duplicates()
        .sort_values()
        .reset_index(drop=True)
    )
    answer_df = pd.DataFrame({'Code': codes_over_capacity})
else:
    answer_df = pd.DataFrame(columns=['Code'])

# Package final result
result = {"codes_over_capacity": answer_df}