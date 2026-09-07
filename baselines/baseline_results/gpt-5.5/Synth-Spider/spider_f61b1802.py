import pandas as pd

t1 = tables["table_1"]
t2 = tables["table_2"]

institutions = t1[["Institution_ID", "Name"]].drop_duplicates(subset=["Institution_ID"])
nicknames = t2[["Institution_ID", "Nickname"]].drop_duplicates(subset=["Institution_ID"])

out = institutions.merge(nicknames, on="Institution_ID", how="left")
out = out[["Name", "Nickname"]].drop_duplicates().reset_index(drop=True)

result = {"institutions_names_nicknames": out}
