import pandas as pd

# Access input tables from the provided 'tables' dict
df_addr_type = tables['table_1']  # spider_7ec3e93f_input_0.pkl
df_map = tables['table_2']        # spider_7ec3e93f_input_1.pkl

# Columns we are asked to aggregate over (as in reference code)
code_cols = ['11', '15', '20', '23', '33', '35', '45', '56', '59', '67', '73', '80', '84', '91', '92']
code_cols = [c for c in code_cols if c in df_map.columns]

# If none of the expected columns exist, create an empty final result
if len(code_cols) == 0 or df_map.empty:
    final_df = pd.DataFrame(columns=['address_type_code', 'count', 'address_type_description'])
else:
    # Melt to long format to count frequencies
    id_vars = [c for c in df_map.columns if c not in code_cols]
    long_codes = df_map.melt(
        id_vars=id_vars,
        value_vars=code_cols,
        var_name="source_col",
        value_name="address_type_code"
    )[['address_type_code']]

    # Normalize to string for robust grouping
    long_codes['address_type_code'] = long_codes['address_type_code'].astype(str).str.strip()

    # Count frequencies
    freq = (
        long_codes.groupby('address_type_code', dropna=False)
        .size()
        .reset_index(name='count')
        .sort_values('count', ascending=False)
    )

    # Determine the most frequent code(s)
    if freq.empty:
        top_codes = pd.DataFrame(columns=['address_type_code', 'count'])
    else:
        top_count = freq['count'].max()
        top_codes = freq[freq['count'] == top_count]

    # Join with reference to get descriptions
    df_addr_type_norm = df_addr_type.copy()
    if 'address_type_code' in df_addr_type_norm.columns:
        df_addr_type_norm['address_type_code'] = df_addr_type_norm['address_type_code'].astype(str).str.strip()
    final_df = top_codes.merge(df_addr_type_norm, on='address_type_code', how='left')

# Prepare final result mapping
result = {
    'most_common_student_address_type': final_df[['address_type_code', 'count'] +
                                                 ([c for c in ['address_type_description'] if c in final_df.columns])]
}