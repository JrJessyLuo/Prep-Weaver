import pandas as pd

# The input DataFrames are provided in a dict named `tables`
df0 = tables['table_1']
df1 = tables['table_2']

# 1) Build long form for df0 and pivot to wide
def explode_attributes(row):
    attrs = row['shuxing']
    vals = row['shuxing_zhi']
    if not isinstance(attrs, (list, tuple)) or not isinstance(vals, (list, tuple)):
        return pd.DataFrame()
    n = min(len(attrs), len(vals))
    return pd.DataFrame({
        'siji_id': [row['siji_id']]*n,
        'attribute': attrs[:n],
        'value': vals[:n]
    })

long_parts = []
for _, r in df0.iterrows():
    long_parts.append(explode_attributes(r))
df0_long = pd.concat(long_parts, ignore_index=True) if long_parts else pd.DataFrame(columns=['siji_id','attribute','value'])

df0_wide = df0_long.pivot_table(index='siji_id', columns='attribute', values='value', aggfunc='first').reset_index()

# 2) Normalize df0.siji_id by stripping quotes and casting to int
def clean_siji_id(x):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        s = s[1:-1]
    return pd.to_numeric(s, errors='coerce')

df0_wide['_siji_id_num'] = df0_wide['siji_id'].apply(clean_siji_id).astype('Int64')

# 3) Group df1 by Driver_ID to count races, identify the Driver_ID with max count
race_counts = df1.groupby('Driver_ID', as_index=False).size().rename(columns={'size': 'race_count'})
max_count = race_counts['race_count'].max()
top_drivers = race_counts.loc[race_counts['race_count'] == max_count, 'Driver_ID']
top_driver_id = int(top_drivers.min())

# 4) Join df1 on Driver_ID to df0_wide on cleaned siji_id to fetch attributes (e.g., Age)
df1_ = df1.copy()
df1_['_Driver_ID'] = df1_['Driver_ID'].astype('Int64')

merged = df1_[df1_['_Driver_ID'] == top_driver_id].merge(
    df0_wide, left_on='_Driver_ID', right_on='_siji_id_num', how='left', suffixes=('_race', '_driver')
)

# Extract the Age for the top driver (if available)
top_driver_age = None
if 'Age' in merged.columns:
    age_vals = merged['Age'].dropna().unique()
    if len(age_vals) > 0:
        top_driver_age = age_vals[0]

# Build final answer DataFrame
answer_df = pd.DataFrame({'Age_of_top_driver_by_race_count': [top_driver_age]})

# Assign to result as required
result = {'top_driver_age': answer_df}