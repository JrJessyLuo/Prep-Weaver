import pandas as pd

# Load the two relevant DataFrames from the provided tables dict
player_attributes = tables["table_1"]  # has preferred_foot
player_info = tables["table_2"]        # has birthday

# Select relevant columns
player_attributes_sel = player_attributes[["player_api_id", "preferred_foot"]].copy()
player_info_sel = player_info[["player_api_id", "birthday"]].copy()

# Parse birthday to datetime
player_info_sel["birthday"] = pd.to_datetime(player_info_sel["birthday"], errors="coerce")

# Merge on player_api_id
merged = player_attributes_sel.merge(player_info_sel, on="player_api_id", how="left")

# Drop duplicate player_api_id rows
merged_dedup = merged.drop_duplicates(subset=["player_api_id"], keep="first").copy()

# Filter to birth years 1987–1992 inclusive
birth_year = merged_dedup["birthday"].dt.year
filtered = merged_dedup[birth_year.between(1987, 1992, inclusive="both")].copy()

# Compute percentage of left-footed players (exclude missing preferred_foot)
filtered = filtered[filtered["preferred_foot"].notna()].copy()
total_count = len(filtered)
left_count = (filtered["preferred_foot"].str.lower() == "left").sum()

left_foot_percentage = 100 * (left_count / total_count) if total_count else float("nan")

# Final answer table
answer_df = pd.DataFrame(
    {"left_foot_percentage": [left_foot_percentage]}
)

result = {"left_foot_percentage_born_1987_1992": answer_df}