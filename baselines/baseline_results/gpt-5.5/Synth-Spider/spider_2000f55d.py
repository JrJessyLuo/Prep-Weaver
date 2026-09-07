import pandas as pd

artists = tables["table_1"].copy()
paintings = tables["table_2"].copy()

# Artists born prior to 1850
artists_pre1850 = artists[artists["birthYear"] < 1850].copy()

# Build artist full name
surname = artists_pre1850["prefix"].fillna("").astype(str).str.strip()
has_last = artists_pre1850["last_name"].notna()
surname = surname.where(~has_last, (artists_pre1850["prefix"].fillna("").astype(str).str.strip() + " " +
                                   artists_pre1850["last_name"].fillna("").astype(str).str.strip()).str.strip())

artists_pre1850["artist_name"] = (
    artists_pre1850["fname"].fillna("").astype(str).str.strip() + " " + surname
).str.strip()

# Join to paintings and select widths
out = paintings.merge(
    artists_pre1850[["artistID", "artist_name"]],
    left_on="painterID",
    right_on="artistID",
    how="inner"
)

out = out[["artist_name", "title", "w_mm"]].rename(columns={"w_mm": "width_mm"})
out = out.sort_values(["artist_name", "title"], kind="stable").reset_index(drop=True)

result = {"painting_widths_pre1850_artists": out}
