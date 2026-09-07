import pandas as pd

# Tables already loaded in scope as `tables`
attributes_raw = tables["table_1"]   # bird_fcdb05fc_input_0.pkl
superheroes = tables["table_2"]      # bird_fcdb05fc_input_1.pkl
hero_attr_values = tables["table_3"] # bird_fcdb05fc_input_2.pkl

# Find 3-D Man's hero_id
hero_row = superheroes.loc[superheroes["superhero_name"] == "3-D Man", ["id", "superhero_name"]]
hero_id = hero_row["id"].iloc[0] if not hero_row.empty else None

if hero_id is None:
    answer_df = pd.DataFrame(columns=["attribute_name", "av"])
else:
    # Convert the single-row "id"/"attribute_name" list-like columns into a proper mapping table
    attr_map = attributes_raw.explode(["id", "attribute_name"]).copy()
    attr_map["aid"] = pd.to_numeric(attr_map["id"], errors="coerce").astype("Int64")
    attr_map = attr_map[["aid", "attribute_name"]]

    # Filter for hero and join to attribute names
    answer_df = (
        hero_attr_values.loc[hero_attr_values["hero_id"] == hero_id, ["aid", "av"]]
        .merge(attr_map, on="aid", how="left")
        .loc[:, ["attribute_name", "av"]]
        .sort_values("attribute_name", na_position="last")
        .reset_index(drop=True)
    )

# Final answer in required format
result = {"3_d_man_attributes": answer_df}