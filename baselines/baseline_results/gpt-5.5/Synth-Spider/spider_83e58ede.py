import pandas as pd

# Tables
games = tables["table_1"]
players_wide = tables["table_2"]
plays = tables["table_3"]

# Find Game_ID for "Super Mario World"
smw_ids = games.loc[games["Title"].eq("Super Mario World"), "Game_ID"]

# Players who played that game (and are active/played = 'T' if available)
plays_f = plays[plays["Game_ID"].isin(smw_ids)]
if "If_active" in plays_f.columns:
    plays_f = plays_f[plays_f["If_active"].astype(str).str.upper().eq("T")]

player_years = (
    plays_f["Player_ID"]
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.strip()
    .dropna()
    .unique()
)

# Reshape player info: get name and rank per year
attrs = players_wide[players_wide["Player_ID"].isin(["Player_name", "Rank_of_the_year"])].copy()

long = attrs.melt(id_vars="Player_ID", var_name="year", value_name="val")
wide = (
    long.pivot_table(index="year", columns="Player_ID", values="val", aggfunc="first")
    .reset_index()
)

wide = wide.rename(
    columns={
        "year": "Player_ID",
        "Player_name": "player_name",
        "Rank_of_the_year": "rank",
    }
)

wide["Player_ID"] = wide["Player_ID"].astype(str).str.strip()
wide["rank"] = pd.to_numeric(wide["rank"], errors="coerce")

# Join to players who played Super Mario World
out = wide[wide["Player_ID"].isin(player_years)][["player_name", "rank"]].dropna(how="all")
out = out.sort_values(["rank", "player_name"], na_position="last").reset_index(drop=True)

result = {"players_names_and_ranks": out}
