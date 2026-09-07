import pandas as pd

artists = tables["table_1"].copy()
sculptures = tables["table_2"].copy()

pre1900_sculptor_ids = sculptures.loc[sculptures["year"].lt(1900), "sculptorID"].dropna().unique()

out = (
    artists.loc[artists["artistID"].isin(pre1900_sculptor_ids), ["fname", "lname"]]
    .drop_duplicates()
    .rename(columns={"fname": "first_name", "lname": "last_name"})
    .reset_index(drop=True)
)

result = {"distinct_sculptors_before_1900": out}
