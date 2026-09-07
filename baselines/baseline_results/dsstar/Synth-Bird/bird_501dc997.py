import pandas as pd

# Source tables from the preloaded `tables` dict (no file I/O)
df_attr_values = tables["table_2"]  # bird_501dc997_input_1.pkl
df_attr_lookup = tables["table_4"]  # superhero_attribute.pkl

# Reproduce the reference logic: filter for hero_id == 5 (Abomination), join to lookup,
# select relevant columns, sort, and reset index
abomination_attributes = (
    df_attr_values.loc[df_attr_values["hero_id"].eq(5)]
    .merge(df_attr_lookup, left_on="attribute_id", right_on="id", how="left")
    .loc[:, ["hero_id", "attribute_id", "attribute_name", "attribute_value"]]
    .sort_values("attribute_id")
    .reset_index(drop=True)
)

# Final answer
result = {"abomination_attribute_values": abomination_attributes}