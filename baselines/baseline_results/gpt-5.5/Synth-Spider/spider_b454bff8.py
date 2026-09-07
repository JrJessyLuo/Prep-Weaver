import pandas as pd

df1 = tables["table_1"]
df2 = tables["table_2"]

out = (
    df1.merge(df2, left_on="Institution_ID", right_on="iid", how="inner")
       .loc[:, ["Name", "Nickname"]]
       .drop_duplicates()
       .reset_index(drop=True)
)

result = {"institutions_and_nicknames": out}
