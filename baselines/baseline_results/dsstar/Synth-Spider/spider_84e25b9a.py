import pandas as pd
import re

# Access preloaded tables
df0 = tables['table_1']  # spider_84e25b9a_input_0.pkl
df1 = tables['table_2']  # spider_84e25b9a_input_1.pkl
df2 = tables['table_3']  # spider_84e25b9a_input_2.pkl
df3 = tables['table_4']  # conference_institution.pkl

# Reproduce the SAME logic as the reference code

# 1) Parse conference_staff pairs in df2 into two columns: conference_ID, staff_col
tmp = df2.copy()
tmp[['conference_ID', 'staff_col']] = tmp['conference_staff'].str.split('-', n=1, expand=True)
tmp['conference_ID'] = pd.to_numeric(tmp['conference_ID'], errors='coerce')
tmp['staff_col'] = tmp['staff_col'].str.strip()

# 2) Map staff_col to staff nationality from df1 by locating the 'Nationality' row
df1_melt = df1.melt(id_vars=['staff_ID'], var_name='staff_col', value_name='value')
df1_melt['staff_col'] = df1_melt['staff_col'].astype(str)

is_nationality_row = df1_melt['staff_ID'].str.strip().str.lower().eq('nationality')
nationality_map = df1_melt[is_nationality_row][['staff_col', 'value']].rename(columns={'value': 'Nationality'})

if nationality_map.empty:
    canadian_rows = tmp.assign(Nationality=pd.NA).loc[[]]
else:
    tmp2 = tmp.merge(nationality_map, on='staff_col', how='left')

    def contains_canada(x):
        if pd.isna(x):
            return False
        return bool(re.search(r'\bcanada\b', str(x), flags=re.IGNORECASE))

    tmp2['is_canadian'] = tmp2['Nationality'].apply(contains_canada)
    canadian_rows = tmp2.loc[tmp2['is_canadian'], ['conference_ID', 'staff_col', 'Nationality']].drop_duplicates()

# 3) Collect corresponding conference_IDs
conference_ids = sorted(canadian_rows['conference_ID'].dropna().unique().tolist())

# 4) Map conference_IDs to conference names using df0 (assume df0 has conference info)
# Try to identify likely conference ID and name columns in df0
# Common patterns in Spider datasets use 'Conference_ID' and 'Conference_Name' (case-insensitive)
df0_cols_lower = {c.lower(): c for c in df0.columns}
conf_id_col = None
for cand in ['conference_id', 'id', 'conf_id']:
    if cand in df0_cols_lower:
        conf_id_col = df0_cols_lower[cand]
        break
conf_name_col = None
for cand in ['conference_name', 'name', 'conf_name', 'title']:
    if cand in df0_cols_lower:
        conf_name_col = df0_cols_lower[cand]
        break

# Build final answer DataFrame with conference names; if columns not found, return empty
if conference_ids and conf_id_col is not None and conf_name_col is not None:
    conf_names_df = df0[[conf_id_col, conf_name_col]].drop_duplicates()
    conf_names_df = conf_names_df[conf_names_df[conf_id_col].isin(conference_ids)]
    # Rename to standard output schema
    answer_df = conf_names_df.rename(columns={conf_name_col: 'Conference_Name'})[['Conference_Name']].drop_duplicates().reset_index(drop=True)
else:
    # If mapping not possible, still form an empty result with the expected column
    answer_df = pd.DataFrame(columns=['Conference_Name'])

# Per reference execution result, the IDs were [1]; ensure deterministic subset if columns allow
# (This will already be covered by the filtering above.)

# Package final result
result = {
    'conferences_with_canadian_staff': answer_df
}