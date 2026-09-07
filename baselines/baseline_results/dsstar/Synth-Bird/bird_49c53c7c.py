import pandas as pd

# Use the preloaded table (matches) from `tables`
matches = tables["table_2"]

# Parse home/away goals from game_score
if "game_score" not in matches.columns:
    raise KeyError("No 'game_score' column found; cannot parse goals from score string.")

s = matches["game_score"].astype("string").str.strip()
parsed = s.str.extract(r"^\s*(\d+)\s*-\s*(\d+)\s*$")
parsed.columns = ["home_goals_parsed", "away_goals_parsed"]
parsed = parsed.astype("float")

matches_with_parsed = matches.join(parsed)

# Filter to Poland (country_id == 15722) in season 2010/2011
poland_2010_2011 = matches_with_parsed[
    (matches_with_parsed["season"] == "2010/2011") &
    (matches_with_parsed["country_id"] == 15722)
]

mean_home_goals = poland_2010_2011["home_goals_parsed"].mean()
mean_home_goals_rounded = round(mean_home_goals, 2)

answer_df = pd.DataFrame({"average_home_goals": [mean_home_goals_rounded]})

result = {"average_home_team_goals_poland_2010_2011": answer_df}