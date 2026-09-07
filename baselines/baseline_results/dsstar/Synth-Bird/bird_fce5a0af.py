import pandas as pd

# Tables are preloaded in `tables`
match_df = tables["table_1"]   # european_football_2_Match
league_df = tables["table_2"]  # european_football_2_League

# Lookup league_id for "Scotland Premier League"
league_name = "Scotland Premier League"
league_row = league_df.loc[league_df["name"] == league_name]

assert not league_row.empty, f'League "{league_name}" not found in League table.'
assert league_row.shape[0] == 1, f'Ambiguous league name match for "{league_name}":\n{league_row}'

league_id = int(league_row["id"].iloc[0])

# Filter matches for season 2015/2016 and this league, then count
season = "2015/2016"
count_matches = int(match_df[(match_df["season"] == season) & (match_df["league_id"] == league_id)].shape[0])

# Final answer table
answer_df = pd.DataFrame(
    [{"league_name": league_name, "season": season, "match_count": count_matches}]
)

result = {"answer": answer_df}