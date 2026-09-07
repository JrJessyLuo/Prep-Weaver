import pandas as pd

# Source tables (already loaded in scope)
team_df = tables["table_1"]
raw_df = tables["table_2"]

# Reshape raw attributes matrix into tidy Team_Attributes-like table
assert "id" in raw_df.columns, "Expected 'id' column in tables['table_2']."
mat = raw_df.set_index("id")
tidy = mat.T.copy()
tidy.index.name = "record_col_key"
tidy.reset_index(drop=False, inplace=True)

# Normalize column names
def _norm_col(c):
    if c is None:
        return c
    return str(c).strip().lower()

tidy.columns = [_norm_col(c) for c in tidy.columns]

# Ensure join key present/normalized
if "taid" in tidy.columns and "team_api_id" not in tidy.columns:
    tidy.rename(columns={"taid": "team_api_id"}, inplace=True)
if "team_api_id" in tidy.columns:
    tidy["team_api_id"] = pd.to_numeric(tidy["team_api_id"], errors="coerce")

# Locate speed class column (same logic as reference)
speed_class_candidates = [c for c in tidy.columns if ("speed" in c and "class" in c)]
for extra in ["bpsc", "build_up_play_speed_class", "buildupplayspeedclass", "build_up_play_speedclass"]:
    if extra in tidy.columns and extra not in speed_class_candidates:
        speed_class_candidates.append(extra)

preferred_order = [
    "buildupplayspeedclass",
    "build_up_play_speed_class",
    "speed_class",
    "build_up_play_speedclass",
    "bpsc",
]
speed_class_col = next((c for c in preferred_order if c in tidy.columns), None)
if speed_class_col is None and speed_class_candidates:
    speed_class_col = speed_class_candidates[0]

assert speed_class_col is not None, (
    "Could not locate a speed_class column. "
    f"Candidates found: {speed_class_candidates[:20]}"
)
assert "team_api_id" in tidy.columns, "Expected 'team_api_id' (or 'taid') in tidy attributes for joining."

# Filter to 'Fast' and join to get team_long_name
fast_attr = tidy[tidy[speed_class_col].astype(str).str.strip().str.lower() == "fast"].copy()

fast_team_ids = (
    fast_attr[["team_api_id"]]
    .dropna()
    .drop_duplicates()
)

fast_teams = (
    team_df.merge(fast_team_ids, on="team_api_id", how="inner")
    .loc[:, ["team_long_name"]]
    .drop_duplicates()
    .sort_values("team_long_name")
    .reset_index(drop=True)
)

# Final answer
result = {"fast_speed_class_team_names": fast_teams}
print(result["fast_speed_class_team_names"].to_string(index=False))