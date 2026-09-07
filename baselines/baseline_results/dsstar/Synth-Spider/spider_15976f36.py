import pandas as pd

# Tables are provided in scope as `tables`
artists_df = tables['table_1']
paintings_df = tables['table_2']

# Reproduce the same logic as the reference code
mary_artists = artists_df[artists_df["fname"] == "Mary"]
mary_artist_ids = mary_artists["artistID"].unique().tolist()

target_painter_ids = mary_artist_ids
filtered_paintings = paintings_df[paintings_df["painterID"].isin(target_painter_ids)][["title", "year"]]

# Prepare final answer as required
result = {
    "mary_paintings_title_year": filtered_paintings.reset_index(drop=True)
}