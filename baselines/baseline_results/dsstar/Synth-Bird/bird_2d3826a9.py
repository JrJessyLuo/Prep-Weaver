import pandas as pd

# Tables are preloaded in-scope as `tables`
player_attr = tables["table_1"]       # bird_2d3826a9_input_0.pkl
player_meta_long = tables["table_2"]  # bird_2d3826a9_input_1.pkl

# ---- Reproduce reference logic ----
need_vars = ["first_name", "lname", "p_api"]
meta_subset = player_meta_long[player_meta_long["variable"].isin(need_vars)].copy()

player_meta_wide = (
    meta_subset.pivot_table(index="id", columns="variable", values="value", aggfunc="first")
    .reset_index()
)

def _norm(s):
    return str(s).strip().lower() if pd.notna(s) else ""

for c in ["first_name", "lname"]:
    if c in player_meta_wide.columns:
        player_meta_wide[c] = player_meta_wide[c].map(_norm)

aaron_rows = player_meta_wide[
    (player_meta_wide.get("first_name", pd.Series("", index=player_meta_wide.index)) == "aaron")
    & (player_meta_wide.get("lname", pd.Series("", index=player_meta_wide.index)) == "doran")
].copy()

aaron_player_api_ids = (
    pd.to_numeric(aaron_rows.get("p_api", pd.Series([], dtype=object)), errors="coerce")
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

aaron_doran_attr = player_attr[player_attr["player_api_id"].isin(aaron_player_api_ids)].copy()
if not aaron_doran_attr.empty:
    aaron_doran_attr = aaron_doran_attr.sort_values(["player_api_id", "date"])

# ---- Compute average overall rating ----
avg_overall = aaron_doran_attr["overall_rating"].mean()

answer_df = pd.DataFrame(
    [{"player_name": "Aaron Doran", "average_overall_rating": avg_overall}]
)

result = {"average_overall_rating": answer_df}