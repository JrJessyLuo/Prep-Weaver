import pandas as pd

# tables are assumed to be already loaded in scope as a dict of DataFrames:
# tables['table_1'] -> bird_cd62e1e6_input_0.pkl (publisher mapping, wide)
# tables['table_2'] -> bird_cd62e1e6_input_1.pkl (superhero table)

df = tables["table_2"]

# Get publisher_id for superhero with id == 38
publisher_id = df.loc[df["id"] == 38, "publisher_id"].iloc[0]

pub_wide = tables["table_1"]

# Convert wide mapping to long: (publisher_id, publisher_name)
pub_long = (
    pub_wide.set_index("id")
    .T
    .reset_index()
    .rename(columns={"index": "publisher_id", "publisher_name": "publisher_name"})
)

# Coerce publisher_id to numeric to match superhero publisher_id
pub_long["publisher_id"] = pd.to_numeric(pub_long["publisher_id"], errors="coerce")

# Join and read publisher_name
publisher_name = pub_long.loc[pub_long["publisher_id"] == publisher_id, "publisher_name"].iloc[0]

answer_df = pd.DataFrame({"publisher_name": [publisher_name]})
result = {"publisher_name_for_superhero_38": answer_df}