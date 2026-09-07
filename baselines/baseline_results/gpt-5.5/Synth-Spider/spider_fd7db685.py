import pandas as pd

artists = tables["table_1"][["artistID", "fname"]].drop_duplicates(subset=["artistID"])
paintings = tables["table_2"]

cnt = paintings.groupby("painterID", as_index=False).size().rename(columns={"size": "number_of_works"})
cnt = cnt[cnt["number_of_works"] >= 2]

out = cnt.merge(artists, left_on="painterID", right_on="artistID", how="left")
out = out[["fname", "number_of_works"]].sort_values(["number_of_works", "fname"], ascending=[False, True]).reset_index(drop=True)

result = {"artists_with_at_least_two_paintings": out}
