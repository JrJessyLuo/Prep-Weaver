import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Identify the column(s) corresponding to the Odeon theater and get its movie code(s)
t2i = t2.set_index("Code")
odeon_cols = t2i.columns[t2i.loc["Name"].astype(str).eq("Odeon")]
odeon_movie_codes = (
    pd.to_numeric(t2i.loc["Movie", odeon_cols], errors="coerce")
    .dropna()
    .astype(int)
    .unique()
)

# Build full movie titles and filter to those played at Odeon
t1["movie_title"] = t1["Title_Part1"].fillna("").astype(str).str.strip() + " " + t1["Title_Part2"].fillna("").astype(str).str.strip()
t1["movie_title"] = t1["movie_title"].str.replace(r"\s+", " ", regex=True).str.strip()

out = (
    t1[t1["Code"].isin(odeon_movie_codes)][["movie_title"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"odeon_movie_titles": out}
