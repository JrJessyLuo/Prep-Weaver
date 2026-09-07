import pandas as pd

# Access preloaded tables
artists_df = tables['table_1']
paintings_df = tables['table_2']

# Compute the count of paintings per painterID
counts = (
    paintings_df
    .groupby("painterID", as_index=False)
    .size()
    .rename(columns={"size": "painting_count"})
    .sort_values("painterID")
)

# Deduplicate artists to one row per artistID with fname (prefer keeping first occurrence)
artists_unique = (
    artists_df.sort_values(["artistID"])
    .drop_duplicates(subset=["artistID"], keep="first")[["artistID", "fname"]]
)

# Join painting counts with artists on painterID = artistID
counts_with_names = (
    counts.merge(artists_unique, left_on="painterID", right_on="artistID", how="left")
    .filter(items=["fname", "painting_count"])
)

# Filter to counts >= 2 and prepare final result
final_df = counts_with_names[counts_with_names["painting_count"] >= 2].reset_index(drop=True)

# Assign to result dict as required
result = {"artists_with_at_least_two_paintings": final_df}