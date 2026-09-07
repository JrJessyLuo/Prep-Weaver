import pandas as pd

# Access preloaded tables
df_artists = tables['table_1']
df_paintings = tables['table_2']
df_sculptures = tables['table_3']

# Confirm key fields for joining
keys_status = {
    "artists.artistID": "artistID" in df_artists.columns,
    "paintings.painterID": "painterID" in df_paintings.columns,
    "sculptures.sculptorID": "sculptorID" in df_sculptures.columns,
}

# Get distinct artistIDs with at least one painting
if keys_status["artists.artistID"] and keys_status["paintings.painterID"]:
    painters_set = set(
        df_paintings.merge(
            df_artists[["artistID"]],
            left_on="painterID",
            right_on="artistID",
            how="inner"
        )["artistID"].dropna().astype(int).unique().tolist()
    )
else:
    painters_set = set()

# Get distinct artistIDs with at least one sculpture
if keys_status["artists.artistID"] and keys_status["sculptures.sculptorID"]:
    sculptors_set = set(
        df_sculptures.merge(
            df_artists[["artistID"]],
            left_on="sculptorID",
            right_on="artistID",
            how="inner"
        )["artistID"].dropna().astype(int).unique().tolist()
    )
else:
    sculptors_set = set()

# Compute painters with paintings but no sculptures
painters_only_set = painters_set - sculptors_set

# Prepare final answer: first and last names for those artists
if len(painters_only_set) > 0:
    # Try to identify name columns. Based on reference, fname, lname_part1, lname_part2 exist.
    cols_available = df_artists.columns
    name_cols = []
    if "fname" in cols_available:
        name_cols.append("fname")
    if "lname_part1" in cols_available:
        name_cols.append("lname_part1")
    if "lname_part2" in cols_available:
        name_cols.append("lname_part2")

    artists_subset = df_artists[df_artists["artistID"].isin(painters_only_set)].copy()

    # Build first_name and last_name
    # Assume fname is first name; combine last name parts into a single last name
    if "fname" in artists_subset.columns:
        artists_subset["first_name"] = artists_subset["fname"].fillna("").astype(str).str.strip()
    else:
        # Fallback: empty first name if not present
        artists_subset["first_name"] = ""

    last_parts = []
    if "lname_part1" in artists_subset.columns:
        last_parts.append(artists_subset["lname_part1"].fillna("").astype(str))
    if "lname_part2" in artists_subset.columns:
        last_parts.append(artists_subset["lname_part2"].fillna("").astype(str))
    if last_parts:
        artists_subset["last_name"] = (
            pd.Series([""] * len(artists_subset))
            .where(False, "")  # placeholder no-op to ensure Series exists
        )
        artists_subset["last_name"] = (
            pd.concat(last_parts, axis=1)
            .agg(" ".join, axis=1)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
        )
    else:
        # If last name parts are not available, try a generic 'lname' if exists, else empty
        if "lname" in artists_subset.columns:
            artists_subset["last_name"] = artists_subset["lname"].fillna("").astype(str).str.strip()
        else:
            artists_subset["last_name"] = ""

    answer_df = (
        artists_subset[["artistID", "first_name", "last_name"]]
        .sort_values("artistID")
        .reset_index(drop=True)
    )
else:
    answer_df = pd.DataFrame(columns=["artistID", "first_name", "last_name"])

# Assign to result as required
result = {"artists_with_paintings_no_sculptures": answer_df}