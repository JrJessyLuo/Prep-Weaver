import pandas as pd

sailors = tables["table_1"].copy()
reserves = tables["table_2"].copy()

# Sailors with rating >= 3
sailors_f = sailors[sailors["rtg"] >= 3]

# Sailors who reserved at least one boat
reserved_sids = reserves["sid"].dropna().unique()

out = sailors_f[sailors_f["s_id"].isin(reserved_sids)][["s_id", "name"]].drop_duplicates().reset_index(drop=True)

result = {"sailors_with_rating_at_least_3_and_reserved": out}
