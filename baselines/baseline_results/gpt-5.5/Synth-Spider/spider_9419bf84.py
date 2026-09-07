import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Map cinema names to their column labels using the "Name" row
name_row = t2.loc[t2["Code"].eq("Name")].iloc[0]
movie_row = t2.loc[t2["Code"].eq("Movie")].iloc[0]

cinema_cols = [c for c in t2.columns if c != "Code" and name_row[c] in ["Odeon", "Imperial"]]

movie_codes = (
    pd.to_numeric(movie_row[cinema_cols], errors="coerce")
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

t1["movie_name"] = t1["trc"].astype(str).str.split("###", n=1, expand=True)[0]

out = (
    t1.loc[t1["Code"].isin(movie_codes), ["movie_name"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"movies": out}
