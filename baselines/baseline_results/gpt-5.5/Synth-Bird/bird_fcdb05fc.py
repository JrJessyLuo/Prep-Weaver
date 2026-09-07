import pandas as pd

# Load tables
attr = tables["table_1"].copy()
heroes = tables["table_2"].copy()
hero_attr_vals = tables["table_3"].copy()

# Find 3-D Man hero id
hero_id = heroes.loc[heroes["superhero_name"].eq("3-D Man"), "id"].iloc[0]

# Prep attribute id types for join
attr["id"] = pd.to_numeric(attr["id"], errors="coerce")

# Filter and join to get attribute names with values
out = (
    hero_attr_vals.loc[hero_attr_vals["hero_id"].eq(hero_id)]
    .merge(attr, left_on="aid", right_on="id", how="left")
    .sort_values(["aid"])
    .rename(columns={"av": "attribute_value"})
    [["attribute_name", "attribute_value"]]
    .reset_index(drop=True)
)

result = {"3d_man_attributes": out}
