import pandas as pd

# Use pre-loaded DataFrames from `tables`
df_clients = tables['table_1']
df_orders = tables['table_2']

# 1) Build client_id_to_name dict from the 'Name' row of clients
client_mapping = {}
if 'IdClient' in df_clients.columns:
    name_rows = df_clients[df_clients['IdClient'].astype(str).str.strip().str.lower() == 'name']
    if not name_rows.empty:
        row = name_rows.iloc[0]
        for col in df_clients.columns:
            if col != 'IdClient':
                client_mapping[str(col)] = row[col]

# 2) Map orders.KH to client names using this dict
df_orders_mapped = df_orders.copy()
if 'KH' in df_orders_mapped.columns and client_mapping:
    def kh_to_name(kh):
        if pd.isna(kh):
            return None
        key = str(int(kh))
        return client_mapping.get(key)
    df_orders_mapped['ClientName'] = df_orders_mapped['KH'].apply(kh_to_name)
else:
    df_orders_mapped['ClientName'] = None

# 3) Group orders by client name and count rows
order_counts = (
    df_orders_mapped
    .dropna(subset=['ClientName'])
    .groupby('ClientName', as_index=False)
    .size()
    .rename(columns={'size': 'OrderCount'})
    .sort_values(['OrderCount', 'ClientName'], ascending=[False, True])
    .reset_index(drop=True)
)

# Assign final result
result = {
    "order_counts_per_client": order_counts
}