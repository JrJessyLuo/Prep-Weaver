import pandas as pd

# --- Get Scotland Premier League league_id from key-value league table (table_1) ---
league_kv = tables["table_1"].copy()

league_names = league_kv[league_kv["attr_value"].astype(str).str.startswith("name:")].copy()
league_names["league_name"] = (
    league_names["attr_value"].astype(str).str.replace("name:", "", regex=False).str.strip()
)

scotland_league_ids = league_names.loc[
    league_names["league_name"].str.contains(r"\bScotland Premier League\b", case=False, na=False),
    "country_id",
]

scotland_league_id = scotland_league_ids.iloc[0] if len(scotland_league_ids) else None

# --- Unpivot match table (table_2) from "attributes as rows" to normal long form ---
matches_raw = tables["table_2"].copy()
matches = matches_raw.set_index("id").T.reset_index().rename(columns={"index": "match_id"})

matches["league_id"] = pd.to_numeric(matches.get("league_id"), errors="coerce")
matches["season"] = matches.get("season").astype(str)

# --- Count matches in 2015/2016 season for Scotland Premier League ---
if scotland_league_id is None:
    n_matches = 0
else:
    n_matches = matches.loc[
        (matches["season"] == "2015/2016") & (matches["league_id"] == float(scotland_league_id))
    ].shape[0]

result = {
    "scotland_premier_league_2015_2016_match_count": pd.DataFrame(
        {"number_of_matches": [n_matches]}
    )
}
