import pandas as pd
import numpy as np
import re

# Input DataFrames are provided in 'tables'
df_buildings = tables['table_1'].copy()
df_regions = tables['table_2'].copy()

# Helper normalization
def norm(s):
    if pd.isna(s):
        return None
    return str(s).strip().lower()

# Prepare regions with combined/normalized names
df_regions = df_regions.copy()
df_regions['_region_name'] = (df_regions['Name_Part1'].fillna('') + ' ' + df_regions['Name_Part2'].fillna('')).str.strip()
df_regions['_region_name_norm'] = df_regions['_region_name'].apply(norm)
df_regions['_name_part1_norm'] = df_regions['Name_Part1'].apply(norm)
df_regions['_name_part2_norm'] = df_regions['Name_Part2'].apply(norm)

# Normalize building fields
df_buildings = df_buildings.copy()
df_buildings['_address_norm'] = df_buildings['Address'].apply(norm)
df_buildings['_name_norm'] = df_buildings['Name'].apply(norm)

# Heuristic region matching (as in reference)
matches = []
for i, b in df_buildings.iterrows():
    addr = b['_address_norm'] or ''
    bname = b['_name_norm'] or ''
    best = None
    for j, r in df_regions.iterrows():
        candidates = [r['_region_name_norm'], r['_name_part1_norm'], r['_name_part2_norm']]
        candidates = [c for c in candidates if c and c != 'none']
        hit = any((c in addr) or (c in bname) for c in candidates)
        if hit:
            best = r['Region_ID']
            break
    matches.append(best)
df_buildings['Region_ID'] = matches

# Detect candidate story columns (numeric-like names present in df_buildings)
candidate_cols = []
for c in df_buildings.columns:
    try:
        ci = int(c)
        if c in ['1','2','4','5','6','8','9','10']:
            candidate_cols.append(c)
    except (ValueError, TypeError):
        continue
candidate_cols = sorted(candidate_cols, key=lambda x: int(x))

# Infer Stories and Stories_Value
def infer_stories_and_value(row):
    hits = [c for c in candidate_cols if pd.notna(row.get(c))]
    if len(hits) == 1:
        stories = int(hits[0])
        metric_value = row[hits[0]]
        return pd.Series({'Stories': stories, 'Stories_Value': metric_value})
    elif len(hits) == 0:
        return pd.Series({'Stories': np.nan, 'Stories_Value': np.nan})
    else:
        chosen = hits[0]
        return pd.Series({'Stories': int(chosen), 'Stories_Value': row[chosen]})

stories_df = df_buildings.apply(infer_stories_and_value, axis=1)
df_with_stories = pd.concat([df_buildings, stories_df], axis=1)

# Remove candidate story columns from clean frame
cols_to_keep = [c for c in df_with_stories.columns if c not in candidate_cols]
df_clean = df_with_stories[cols_to_keep].copy()

# Merge with regions basic info
df_merged = df_buildings.merge(
    df_regions[['Region_ID', 'Capital', 'Area', 'Population', 'Name_Part1', 'Name_Part2']],
    on='Region_ID',
    how='left'
)
df_merged_with_stories = df_merged.merge(
    df_clean[['Building_ID', 'Stories', 'Stories_Value']],
    on='Building_ID',
    how='left'
)

# Address-based region extraction
region_name_set = set(df_regions['Name_Part1'].dropna().str.strip().str.lower().unique())

def extract_region_from_address(addr):
    if pd.isna(addr):
        return None
    tokens = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ']+", str(addr))
    tokens_lower = [t.lower() for t in tokens]
    for t in tokens_lower:
        if t in region_name_set:
            return t
    for i in range(len(tokens_lower)-1):
        pair = (tokens_lower[i] + " " + tokens_lower[i+1]).strip()
        if pair in region_name_set:
            return pair
    return None

df_clean['region_from_address_norm'] = df_clean['Address'].apply(extract_region_from_address)

# Build final region name
df_regions_lookup = df_regions[['Region_ID', 'Name_Part1']].copy()
df_regions_lookup['_name_part1_norm'] = df_regions_lookup['Name_Part1'].apply(norm)

df_enriched = df_clean.merge(
    df_merged[['Building_ID', 'Region_ID', 'Name_Part1']], on='Building_ID', how='left', suffixes=('', '_from_merge')
)

def choose_region_name(row):
    if pd.notna(row.get('Name_Part1')) and str(row['Name_Part1']).strip() != '':
        return str(row['Name_Part1']).strip()
    if pd.notna(row.get('region_from_address_norm')):
        match = df_regions_lookup[df_regions_lookup['_name_part1_norm'] == row['region_from_address_norm']]
        if not match.empty:
            return match.iloc[0]['Name_Part1']
        else:
            return str(row['region_from_address_norm']).title()
    return np.nan

df_enriched['Region_Name_Final'] = df_enriched.apply(choose_region_name, axis=1)

# Filter to Abruzzo and select number of stories
target_region = "Abruzzo"
is_abruzzo = df_enriched['Region_Name_Final'].str.lower() == target_region.lower()
df_abruzzo_buildings = df_enriched[is_abruzzo].copy()

# Final answer: number of stories of buildings in Abruzzo
answer_df = df_abruzzo_buildings[['Building_ID', 'Name', 'Stories']].reset_index(drop=True)

# Package result
result = {"stories_in_abruzzo": answer_df}