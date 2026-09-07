import pandas as pd

# Source DataFrames from provided `tables` dict
clients_df = tables['table_1'].copy()
orders_df = tables['table_2'].copy()

# Ensure IdClient dtypes compatible for join
if clients_df['IdClient'].dtype != orders_df['IdClient'].dtype:
    clients_df['IdClient'] = clients_df['IdClient'].astype(str)
    orders_df['IdClient'] = orders_df['IdClient'].astype(str)

# Normalize IdOrder: handle possible comma-separated values and explode
orders_norm = orders_df.copy()
orders_norm['IdOrder'] = orders_norm['IdOrder'].astype(str).str.strip()
orders_norm = orders_norm.assign(IdOrder=orders_norm['IdOrder'].str.split(r'\s*,\s*')).explode('IdOrder', ignore_index=True)
orders_norm = orders_norm[orders_norm['IdOrder'].str.len() > 0]

# Join and select final columns
joined_df = clients_df.merge(orders_norm, on='IdClient', how='inner')
answer_df = joined_df[['IdOrder', 'Name']].drop_duplicates().reset_index(drop=True)

# Package result as required
result = {"orders_with_clients": answer_df}