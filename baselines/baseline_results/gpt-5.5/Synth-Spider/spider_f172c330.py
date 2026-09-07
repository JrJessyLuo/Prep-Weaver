import pandas as pd

p = tables["table_1"].copy()
a = tables["table_2"].copy()

p["player_name"] = p["First_part"].astype(str).str.strip() + " " + p["Last_part"].astype(str).str.strip()

active_cols = [c for c in a.columns if c.startswith("If_active_")]
a[active_cols] = a[active_cols].astype("string")

a["played_any_game"] = a[active_cols].eq("T").any(axis=1)

merged = p.merge(a[["Player_ID", "played_any_game"]], on="Player_ID", how="left")
no_game = merged["played_any_game"].fillna(False) == False

out = (
    merged.loc[no_game, ["player_name"]]
    .drop_duplicates()
    .sort_values("player_name", kind="stable")
    .reset_index(drop=True)
)

result = {"players_no_games": out}
