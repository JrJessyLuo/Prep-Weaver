import pandas as pd

# Tables are preloaded in `tables`
player_df = tables["table_1"]   # bird_c08c3554_input_0.pkl
country_df = tables["table_2"]  # bird_c08c3554_input_1.pkl
match_df = tables["table_3"]    # bird_c08c3554_input_2.pkl

# Identify player-id columns in match
player_cols_in_match = [
    c for c in match_df.columns
    if c.startswith("home_player_") or c.startswith("away_player_")
]

# Build player -> inferred_country_id mapping via match appearances (same logic as reference)
player_ids = set(player_df["player_api_id"].unique())

long = match_df[["country_id"] + player_cols_in_match].melt(
    id_vars=["country_id"],
    value_vars=player_cols_in_match,
    value_name="player_api_id"
).dropna(subset=["player_api_id"])

# Ensure numeric type (melt can produce floats due to NaNs)
long["player_api_id"] = pd.to_numeric(long["player_api_id"], errors="coerce").dropna().astype("int64")
long = long[long["player_api_id"].isin(player_ids)]

player_country_counts = (
    long.groupby(["player_api_id", "country_id"])
        .size()
        .reset_index(name="appearances")
        .sort_values(["player_api_id", "appearances"], ascending=[True, False])
)

primary_country = (
    player_country_counts
        .drop_duplicates("player_api_id", keep="first")
        .rename(columns={"country_id": "inferred_country_id"})
)

# Attach inferred country name (same join style as reference)
primary_country = primary_country.merge(
    country_df.rename(columns={"kode": "inferred_country_id", "nama": "inferred_country_name"}),
    on="inferred_country_id",
    how="left"
)

# Compute average weight per inferred country (heaviest average)
# Weight column in player table is `weight` (as in European Soccer DB Player table).
weights = (
    primary_country.merge(
        player_df[["player_api_id", "weight"]],
        on="player_api_id",
        how="left"
    )
)

avg_weight_by_country = (
    weights.dropna(subset=["inferred_country_name", "weight"])
           .groupby("inferred_country_name", as_index=False)
           .agg(
               avg_weight=("weight", "mean"),
               player_count=("player_api_id", "nunique")
           )
           .sort_values(["avg_weight", "player_count"], ascending=[False, False])
)

answer_df = avg_weight_by_country.head(1).reset_index(drop=True)

result = {"heaviest_average_weight_country": answer_df}