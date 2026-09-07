import pandas as pd

# Tables already loaded in-scope as `tables`
colours = tables["table_1"]  # bird_5bffd56f_input_0.pkl
heroes = tables["table_2"]   # bird_5bffd56f_input_1.pkl

target_name = "Blackwulf"

# Retrieve yc for superhero_name == "Blackwulf"
hero_match = heroes.loc[
    heroes["superhero_name"].astype(str).eq(target_name),
    ["id", "superhero_name", "yc"]
]

if len(hero_match) == 1 and not pd.isna(hero_match["yc"].iloc[0]):
    yc_code_int = int(hero_match["yc"].iloc[0])

    # Look up yc in colour lookup table
    colour_match = colours.loc[
        colours["variable"].astype(str).eq(str(yc_code_int)),
        ["colour"]
    ]

    answer_df = colour_match.head(1).reset_index(drop=True)
else:
    answer_df = pd.DataFrame({"colour": []})

result = {"blackwulf_eye_colour": answer_df}