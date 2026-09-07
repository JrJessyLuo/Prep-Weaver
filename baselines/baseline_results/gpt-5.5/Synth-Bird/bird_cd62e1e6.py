import pandas as pd

t1 = tables["table_1"]
heroes = tables["table_2"]

# Build publisher lookup (publisher_id -> publisher_name) from the transposed/key-value style table_1
pub_row = t1.loc[t1["id"].astype(str).str.strip().eq("publisher_name")].drop(columns=["id"])
publisher_lu = (
    pub_row.T.reset_index()
    .rename(columns={"index": "publisher_id", pub_row.index[0]: "publisher_name"})
)
publisher_lu["publisher_id"] = pd.to_numeric(publisher_lu["publisher_id"], errors="coerce")

# Get publisher for superhero ID 38
hero_pub = heroes.loc[heroes["id"].eq(38), ["publisher_id"]].copy()
hero_pub["publisher_id"] = pd.to_numeric(hero_pub["publisher_id"], errors="coerce")

out = hero_pub.merge(publisher_lu, on="publisher_id", how="left")[["publisher_name"]]

result = {"publisher_name_for_superhero_38": out.reset_index(drop=True)}
