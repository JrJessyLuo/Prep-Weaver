import pandas as pd
import re

# Input tables provided in scope as `tables`
df0 = tables['table_1']
df1 = tables['table_2']
df2 = tables['table_3']  # not used directly but kept to mirror reference environment

# Helper to parse state and country from df1.state_country
def split_state_country(val):
    if pd.isna(val):
        return pd.Series([pd.NA, pd.NA])
    parts = str(val).split('~')
    if len(parts) == 2:
        return pd.Series(parts)
    return pd.Series([pd.NA, val])

df1 = df1.copy()
df1[['state', 'country_raw']] = df1['state_country'].apply(split_state_country)

# Normalize country names to catch China variants
def norm_country(x: str):
    if pd.isna(x):
        return pd.NA
    s = str(x).strip().upper()
    s = re.sub(r'[\.\s]+', '', s)  # remove dots and spaces
    china_aliases = {
        "CHINA", "PRC", "PEOPLE'SREPUBLICOFCHINA", "PEOPLESREPUBLICOFCHINA",
        "MAINLANDCHINA", "CN", "P.R.CHINA", "P.R.C", "P.R.OFCHINA", "CHN"
    }
    if s in china_aliases:
        return "CHINA"
    if "CHINA" in s or "PRC" in s:
        return "CHINA"
    return s

df1['country_norm'] = df1['country_raw'].apply(norm_country)

# Normalize for comparison
df1_codes = df1['city_code'].astype(str).str.strip().str.upper()

# Create a normalized attribute_value field for df0
df0 = df0.copy()
df0['attr_norm'] = df0['attribute_value'].astype(str).str.strip().str.upper()

# Join df0 rows whose attr_norm matches a city_code in df1
df0_city = df0[df0['attr_norm'].isin(df1_codes)].copy()

# Prepare df1 with normalized key for merge
df1_merge = df1.copy()
df1_merge['city_code_norm'] = df1_merge['city_code'].astype(str).str.strip().str.upper()

merged = df0_city.merge(
    df1_merge[['city_code_norm', 'country_norm']],
    left_on='attr_norm',
    right_on='city_code_norm',
    how='left'
)

# Filter to China
merged_china = merged[merged['country_norm'] == 'CHINA']

# Count distinct student_id
distinct_students_china = merged_china['student_id'].astype(str).nunique()

# Build final answer DataFrame
answer_df = pd.DataFrame({"distinct_students_in_china": [distinct_students_china]})

# Assign to result as required
result = {"students_in_china": answer_df}