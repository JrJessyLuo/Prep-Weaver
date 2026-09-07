import pandas as pd

players = tables["table_1"][["player_api_id", "weight"]].copy()
countries = tables["table_2"][["kode", "nama"]].copy()
matches = tables["table_3"][["country_id"] + [c for c in tables["table_3"].columns if c.startswith("home_player_") or c.startswith("away_player_")]].copy()

# Use only player id columns (home_player_1..11, away_player_1..11)
player_cols = [c for c in matches.columns if c.startswith("home_player_") or c.startswith("away_player_")]
player_cols = [c for c in player_cols if c.split("_")[-1].isdigit()]  # keep *_1..*_11, drop *_X* and *_Y*
matches = matches[["country_id"] + player_cols]

long_players = (
    matches.melt(id_vars="country_id", value_vars=player_cols, value_name="player_api_id")
    .drop(columns="variable")
    .dropna(subset=["player_api_id"])
)
long_players["player_api_id"] = long_players["player_api_id"].astype("int64")

# Deduplicate to avoid counting repeated appearances of same player within a country
long_players = long_players.drop_duplicates(subset=["country_id", "player_api_id"])

# Join weights
long_players = long_players.merge(players, on="player_api_id", how="inner").dropna(subset=["weight"])

avg_w = (
    long_players.groupby("country_id", as_index=False)["weight"]
    .mean()
    .rename(columns={"weight": "avg_weight"})
)

out = (
    avg_w.merge(countries, left_on="country_id", right_on="kode", how="left")
    .rename(columns={"nama": "country"})
    .sort_values("avg_weight", ascending=False)
    .head(1)[["country", "avg_weight"]]
    .reset_index(drop=True)
)

result = {"heaviest_avg_weight_country": out}
