import pandas as pd

# Access pre-loaded tables
df0 = tables['table_1'].copy()
df1 = tables['table_2'].copy()

# 1) Parse movie titles from df0 by splitting 'trc' at '###' into a clean 'Title' column
df0['Title'] = df0['trc'].astype(str).str.split('###', n=1).str[0].str.strip()

# 2) Extract the cinema-to-code mapping from df1 for 'Odeon' and 'Imperial' as integers
df1_indexed = df1.set_index('Code')
row_name = df1_indexed.loc['Name']
cinema_to_code = {}
for col in ['1', '2']:
    if col in row_name.index.astype(str):
        cinema = str(row_name[col]).strip()
        code_int = int(col)
        cinema_to_code[cinema] = code_int

# 3) Identify codes for Odeon or Imperial from the 'Movie' row
row_movie = df1_indexed.loc['Movie']
target_codes = set()
for cinema in ['Odeon', 'Imperial']:
    if cinema in cinema_to_code:
        col_idx = str(cinema_to_code[cinema])
        if col_idx in row_movie.index.astype(str):
            val = row_movie[col_idx]
            if pd.notna(val):
                target_codes.add(int(val))

# 4) Filter df0 by these codes and select Titles
answer_df = df0[df0['Code'].isin(target_codes)][['Title']].reset_index(drop=True)

# Package final result
result = {'movies_in_odeon_or_imperial': answer_df}