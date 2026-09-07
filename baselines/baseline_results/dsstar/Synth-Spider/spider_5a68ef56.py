import pandas as pd

# Access input tables from the provided `tables` dict
df0 = tables['table_1']  # prices
df1 = tables['table_2']  # receipts

# Work only with rows in df1 where Attribute == 'Item' (case-insensitive) and Value is not null
df1_items = df1[df1['Attribute'].str.lower().eq('item') & df1['Value'].notna()].copy()

# Ensure Value is string
df1_items['Value'] = df1_items['Value'].astype(str)

# Split on '-' into up to 5 parts
parts = df1_items['Value'].str.split('-', n=4, expand=True)

# Ensure we have exactly 5 columns
for i in range(5 - parts.shape[1]):
    parts[i + parts.shape[1]] = None

parts = parts.iloc[:, :5]
parts.columns = ['Id_Part1', 'Id_Part2', 'Id_Part3', 'Id_Part4', 'Id_Part5']

# Normalize None-like strings to actual None and keep as object dtype
for c in parts.columns:
    parts[c] = parts[c].replace({'None': None, 'nan': None, 'NaN': None, '': None})

# Attach parsed parts back to df1_items
df1_items = pd.concat([df1_items.reset_index(drop=True), parts.reset_index(drop=True)], axis=1)

# Prepare df0 join keys: ensure dtype/object alignment and normalize None-like
df0_norm = df0.copy()
for c in ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']:
    if c in df0_norm.columns:
        df0_norm[c] = df0_norm[c].astype(object).replace({'None': None, 'nan': None, 'NaN': None, '': None})

# Merge on Id_Part1..Id_Part5
merge_keys = ['Id_Part1','Id_Part2','Id_Part3','Id_Part4','Id_Part5']
merged = df1_items.merge(df0_norm, on=merge_keys, how='left', suffixes=('_df1','_df0'))

# Filter for items with Price > 13
high_price = merged[merged['Price'] > 13]

# Get distinct receipt numbers
distinct_receipts = high_price[['Receipt']].drop_duplicates().sort_values('Receipt').reset_index(drop=True)

# Assign final answer as required
result = {'distinct_receipts_over_13': distinct_receipts}