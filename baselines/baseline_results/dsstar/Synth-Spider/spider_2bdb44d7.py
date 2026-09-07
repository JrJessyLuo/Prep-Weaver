import pandas as pd

# Source DataFrames from provided `tables` dict
df_prev = tables['table_2']  # corresponds to spider_2bdb44d7_input_1.pkl

# Reproduce the same logic as the reference code:
# Filter for rows where process_id is null or missing
filtered_df = df_prev[df_prev['process_id'].isna()]

# Extract unique document_id values from the filtered dataframe
unique_document_ids_prev = filtered_df['document_id'].dropna().unique().tolist()

# Prepare final answer as a DataFrame
answer_df = pd.DataFrame({'document_id': unique_document_ids_prev})

# Assign the final answer to `result` as specified
result = {'document_ids_without_process': answer_df}