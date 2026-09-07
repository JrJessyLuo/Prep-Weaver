import pandas as pd

# Load tables
t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Normalize artist table (table_1 is transposed: attributes in rows, artist IDs in columns)
artists = (
    t1.set_index("artistID")
      .T
      .reset_index()
      .rename(columns={"index": "artistID"})
)

artists["artistID"] = pd.to_numeric(artists["artistID"], errors="coerce")
artists["fname"] = artists["fname"].astype(str)

artists["lname_part1"] = artists["lname_part1"].astype(str)
artists["lname_part2"] = artists["lname_part2"].where(artists["lname_part2"].notna(), "")
artists["lname_part2"] = artists["lname_part2"].astype(str)

artists["last_name"] = (artists["lname_part1"].str.strip() + " " + artists["lname_part2"].str.strip()).str.strip()
artists = artists.rename(columns={"fname": "first_name"})[["artistID", "first_name", "last_name"]]

# Find painterIDs that have BOTH oil and lithograph paintings
t2["medium_norm"] = t2["medium"].astype(str).str.strip().str.lower()
med = t2[t2["medium_norm"].isin(["oil", "lithograph"])].copy()

both_ids = (
    med.groupby("painterID")["medium_norm"]
       .nunique()
       .reset_index(name="n_media")
       .query("n_media == 2")[["painterID"]]
)

# Join to names
out = both_ids.merge(artists, left_on="painterID", right_on="artistID", how="inner")
out = out[["first_name", "last_name"]].drop_duplicates().reset_index(drop=True)

result = {"artists_oil_and_lithograph": out}
