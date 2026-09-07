import pandas as pd

t1 = tables["table_1"].copy()
t2 = tables["table_2"].copy()

# Colour lookup (code -> colour name)
colour_lu = (
    t1[t1["id"].astype(str).str.lower() == "colour"][["variable", "colour"]]
    .drop_duplicates()
    .assign(variable=lambda d: d["variable"].astype(str))
)

# Find Blackwulf and map eye colour code (yc) to colour name
bw = t2[t2["superhero_name"].astype(str).str.casefold() == "blackwulf"].copy()
bw["yc"] = bw["yc"].astype(str)

out = (
    bw.merge(colour_lu, left_on="yc", right_on="variable", how="left")
    .rename(columns={"colour": "eye_colour"})
    [["eye_colour"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

result = {"eye_colour_of_blackwulf": out}
