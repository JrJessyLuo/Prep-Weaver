import pandas as pd

# Access pre-loaded tables
df_movies = tables['table_1'].copy()
df_theaters = tables['table_2'].copy()

# Construct full titles
df_movies["Title"] = df_movies["Title_Part1"].astype(str) + " " + df_movies["Title_Part2"].astype(str)

# Normalize key types for merging
df_movies["Code_str"] = df_movies["Code"].astype(str)
df_theaters["Code_str"] = df_theaters["Code"].astype(str) if "Code" in df_theaters.columns else ""

# --------------------------
# Parse df_theaters to map theater name -> list of movie Codes.
# The first row values under columns '1'..'6' are theater names.
# Each subsequent row lists codes that are shown in each theater (non-null means included).
# --------------------------

# Identify theater number columns
theater_num_cols = [c for c in df_theaters.columns if c in ["1", "2", "3", "4", "5", "6"]]

# Build mapping of theater column -> theater name from header row
theater_name_map = {}
if not df_theaters.empty:
    header_row = df_theaters.iloc[0]
    for c in theater_num_cols:
        theater_name = header_row[c]
        if pd.notna(theater_name):
            theater_name_map[c] = str(theater_name)

# Initialize mapping theater name -> list of Code strings
theater_to_codes = {name: [] for name in theater_name_map.values()}

# Standardize 'Code' column as string for reading codes from df_theaters
df_theaters_codes = df_theaters.copy()
if "Code" in df_theaters_codes.columns:
    df_theaters_codes["Code"] = df_theaters_codes["Code"].astype(str)

# Collect codes per theater from subsequent rows (after header)
for idx in range(1, len(df_theaters_codes)):
    row = df_theaters_codes.iloc[idx]
    code_val = row.get("Code", None)
    if pd.isna(code_val):
        continue
    code_str = str(code_val)
    for c, theater_name in theater_name_map.items():
        flag = row.get(c, None)
        if pd.notna(flag):
            theater_to_codes[theater_name].append(code_str)

# Extract codes for Odeon
odeon_codes = theater_to_codes.get("Odeon", [])

# Filter movies shown at Odeon and select titles
result_df = (
    df_movies[df_movies["Code_str"].isin(odeon_codes)]
    .loc[:, ["Title"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Package final answer
result = {"odeon_movie_titles": result_df}