import pandas as pd

# Tables are preloaded in `tables`
player_attrs = tables["table_1"]
players = tables["table_2"]

# --- Find player_api_id(s) with maximum overall_rating ---
max_overall_rating = player_attrs["overall_rating"].max(skipna=True)
max_rating_rows = player_attrs.loc[player_attrs["overall_rating"] == max_overall_rating].copy()

max_rating_rows["date"] = pd.to_datetime(max_rating_rows["date"], errors="coerce")

max_rating_records = max_rating_rows[["player_api_id", "overall_rating", "date"]].sort_values(
    ["overall_rating", "player_api_id", "date"], ascending=[False, True, True]
)

# --- Identify birthday-like column in players table ---
birthday_candidates = ["birthday", "birth_date", "birthdate", "date_of_birth", "dob", "birthDay"]
birthday_col = next((c for c in birthday_candidates if c in players.columns), None)

if birthday_col is None:
    lower_map = {c.lower(): c for c in players.columns}
    for key in ["birth", "dob"]:
        hit = next((orig for low, orig in lower_map.items() if key in low), None)
        if hit is not None:
            birthday_col = hit
            break

if birthday_col is None:
    raise KeyError(
        "No birthday-equivalent column found in players table. "
        f"Available columns: {players.columns.tolist()}"
    )

extra_cols = [c for c in ["player_name", "player_fifa_api_id"] if c in players.columns]
players_subset = players[["player_api_id", birthday_col] + extra_cols].copy()

# --- Join max rating records to players and select final answer ---
answer_df = max_rating_records.merge(players_subset, on="player_api_id", how="left")
answer_df[birthday_col] = pd.to_datetime(answer_df[birthday_col], errors="coerce")

answer_df = answer_df.sort_values(
    ["overall_rating", "player_api_id", "date"], ascending=[False, True, True]
).reset_index(drop=True)

# Keep the minimal output focused on the question
cols = [c for c in ["player_api_id", "player_name", "overall_rating", birthday_col] if c in answer_df.columns]
answer_df = answer_df[cols].rename(columns={birthday_col: "birthday"})

# Final result as required
result = {"highest_overall_rating_player_birthday": answer_df}