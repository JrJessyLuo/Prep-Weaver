import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

t2["theater_name"] = t2["Name_Part1"].fillna("").astype(str) + t2["Name_Part2"].fillna("").astype(str)

theaters = {"Odeon", "Imperial"}
movie_codes = (
    t2.loc[t2["theater_name"].isin(theaters), "Movie"]
      .dropna()
      .astype(int)
      .unique()
)

out = (
    t1.loc[t1["Code"].isin(movie_codes), ["movie_title"]]
      .drop_duplicates()
      .reset_index(drop=True)
)

result = {"movies_at_odeon_or_imperial": out}
