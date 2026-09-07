import pandas as pd

artists = tables["table_1"].copy()
paintings = tables["table_2"].copy()
sculptures = tables["table_3"].copy()

painter_ids = set(paintings["painterID"].dropna().astype("int64").unique())

if "sculptorID" in sculptures.columns and not sculptures.empty:
    sculptor_ids = set(sculptures["sculptorID"].dropna().astype("int64").unique())
else:
    sculptor_ids = set()

target_ids = painter_ids - sculptor_ids

artists["lname"] = (
    artists["lname_part1"].fillna("").astype(str).str.strip()
    + " "
    + artists["lname_part2"].fillna("").astype(str).str.strip()
).str.strip()

out = (
    artists[artists["artistID"].isin(target_ids)][["fname", "lname"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"artists_with_painting_no_sculpture": out}
