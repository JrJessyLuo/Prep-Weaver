import pandas as pd

colors = tables["table_1"].copy()
heroes = tables["table_2"].copy()

# Normalize color names
colors["yanse_norm"] = (
    colors["yanse"].astype(str).str.strip().str.lower()
)

# Get colour IDs for blue eyes and blond hair (handle blond/blonde variants)
blue_ids = colors.loc[colors["yanse_norm"].eq("blue"), "leibie"].dropna().astype(int).unique()
blond_ids = colors.loc[colors["yanse_norm"].isin(["blond", "blonde"]), "leibie"].dropna().astype(int).unique()

# Filter heroes by eye color (eid) and hair color (hid)
out = heroes[
    heroes["eid"].isin(blue_ids) & heroes["hid"].isin(blond_ids)
][["superhero_name"]].drop_duplicates().sort_values("superhero_name").reset_index(drop=True)

result = {"blue_eyes_blond_hair_superheroes": out}
