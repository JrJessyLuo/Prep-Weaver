import pandas as pd

# Build a normalized colour lookup (handle split colours like "Black/Blue")
col = tables["table_1"].copy()
col["colour"] = col["colour_part1"].fillna("")
mask = col["sep"].notna() & col["part2"].notna()
col.loc[mask, "colour"] = (
    col.loc[mask, "colour_part1"].astype(str)
    + col.loc[mask, "sep"].astype(str)
    + col.loc[mask, "part2"].astype(str)
)
col_lookup = col[["id", "colour"]]

heroes = tables["table_2"].copy()

# Join hair colour
heroes = heroes.merge(
    col_lookup.rename(columns={"id": "hair_colour_id", "colour": "hair_colour"}),
    on="hair_colour_id",
    how="left",
)

# Join eye colour (infer: yc is eye_colour_id)
heroes = heroes.merge(
    col_lookup.rename(columns={"id": "yc", "colour": "eye_colour"}),
    on="yc",
    how="left",
)

# Filter heroes with both hair and eyes exactly "Black"
m = (heroes["hair_colour"].str.strip().str.lower() == "black") & (
    heroes["eye_colour"].str.strip().str.lower() == "black"
)

out = (
    heroes.loc[m, ["superhero_name"]]
    .dropna()
    .drop_duplicates()
    .sort_values("superhero_name")
    .reset_index(drop=True)
    .rename(columns={"superhero_name": "hero_name"})
)

result = {"heroes_black_eyes_and_hair": out}
