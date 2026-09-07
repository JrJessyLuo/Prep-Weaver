import pandas as pd

# Tables already loaded in-scope as `tables`
colours = tables["table_1"]  # bird_fab5fab4_input_0.pkl
heroes = tables["table_2"]   # bird_fab5fab4_input_1.pkl

# 1) Identify the colour ID(s) that correspond to “Black” in the colours lookup table
black_colour_ids = (
    colours.loc[colours["colour_part1"].astype(str).str.strip().str.casefold() == "black", "id"]
    .dropna()
    .astype(int)
    .unique()
    .tolist()
)

# 2) Inspect heroes table for an eye-colour column
possible_eye_cols = [
    "eye_colour_id",
    "eye_color_id",
    "eyes_colour_id",
    "eyes_color_id",
    "eye_id",
    "eyes_id",
]
eye_col = next((c for c in possible_eye_cols if c in heroes.columns), None)

if eye_col is None:
    raise KeyError(
        "No eye colour column found in heroes table.\n"
        f"Heroes columns: {list(heroes.columns)}"
    )

# 3) Filter heroes where hair_colour_id is Black AND eye_colour_id is Black, then output superhero_name
final_df = (
    heroes.loc[
        heroes["hair_colour_id"].isin(black_colour_ids) & heroes[eye_col].isin(black_colour_ids),
        ["superhero_name"],
    ]
    .dropna()
    .drop_duplicates()
    .sort_values("superhero_name")
    .reset_index(drop=True)
)

result = {"heroes_with_black_eyes_and_hair": final_df}