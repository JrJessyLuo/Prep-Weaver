import pandas as pd

# Load main superhero table (already in scope via `tables`)
df = tables["table_2"].copy()

# Ensure numeric comparison works even if columns are strings/mixed
df["height_cm"] = pd.to_numeric(df["height_cm"], errors="coerce")
df["weight_kg"] = pd.to_numeric(df["weight_kg"], errors="coerce")

# Filter by height and weight
matches = df[(df["height_cm"] == 188) & (df["weight_kg"] == 108)].copy()

# Get the race of the matching superhero(es)
answer_df = matches[["race"]].drop_duplicates().reset_index(drop=True)

# Final result as required
result = {"superhero_race": answer_df}