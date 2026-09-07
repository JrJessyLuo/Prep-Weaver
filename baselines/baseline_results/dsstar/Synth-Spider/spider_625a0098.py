import pandas as pd

# Access the DataFrames from the provided `tables` dict
df_headphones = tables['table_1']  # corresponds to spider_625a0098_input_0.pkl
df_inventory = tables['table_2']   # corresponds to spider_625a0098_input_1.pkl

# Filter headphones to those not present in inventory by Headphone_ID and select unique Model
inventory_ids = set(df_inventory['Headphone_ID'].unique())
models_not_in_inventory = (
    df_headphones.loc[~df_headphones['Headphone_ID'].isin(inventory_ids), ['Model']]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Package final answer as required
result = {
    "models_not_in_stock": models_not_in_inventory
}