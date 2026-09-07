import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

# Extract club names from the transposed/key-value style table_1
name_row = t1.loc[t1["Club_ID"].astype(str).str.lower().eq("name")]
name_long = (
    name_row.drop(columns=["Club_ID"])
    .melt(var_name="Club_ID", value_name="club_name")
    .dropna(subset=["club_name"])
)
name_long["Club_ID"] = name_long["Club_ID"].astype(str)

# Club IDs that have at least one player
club_with_players = set(t2["Club_ID"].dropna().astype(int).astype(str).unique())

# Clubs that do not have players
out = name_long.loc[~name_long["Club_ID"].isin(club_with_players), ["club_name"]].reset_index(drop=True)

result = {"clubs_without_players": out}
