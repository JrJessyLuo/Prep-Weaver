import pandas as pd

games = tables["table_1"]
players = tables["table_2"]
activity = tables["table_3"]

# Players who are Guards
guards = players.loc[players["Position"].eq("Guard"), ["Player_ID"]].drop_duplicates()

# Activity columns -> long form with corresponding Game_ID
act_cols = [c for c in activity.columns if c.startswith("If_active_")]
guards_act = guards.merge(activity, on="Player_ID", how="inner")

long_act = guards_act.melt(
    id_vars=["Player_ID"],
    value_vars=act_cols,
    var_name="if_active_col",
    value_name="active_flag",
)

long_act["Game_ID"] = (
    long_act["if_active_col"].str.extract(r"If_active_(\d+)", expand=False).astype("Int64")
)

# Games played by Guards (active == 'T')
guard_game_ids = (
    long_act.loc[long_act["active_flag"].astype(str).str.upper().eq("T"), "Game_ID"]
    .dropna()
    .astype(int)
    .unique()
)

avg_units = games.loc[games["Game_ID"].isin(guard_game_ids), "Units_sold_Millions"].mean()

result = {
    "average_units_sold_millions_guard_players": pd.DataFrame(
        {"average_units_sold_millions": [avg_units]}
    )
}
