import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]
t4 = tables["table_4"]

abom_ids = t1.loc[t1["superhero_name"].eq("Abomination"), "id"].dropna().unique()

out = (
    t2[t2["hero_id"].isin(abom_ids)]
    .merge(t4, left_on="attribute_id", right_on="id", how="left")
    .assign(attribute_value=lambda d: d["attribute_value"].astype(str).str.strip().str.strip('"'))
    .loc[:, ["attribute_name", "attribute_value"]]
    .sort_values("attribute_name", kind="stable")
    .reset_index(drop=True)
)

result = {"abomination_attribute_values": out}
