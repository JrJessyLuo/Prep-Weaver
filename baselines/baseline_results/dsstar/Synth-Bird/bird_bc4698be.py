import pandas as pd

# Input tables are already loaded in `tables`
colours = tables["table_1"]  # bird_bc4698be_input_0.pkl
heroes = tables["table_2"]   # bird_bc4698be_input_1.pkl

# Prepare lookup key for join
colours = colours.copy()
colours["leibie_int"] = pd.to_numeric(colours["leibie"], errors="coerce").astype("Int64")

def attach_colour_name(df, fk_col, lookup, lookup_key="leibie_int", lookup_value="yanse", out_col=None):
    out_col = out_col or f"{fk_col}_colour_name"
    tmp = (
        lookup[[lookup_key, lookup_value]]
        .drop_duplicates()
        .rename(columns={lookup_key: fk_col, lookup_value: out_col})
    )
    return df.merge(tmp, on=fk_col, how="left")

# Map eid/hid to colour names
heroes_mapped = heroes.copy()
for fk in ["eid", "hid"]:
    heroes_mapped = attach_colour_name(heroes_mapped, fk, colours)

# Filter: blue eyes + blond hair; deduplicate and sort names
answer_df = (
    heroes_mapped.loc[
        (heroes_mapped["eid_colour_name"] == "Blue") &
        (heroes_mapped["hid_colour_name"] == "Blond"),
        ["superhero_name"]
    ]
    .dropna()
    .drop_duplicates()
    .sort_values("superhero_name")
    .reset_index(drop=True)
)

# Final answer per guidelines
result = {"blue_eyes_blond_hair_superheroes": answer_df}