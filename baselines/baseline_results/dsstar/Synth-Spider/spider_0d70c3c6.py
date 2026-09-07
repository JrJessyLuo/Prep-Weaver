import pandas as pd

# The input DataFrames are provided in the `tables` dict.
# Reproduce the same logic as the reference code but source from tables['table_1'].

df = tables['table_1']

# Extract all product names without any specific order
answer_df = df[['product_name']].drop_duplicates()

# Assign final result
result = {"product_names": answer_df}