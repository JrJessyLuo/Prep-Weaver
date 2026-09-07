import pandas as pd

# Access pre-loaded DataFrames from the provided tables dict
df_discounts = tables['table_1']  # spider_84e51fe9_input_0.pkl
df_rentals = tables['table_2']    # spider_84e51fe9_input_1.pkl

# Group rental history by discount_id and count records
discount_usage = (
    df_rentals
    .groupby('discount_id', as_index=False)
    .size()
    .rename(columns={'size': 'usage_count'})
)

# Join with discounts to get discount names
discount_usage_named = discount_usage.merge(
    df_discounts[['id', 'nm']],
    left_on='discount_id',
    right_on='id',
    how='left'
)

# Select the discount name with the highest count
top_discount = (
    discount_usage_named
    .sort_values(['usage_count', 'discount_id'], ascending=[False, True])
    .head(1)[['nm']]
)

# Prepare the final result as required
result = {"most_used_discount": top_discount}