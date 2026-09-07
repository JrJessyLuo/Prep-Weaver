import pandas as pd

artists = tables["table_1"]
paintings = tables["table_2"]

mary_ids = artists.loc[artists["fname"].astype(str).str.strip().eq("Mary"), "artistID"]

out = paintings[paintings["painterID"].isin(mary_ids)][["title", "year"]].drop_duplicates().reset_index(drop=True)

result = {"mary_paintings": out}
