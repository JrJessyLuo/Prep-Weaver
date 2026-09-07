import pandas as pd

heroes = tables["table_1"]
powers_wide = tables["table_2"].copy()

# Treat all columns except the first ("hero_id") as hero columns whose cells list power_ids
hero_cols = [c for c in powers_wide.columns if c != "hero_id"]

# Convert cell values like '"120"' -> 120; non-numeric -> NaN
powers_num = powers_wide[hero_cols].apply(
    lambda s: pd.to_numeric(s.astype(str).str.strip().str.replace('"', "", regex=False), errors="coerce")
)

# Count how many non-null power entries each hero column has (handle duplicated column names by summing)
power_counts = powers_num.notna().sum(axis=0)
power_counts = power_counts.groupby(level=0).sum()

# Hero (column) with the most powers
top_hero_col = power_counts.sort_values(ascending=False).index[0]
top_hero_id = int(pd.to_numeric(top_hero_col, errors="coerce"))

top_name = heroes.loc[heroes["id"] == top_hero_id, "superhero_name"].iloc[0]
result_df = pd.DataFrame({"superhero_name": [top_name]})

result = {"superhero_with_most_powers": result_df}
