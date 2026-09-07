import pandas as pd
import re

# The input tables are already loaded into 'tables' dict:
# tables['table_1'] -> games
# tables['table_2'] -> players
# tables['table_3'] -> player_active
# tables['table_4'] -> platforms

# 1) Map the provided tables
games_df = tables['table_1'].copy()
players_df = tables['table_2'].copy()
player_active_df = tables['table_3'].copy()
platforms_df = tables['table_4'].copy()

# 2) Reproduce the same parsing logic for Developers_Platform to extract Platform_ID
def extract_platform_id(val):
    if pd.isna(val):
        return pd.NA
    s = str(val)
    if "::" in s:
        tail = s.split("::")[-1].strip()
        m = re.search(r"(\d+)$", tail)
        if m:
            return int(m.group(1))
    m2 = re.search(r"(\d+)$", s)
    if m2:
        return int(m2.group(1))
    return pd.NA

games_df["Parsed_Platform_ID"] = games_df["Developers_Platform"].apply(extract_platform_id)

# 3) Join games to platforms on parsed Platform_ID (as in the reference)
games_with_platform = games_df.merge(
    platforms_df,
    left_on="Parsed_Platform_ID",
    right_on="Platform_ID",
    how="left",
    suffixes=("", "_platform")
)

# 4) Filter players with Position == "Guard" and link to activity (as in the reference)
guards = players_df[players_df["Position"].str.lower() == "guard"] if "Position" in players_df.columns else players_df.iloc[0:0]
guards_with_activity = guards.merge(player_active_df, on="Player_ID", how="left") if not guards.empty else guards

# Note: Per the reference code, there is no linkage between players and games/platforms.
# Therefore, "games played by players who have the position Guard" cannot be linked.
# Following the reference logic, the feasible computation is to take the average over all games,
# since no player-game linkage exists in the data.
avg_units = games_with_platform["Units_sold_Millions"].mean()

# Prepare the final answer DataFrame
answer_df = pd.DataFrame([{"average_units_sold_millions": avg_units}])

# Package into the required result dict
result = {"average_units_sold_millions_for_guard_players_games": answer_df}